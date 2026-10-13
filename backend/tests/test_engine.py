from app.game.engine import build_report
from app.game.islands import ISLANDS
from app.game.scenarios import SCENARIOS, get_cards, setup


def _game(island_id, scenario_id="strait_crisis"):
    return setup(island_id, scenario_id)


def _baseline(island, scenario):
    return [(c["id"], next(o["id"] for o in c["options"] if o.get("baseline"))) for c in get_cards(island, scenario)]


def _with(island, scenario, **overrides):
    return [(cid, overrides.get(cid, oid)) for cid, oid in _baseline(island, scenario)]


def _summary(island, scenario, **overrides):
    return build_report(island, scenario, _with(island, scenario, **overrides))["summary"]


def test_every_scenario_island_and_option_simulates():
    for scenario_id in SCENARIOS:
        for island_id in ISLANDS:
            island, scenario = _game(island_id, scenario_id)
            cards = get_cards(island, scenario)
            assert len(cards) == 7
            assert len({c["id"] for c in cards}) == 7
            for card in cards:
                assert sum(1 for o in card["options"] if o.get("baseline")) == 1, (scenario_id, card["id"])
                assert "{" not in card["situation"] + card["title"], (scenario_id, card["id"])
                for opt in card["options"]:
                    report = build_report(island, scenario, _with(island, scenario, **{card["id"]: opt["id"]}))
                    assert len(report["simulation"]["timeline"]) == 8
                    assert 0 <= report["summary"]["approval_end"] <= 100
                    assert all("{" not in step for step in opt["chain"]), (scenario_id, opt["id"])


def test_scenarios_have_different_questions():
    island = ISLANDS["coralia"]
    decks = {sid: {c["title"] for c in get_cards(*_game(island["id"], sid))} for sid in SCENARIOS}
    for a in decks:
        for b in decks:
            if a != b:
                assert len(decks[a] & decks[b]) <= 3, (a, b)  # only the shared desks (rates, company, future)


def test_company_trouble_depends_on_scenario():
    texts = {get_cards(*_game("nordhaven", sid))[5]["situation"] for sid in SCENARIOS}
    assert len(texts) == len(SCENARIOS)


def test_printing_money_raises_inflation_and_weakens_currency():
    island, scenario = _game("coralia")
    base = _summary(island, scenario)
    printed = _summary(island, scenario, fuel="print_cash")
    assert printed["peak_inflation"] > base["peak_inflation"] + 3
    assert printed["currency_change"] < base["currency_change"]


def test_printing_in_a_slump_is_less_inflationary():
    island, war = _game("nordhaven")
    run_island, bank_run = _game("nordhaven", "bank_run")
    war_extra = _summary(island, war, company="bailout")["peak_inflation"] - _summary(island, war)["peak_inflation"]
    run_extra = (_summary(run_island, bank_run, qe="big_qe")["peak_inflation"]
                 - _summary(run_island, bank_run)["peak_inflation"])
    assert run_extra < war_extra


def test_rate_hike_lowers_inflation_but_costs_jobs():
    island, scenario = _game("nordhaven")
    base = _summary(island, scenario)
    hawk = _summary(island, scenario, rates="hike_big")
    assert hawk["end_inflation"] < base["end_inflation"]
    assert hawk["avg_unemployment"] > base["avg_unemployment"]


def test_trust_matters_same_printing_hurts_poor_island_more():
    def extra(iid):
        island, scenario = _game(iid)
        return _summary(island, scenario, fuel="print_cash")["peak_inflation"] - _summary(island, scenario)["peak_inflation"]
    assert extra("kalani") > extra("aurelia")


def test_pandemic_wage_scheme_protects_jobs():
    island, scenario = _game("coralia", "grey_fever")
    assert (_summary(island, scenario, jobs="furlough")["avg_unemployment"]
            < _summary(island, scenario)["avg_unemployment"])


def test_terror_hits_tourist_islands_hardest():
    def slump(iid):
        island, scenario = _game(iid, "harbour_attack")
        return _summary(island, scenario)["avg_unemployment"] - island["start"]["unemployment"]
    assert slump("coralia") > slump("nordhaven")


def test_bank_run_guarantee_beats_letting_it_run():
    island, scenario = _game("terrava", "bank_run")
    calm = _summary(island, scenario, deposits="guarantee_all")
    panic = _summary(island, scenario, deposits="nothing")
    assert calm["avg_unemployment"] < panic["avg_unemployment"]


def test_hidden_debt_starts_with_more_debt_and_less_trust():
    island, scenario = _game("coralia", "hidden_debt")
    assert island["start"]["debt_to_gdp"] == ISLANDS["coralia"]["start"]["debt_to_gdp"] + 15
    assert island["credibility"] < ISLANDS["coralia"]["credibility"]
    assert ISLANDS["coralia"]["start"]["debt_to_gdp"] == 52.0  # the shared island data is untouched


def test_tariffs_raise_prices_at_home():
    island, scenario = _game("nordhaven", "tariff_wall")
    assert (_summary(island, scenario, retaliate="match")["peak_inflation"]
            > _summary(island, scenario)["peak_inflation"])


def test_consequence_map_measures_non_baseline_choices():
    island, scenario = _game("terrava")
    report = build_report(island, scenario, _with(island, scenario, fuel="print_cash", future="green"))
    entry = next(e for e in report["consequence_map"] if e["card_id"] == "fuel")
    infl = next(i for i in entry["impact"] if i["key"] == "peak_inflation")
    assert infl["delta"] > 0 and infl["good"] is False
    assert all("what_if" in e for e in report["consequence_map"])


def test_every_quarter_has_real_news():
    for scenario_id in SCENARIOS:
        for island_id in ISLANDS:
            island, scenario = _game(island_id, scenario_id)
            report = build_report(island, scenario, _baseline(island, scenario))
            for quarter in report["headlines"]:
                assert not quarter["items"][0]["text"].startswith("Steady quarter"), (scenario_id, island_id, quarter)
            first = report["headlines"][0]["items"][0]["text"]
            assert first.startswith(scenario["news"]["during"][0].split("{")[0][:12]), (scenario_id, first)
