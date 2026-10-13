"""The crises a Governor can face. Every island can be played against every scenario.

A scenario module provides:
  SCENARIO  - title, intro, briefing and the `shock`: how the crisis hits the economy quarter by
              quarter (see `engine.simulate`), plus optional changes to the island's starting point.
  cards()   - the seven visitors of the day, built for a given island.
"""

from copy import deepcopy

from ..islands import get_island
from . import bank_run, pandemic, scandal, terror, trade_war, war
from .common import fmt

_MODULES = [war, pandemic, terror, scandal, trade_war, bank_run]
SCENARIOS: dict[str, dict] = {m.SCENARIO["id"]: m.SCENARIO for m in _MODULES}
_CARDS = {m.SCENARIO["id"]: m.cards for m in _MODULES}
DEFAULT_SCENARIO = war.SCENARIO["id"]

_PUBLIC_KEYS = ("id", "category", "icon", "title", "tagline", "intro", "briefing", "teaches", "map", "status",
                "causes")


def get_scenario(scenario_id: str) -> dict | None:
    return SCENARIOS.get(scenario_id)


def island_for(island: dict, scenario: dict) -> dict:
    """The island as it stands on the morning the crisis breaks."""
    island = deepcopy(island)
    shock = scenario["shock"]
    for key, delta in shock.get("start", {}).items():
        island["start"][key] = round(island["start"][key] + delta, 2)
    island["credibility"] = round(island["credibility"] + shock.get("credibility", 0.0), 3)
    island["company"]["crisis"] = island["company"]["crises"][scenario["id"]]
    return island


def setup(island_id: str, scenario_id: str) -> tuple[dict, dict] | None:
    island, scenario = get_island(island_id), get_scenario(scenario_id)
    if island is None or scenario is None:
        return None
    return island_for(island, scenario), scenario


def get_cards(island: dict, scenario: dict) -> list[dict]:
    return _CARDS[scenario["id"]](island)


def public_scenario(scenario: dict, island: dict | None = None) -> dict:
    out = {k: deepcopy(scenario.get(k)) for k in _PUBLIC_KEYS}
    if island is not None:
        out["intro"] = fmt(out["intro"], island)
        out["briefing"] = [fmt(b, island) for b in out["briefing"]]
    else:
        out["intro"] = out["intro"].replace("{island}", "your island")
        out["briefing"] = [b.replace("{currency}", "local currency") for b in out["briefing"]]
    return out


def find_option(cards: list[dict], card_id: str, option_id: str) -> dict | None:
    for card in cards:
        if card["id"] == card_id:
            return next((o for o in card["options"] if o["id"] == option_id), None)
    return None


def baseline_option(card: dict) -> dict:
    return next(o for o in card["options"] if o.get("baseline"))
