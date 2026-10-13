"""Play without accounts or a database.

The browser keeps the game (island, crisis and the choices made so far) and sends it with every
request. Everything else (the next visitor, the reactions, the two-year report) is rebuilt from
those choices, so the server stores nothing.
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..game.engine import build_report, live_stats, start_sustainability
from ..game.islands import WORLD, get_island, public_islands
from ..game.scenarios import SCENARIOS, find_option, get_cards, public_scenario, setup

router = APIRouter(prefix="/api", tags=["play"])


class PlayIn(BaseModel):
    island_id: str
    scenario_id: str
    decisions: list[tuple[str, str]] = Field(default_factory=list, max_length=20)  # (card_id, option_id)


class DecideIn(PlayIn):
    card_id: str
    option_id: str


@router.get("/islands")
def islands() -> dict:
    return {
        "islands": [{**i, "start": {**i["start"], "sustainability": start_sustainability(i)}} for i in public_islands()],
        "world": WORLD,
        "scenarios": [public_scenario(s) for s in SCENARIOS.values()],
    }


def _load(body: PlayIn) -> tuple[dict, dict, list[dict], list[dict]]:
    """Check the game the browser sent and turn its choices back into card options."""
    if get_island(body.island_id) is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown island")
    found = setup(body.island_id, body.scenario_id)
    if found is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown scenario")
    island, scenario = found
    cards = get_cards(island, scenario)
    if len(body.decisions) > len(cards):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Too many decisions")
    options = []
    for card, (card_id, option_id) in zip(cards, body.decisions):
        option = find_option(cards, card_id, option_id) if card_id == card["id"] else None
        if option is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "These decisions don't match the day's visitors")
        options.append(option)
    return island, scenario, cards, options


def _reaction(island: dict, before: list[dict], option: dict) -> dict:
    """What a choice did straight away: the crowd, plus how the headline numbers moved."""
    was, now = live_stats(island, before), live_stats(island, before + [option])
    return {**option["today"], "deltas": {k: round(now[k] - was[k], 2) for k in now if isinstance(now[k], (int, float))}}


def _view(island: dict, scenario: dict, cards: list[dict], options: list[dict]) -> dict:
    step = len(options)
    return {
        "status": "in_office" if step < len(cards) else "day_over",
        "island": {**island, "start": {**island["start"], "sustainability": start_sustainability(island)}},
        "scenario": public_scenario(scenario, island),
        "step": step,
        "total_steps": len(cards),
        "card": cards[step] if step < len(cards) else None,
        "live_stats": live_stats(island, options),
        # Who is coming today, in order (titles stay hidden until each visitor arrives)
        "agenda": [{"time": c["time"], "speaker": c["speaker"], "speaker_icon": c["speaker_icon"]} for c in cards],
        "decisions": [
            {
                "step": i, "card_id": card["id"], "option_id": option["id"], "card_title": card["title"],
                "option_title": option["title"], "icon": option["icon"], "time": card["time"],
                "reaction": _reaction(island, options[:i], option),
                "card": card,  # the full question, so the player can look back at it
            }
            for i, (card, option) in enumerate(zip(cards, options))
        ],
    }


@router.post("/play")
def play(body: PlayIn) -> dict:
    """The game as it stands after the choices made so far."""
    return _view(*_load(body))


@router.post("/play/decide")
def decide(body: DecideIn) -> dict:
    island, scenario, cards, options = _load(body)
    if len(options) >= len(cards):
        raise HTTPException(status.HTTP_409_CONFLICT, "The day is already over")
    card = cards[len(options)]
    if body.card_id != card["id"]:
        raise HTTPException(status.HTTP_409_CONFLICT, "That decision isn't on your desk right now")
    option = find_option(cards, body.card_id, body.option_id)
    if option is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown option")
    return {"reaction": _reaction(island, options, option), "game": _view(island, scenario, cards, options + [option])}


@router.post("/play/report")
def report(body: PlayIn) -> dict:
    island, scenario, cards, options = _load(body)
    if len(options) < len(cards):
        raise HTTPException(status.HTTP_409_CONFLICT, "You still have decisions to make today")
    return build_report(island, scenario, [(o_card["id"], o["id"]) for o_card, o in zip(cards, options)])
