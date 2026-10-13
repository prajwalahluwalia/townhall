from app.game.cards import get_cards
from app.game.engine import build_report
from app.game.islands import ISLANDS


def _baseline(island):
    return [(c["id"], next(o["id"] for o in c["options"] if o.get("baseline"))) for c in get_cards(island)]


def _with(island, **overrides):
    return [(cid, overrides.get(cid, oid)) for cid, oid in _baseline(island)]


def test_every_island_and_option_simulates():
    for island in ISLANDS.values():
        for card in get_cards(island):
            for opt in card["options"]:
                report = build_report(island, _with(island, **{card["id"]: opt["id"]}))
                assert len(report["simulation"]["timeline"]) == 8
                assert 0 <= report["summary"]["approval_end"] <= 100


def test_printing_money_raises_inflation_and_weakens_currency():
    island = ISLANDS["coralia"]
    base = build_report(island, _baseline(island))["summary"]
    printed = build_report(island, _with(island, fuel="print_cash"))["summary"]
    assert printed["peak_inflation"] > base["peak_inflation"] + 3
    assert printed["currency_change"] < base["currency_change"]


def test_rate_hike_lowers_inflation_but_costs_jobs():
    island = ISLANDS["nordhaven"]
    base = build_report(island, _baseline(island))["summary"]
    hawk = build_report(island, _with(island, rates="hike_big"))["summary"]
    assert hawk["end_inflation"] < base["end_inflation"]
    assert hawk["avg_unemployment"] > base["avg_unemployment"]


def test_trust_matters_same_printing_hurts_poor_island_more():
    def extra(iid):
        island = ISLANDS[iid]
        return (build_report(island, _with(island, fuel="print_cash"))["summary"]["peak_inflation"]
                - build_report(island, _baseline(island))["summary"]["peak_inflation"])
    assert extra("kalani") > extra("aurelia")


def test_consequence_map_measures_non_baseline_choices():
    island = ISLANDS["terrava"]
    report = build_report(island, _with(island, fuel="print_cash", future="green"))
    entry = next(e for e in report["consequence_map"] if e["card_id"] == "fuel")
    infl = next(i for i in entry["impact"] if i["key"] == "peak_inflation")
    assert infl["delta"] > 0 and infl["good"] is False
    assert all("what_if" in e for e in report["consequence_map"])
