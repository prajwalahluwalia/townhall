from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..auth import current_user
from ..db import get_db
from ..game.engine import build_report, live_stats, start_sustainability
from ..game.islands import WORLD, get_island, public_islands
from ..game.scenarios import SCENARIOS, find_option, get_cards, public_scenario, setup
from ..models import Decision, Game, User
from ..schemas import DecisionIn, NewGameIn

router = APIRouter(prefix="/api", tags=["game"])


@router.get("/islands")
def islands() -> dict:
    return {
        "islands": [{**i, "start": {**i["start"], "sustainability": start_sustainability(i)}} for i in public_islands()],
        "world": WORLD,
        "scenarios": [public_scenario(s) for s in SCENARIOS.values()],
    }


def _own_game(game_id: int, user: User, db: Session) -> Game:
    game = db.get(Game, game_id)
    if game is None or game.user_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Game not found")
    return game


def _setup(game: Game) -> tuple[dict, dict]:
    found = setup(game.island_id, game.scenario_id)
    if found is None:
        raise HTTPException(status.HTTP_410_GONE, "This term's island or scenario no longer exists")
    return found


def _decision_view(cards: list[dict], d: Decision) -> dict:
    card = next(c for c in cards if c["id"] == d.card_id)
    option = find_option(cards, d.card_id, d.option_id)
    return {
        "step": d.step, "card_id": d.card_id, "option_id": d.option_id, "reaction": d.reaction,
        "card_title": card["title"], "option_title": option["title"], "icon": option["icon"], "time": card["time"],
    }


def _game_view(game: Game) -> dict:
    island, scenario = _setup(game)
    cards = get_cards(island, scenario)
    step = game.current_step
    return {
        "id": game.id,
        "status": game.status,
        "island": {**island, "start": {**island["start"], "sustainability": start_sustainability(island)}},
        "scenario": public_scenario(scenario, island),
        "step": step,
        "total_steps": len(cards),
        "card": cards[step] if game.status == "in_office" and step < len(cards) else None,
        "live_stats": game.live_stats,
        "decisions": [_decision_view(cards, d) for d in game.decisions],
        "score": game.score,
        "ending": game.ending,
        "created_at": game.created_at.isoformat(),
    }


@router.get("/games")
def list_games(user: User = Depends(current_user), db: Session = Depends(get_db)) -> list[dict]:
    games = db.scalars(select(Game).where(Game.user_id == user.id).order_by(Game.updated_at.desc())).all()
    out = []
    for g in games:
        found = setup(g.island_id, g.scenario_id)
        island, scenario = found if found else (get_island(g.island_id), SCENARIOS.get(g.scenario_id))
        out.append({
            "id": g.id,
            "island_id": g.island_id,
            "island_name": island["name"] if island else g.island_id,
            "tier_label": island["tier_label"] if island else "",
            "scenario_id": g.scenario_id,
            "scenario_title": scenario["title"] if scenario else g.scenario_id,
            "scenario_icon": scenario["icon"] if scenario else "",
            "status": g.status,
            "step": g.current_step,
            "total_steps": len(get_cards(island, scenario)) if found else 0,
            "score": g.score,
            "ending": g.ending,
            "updated_at": g.updated_at.isoformat(),
        })
    return out


@router.post("/games", status_code=status.HTTP_201_CREATED)
def new_game(body: NewGameIn, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    if get_island(body.island_id) is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown island")
    found = setup(body.island_id, body.scenario_id)
    if found is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown scenario")
    island, scenario = found
    game = Game(user_id=user.id, island_id=island["id"], scenario_id=scenario["id"], live_stats=live_stats(island, []))
    db.add(game)
    db.commit()
    db.refresh(game)
    return _game_view(game)


@router.get("/games/{game_id}")
def get_game(game_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    return _game_view(_own_game(game_id, user, db))


@router.post("/games/{game_id}/decisions")
def decide(game_id: int, body: DecisionIn, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    game = _own_game(game_id, user, db)
    if game.status != "in_office":
        raise HTTPException(status.HTTP_409_CONFLICT, "This term is already over")
    island, scenario = _setup(game)
    cards = get_cards(island, scenario)
    card = cards[game.current_step]
    if body.card_id != card["id"]:
        raise HTTPException(status.HTTP_409_CONFLICT, "That decision isn't on your desk right now")
    option = find_option(cards, body.card_id, body.option_id)
    if option is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown option")

    before = game.live_stats
    chosen = [find_option(cards, d.card_id, d.option_id) for d in game.decisions] + [option]
    after = live_stats(island, chosen)
    reaction = {
        **option["today"],
        "deltas": {k: round(after[k] - before[k], 2) for k in after if isinstance(after[k], (int, float))},
    }
    db.add(Decision(game_id=game.id, step=game.current_step, card_id=card["id"], option_id=option["id"],
                    reaction=reaction))
    game.current_step += 1
    game.live_stats = after
    try:
        db.commit()
    except IntegrityError:  # the same step submitted twice (double click)
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "That decision was already made")
    db.refresh(game)
    return {"reaction": reaction, "game": _game_view(game)}


@router.post("/games/{game_id}/fast-forward")
def fast_forward(game_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    game = _own_game(game_id, user, db)
    if game.status == "completed" and game.result:
        return game.result
    island, scenario = _setup(game)
    if game.current_step < len(get_cards(island, scenario)):
        raise HTTPException(status.HTTP_409_CONFLICT, "You still have decisions to make today")
    report = build_report(island, scenario, [(d.card_id, d.option_id) for d in game.decisions])
    game.result = report
    game.score = report["score"]
    game.ending = report["ending"]["title"]
    game.status = "completed"
    db.commit()
    return report


@router.get("/games/{game_id}/report")
def get_report(game_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)) -> dict:
    game = _own_game(game_id, user, db)
    if not game.result:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This term hasn't finished yet")
    return game.result


@router.delete("/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(game_id: int, user: User = Depends(current_user), db: Session = Depends(get_db)) -> None:
    db.delete(_own_game(game_id, user, db))
    db.commit()
