"""The economic model behind Town Hall.

A deliberately small model with honest mechanics. It runs quarter by quarter for
two years after the player's day in office. Every equation maps to an idea the
game is trying to teach:

  * Inflation  = what people expect it to be (anchored by credibility)
               + demand pull (too much spending: output gap)
               + cost push (oil, grain and other supply shocks from the crisis)
               + imported inflation (a weaker currency makes imports cost more)
               + money printing (new money chasing the same goods; less so in a slump)
               + wage push (pay rises passed on as prices)
  * Money is mostly created by banks when they lend. Interest rates control how
    fast that happens. Printing adds central-bank money on top.
  * The currency moves with interest rates, relative inflation, trust, and the
    oil import bill.
  * Effects are delayed: rate changes take about a year to fully bite.

Each scenario describes its crisis as a `shock`: quarter-by-quarter series for
oil and grain prices, capital flight (risk), lost spending (demand), scarce
goods (supply), frozen lending (credit), emergency spending (fiscal) and
direct job losses (layoffs), plus the quarter the crisis ends.

`simulate` is a pure function of (island, choices, scenario), so the report can
replay it with one choice swapped out to measure what that single decision caused.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .scenarios import baseline_option, get_cards, public_scenario
from .scenarios.common import fmt

QUARTERS = 8
SHOCK_SERIES = ("oil", "grain", "risk", "demand", "supply", "credit", "fiscal", "layoffs")

TARGET_INFLATION = {"rich": 2.0, "developed": 2.0, "developing": 4.0, "poor": 5.0, "very_poor": 6.0}

# Rate changes bite gradually; money printing lands over about a year.
RATE_RAMP = [0.3, 0.6, 0.85, 1.0, 1.0, 1.0, 1.0, 1.0]
PRINT_WEIGHTS = [0.3, 0.35, 0.2, 0.15, 0.0, 0.0, 0.0, 0.0]
# One-off actions (a lockdown, a curfew, a defended currency) fade over the first year.
FADE = [1.0, 0.5, 0.2, 0.0, 0.0, 0.0, 0.0, 0.0]
EASE = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0]

CITIZENS = [
    {"id": "saver", "name": "Meera", "role": "Retired teacher with savings in the bank", "avatar": "saver"},
    {"id": "driver", "name": "Ravi", "role": "Taxi driver, fills up every day", "avatar": "driver"},
    {"id": "farmer", "name": "Tomas", "role": "Farmer with a big bank loan", "avatar": "farmer"},
    {"id": "shop", "name": "Amina", "role": "Runs a corner shop that sells imported goods", "avatar": "shop"},
    {"id": "worker", "name": "Leo", "role": "Works at the island's biggest company", "avatar": "worker"},
]

BASKET = [
    {"id": "bread", "name": "Loaf of bread", "base": 2.0},
    {"id": "fuel", "name": "Litre of petrol", "base": 1.5},
    {"id": "rent", "name": "Monthly rent", "base": 600.0},
    {"id": "phone", "name": "Imported phone", "base": 400.0},
]


def _clamp(x: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, x))


def sustainability_index(env: float, debt: float, reserves: float, company: float, unemployment: float,
                         inflation: float, target: float, credibility: float) -> float:
    """How well the island can keep going: nature, finances, savings, its big employer, people, and trust."""
    reserves_health = _clamp(reserves / 6 * 100, 0, 100)
    fiscal_health = _clamp(100 - debt * 0.55, 0, 100)
    social = _clamp(100 - 2.2 * unemployment - 1.5 * max(inflation - target, 0), 0, 100)
    return (0.25 * env + 0.2 * fiscal_health + 0.15 * reserves_health + 0.1 * company
            + 0.15 * social + 0.15 * credibility * 100)


def start_sustainability(island: dict) -> float:
    s = island["start"]
    return round(sustainability_index(s["environment"], s["debt_to_gdp"], s["reserves_months"],
                                      island["company"]["health"], s["unemployment"], s["inflation"],
                                      TARGET_INFLATION[island["tier"]], island["credibility"]), 1)


@dataclass
class Levers:
    rate_change: float = 0.0
    print_pct: float = 0.0
    credibility: float = 0.0
    fiscal: float = 0.0
    austerity: float = 0.0
    green_invest: float = 0.0
    foreign_borrow: float = 0.0
    wage_push: float = 0.0
    fuel_subsidy: float = 0.0
    contain: float = 0.0          # shrinks the crisis itself (lockdown, deposit guarantee); negative grows it
    drag_now: float = 0.0         # an immediate hit to spending that fades (curfew, bank holiday)
    confidence: float = 0.0       # calms fleeing money and brings spending back sooner
    trade: float = 0.0            # more (or fewer) exports while the crisis lasts
    job_protect: float = 0.0      # keeps people in jobs while spending is down (wage schemes)
    supply_push: float = 0.0      # makes goods dearer (+) or cheaper (−) for about a year
    tariff: float = 0.0           # % tax on imports: dearer goods, and others retaliate
    fx_support: float = 0.0       # reserves spent propping up the currency
    credit: float = 0.0           # bank lending rules: negative means slower lending
    shorten: int = 0              # quarters taken off the crisis
    shorten_if_trusted: int = 0   # ...but only if the world trusts the island
    stance: str | None = None
    company: str | None = None
    price_cap: bool = False
    food_stamps: bool = False
    tariff_cut: bool = False
    strike: bool = False
    un_package: bool = False
    capital_controls: bool = False
    today: dict = field(default_factory=lambda: {"approval": 0.0, "reserves": 0.0, "debt": 0.0, "currency": 0.0})

    @classmethod
    def from_options(cls, options: list[dict]) -> "Levers":
        lv = cls()
        additive = {"rate_change", "print_pct", "credibility", "fiscal", "austerity", "green_invest",
                    "foreign_borrow", "contain", "drag_now", "confidence", "trade", "job_protect", "supply_push",
                    "tariff", "fx_support", "credit", "shorten", "shorten_if_trusted"}
        for opt in options:
            for key, value in opt.get("levers", {}).items():
                if key in additive:
                    setattr(lv, key, getattr(lv, key) + value)
                else:
                    setattr(lv, key, value)
            for key in lv.today:
                lv.today[key] += opt.get("today", {}).get(key, 0.0)
        return lv


def live_stats(island: dict, options: list[dict]) -> dict:
    """What the HUD shows during the day: start values plus immediate reactions only."""
    s = island["start"]
    lv = Levers.from_options(options)
    return {
        "approval": round(_clamp(s["approval"] + lv.today["approval"], 0, 100), 1),
        "reserves_months": round(max(0.0, s["reserves_months"] + lv.today["reserves"]), 2),
        "debt_to_gdp": round(s["debt_to_gdp"] + lv.today["debt"], 1),
        "currency_index": round(s["currency_index"] + lv.today["currency"], 1),
        "inflation": s["inflation"],
        "unemployment": s["unemployment"],
        "interest_rate": round(s["interest_rate"] + lv.rate_change, 2),
        "sustainability": start_sustainability(island),
    }


def _exposure(island: dict, kind: str | None) -> float:
    """How hard a lost-spending shock hits this island, given what it earns its living from."""
    tourism, exports = island["tourism_share"], island["export_sensitivity"]
    return {
        "tourism": 0.5 + 1.2 * tourism,
        "exports": 0.4 + exports,
        "all": 0.5 + (tourism + exports) / 2,
    }.get(kind, 1.0)


def simulate(island: dict, options: list[dict], scenario: dict) -> dict:
    """Run the two years after the day in office. Returns a quarter-by-quarter timeline."""
    lv = Levers.from_options(options)
    s = island["start"]
    q_count = QUARTERS
    target = TARGET_INFLATION[island["tier"]]
    shock = scenario["shock"]

    cred0 = island["credibility"]
    cred = _clamp(cred0 + lv.credibility, 0.03, 0.97)

    # When does the crisis end? Some choices bring it forward (or push it back).
    planned_end = shock["ends"]
    end = planned_end - lv.shorten
    if cred >= 0.7:
        end -= lv.shorten_if_trusted  # trusted islands can actually get others to listen
    end = int(_clamp(end, 2, q_count + 1))
    series = {k: list(shock.get(k, [0.0] * q_count)) for k in SHOCK_SERIES}
    if end < planned_end:
        # The crisis ended early: everything after it moves forward.
        cut = planned_end - end
        series = {k: v[: end - 1] + v[end - 1 + cut:] + [0.0] * cut for k, v in series.items()}
    elif end > planned_end:
        # It dragged on: the worst of it lasts longer.
        extra = end - planned_end
        series = {k: (v[: planned_end - 1] + [v[planned_end - 2]] * extra + v[planned_end - 1:])[:q_count]
                  for k, v in series.items()}
    oil, grain, risk = series["oil"], series["grain"], series["risk"]
    exposure = _exposure(island, shock.get("exposure"))
    contain_scale = _clamp(1 - 0.45 * lv.contain, 0.3, 1.6)
    calm = 1 - _clamp(lv.confidence, -0.6, 0.8)

    oil_mult = {"sanction": 1.25, "neutral": 0.7, "mediate": 1.0}.get(lv.stance, 1.0)
    fuel_dep0 = island["fuel_dependence"]
    food_dep = island["food_dependence"]
    export_sens = island["export_sensitivity"]
    foreign_debt_share = island["foreign_debt_share"] + (0.1 if lv.foreign_borrow else 0.0)
    import_share = (fuel_dep0 + food_dep) / 2 + 0.2

    i0 = s["interest_rate"]
    policy_rate = i0 + lv.rate_change + (1.0 if lv.un_package else 0.0)
    pi0 = s["inflation"]
    u0 = s["unemployment"]

    # State that carries across quarters. Today's immediate reactions are the starting point.
    pi_prev = pi0
    gap = 0.0
    currency = s["currency_index"] + lv.today["currency"]
    reserves = max(0.0, s["reserves_months"] + lv.today["reserves"])
    debt = s["debt_to_gdp"] + lv.today["debt"]
    approval = _clamp(s["approval"] + lv.today["approval"], 0, 100)
    approval_base = s["approval"]
    env = s["environment"]
    company = float(island["company"]["health"])
    price_level = 100.0
    wage_level = 100.0
    real_savings = 100.0
    bank_money, cb_money = 85.0, 15.0
    currency_year_ago = [currency] * 4
    farmer_debt_real = 100.0

    timeline: list[dict] = []
    for q in range(q_count):
        t = q + 1
        oil_t = oil[q] * oil_mult
        grain_t = grain[q]
        active = t < end
        demand_t = series["demand"][q] * exposure * contain_scale
        supply_t = series["supply"][q] * contain_scale
        credit_t = series["credit"][q] * contain_scale
        fiscal_t = series["fiscal"][q]
        layoffs_t = series["layoffs"][q] * exposure * contain_scale * (1 - 0.6 * _clamp(lv.job_protect, 0, 1))
        risk_t = risk[q] * contain_scale * calm * (0.35 if lv.capital_controls else 1.0)
        tariff_t = lv.tariff if t <= 6 else 0.0

        green_cut = min(0.3, lv.green_invest * 0.05 * max(0, t - 3))
        fuel_dep = fuel_dep0 * (1 - green_cut)
        subsidy_on = t <= 4  # nobody can afford a fuel subsidy forever
        subsidy_cover = lv.fuel_subsidy if subsidy_on else 0.0

        # ---- Expectations: how anchored are people to the old normal?
        if pi_prev > target + 4:
            cred = _clamp(cred - 0.03, 0.03, 0.97)
        elif abs(pi_prev - target) < 1.5:
            cred = _clamp(cred + 0.02, 0.03, 0.97)
        expected = cred * pi0 + (1 - cred) * (0.6 * pi_prev + 0.4 * pi0)

        # ---- Demand side: the output gap (economy running hot > 0, cold < 0)
        stimulus = 0.5 * lv.print_pct * [1, 0.7, 0.4, 0.2, 0.1, 0, 0, 0][q]
        fiscal = (lv.fiscal * 0.8 if t <= 4 else 0.0) + (0.25 if lv.food_stamps and t <= 4 else 0.0)
        fiscal += 0.35 * lv.fuel_subsidy if subsidy_on else 0.0
        fiscal -= 0.7 * lv.austerity if t >= 2 else 0.0
        fiscal += (0.2 * lv.green_invest if t <= 4 else 0.15 * lv.green_invest)
        rate_drag = 0.45 * (policy_rate - i0) * RATE_RAMP[q]
        supply_drag = oil_t * fuel_dep * (1 - 0.5 * subsidy_cover) * 0.035
        strike_drag = [1.5, 1.0, 0, 0, 0, 0, 0, 0][q] if lv.strike else 0.0
        shortage_drag = [0.3, 0.8, 0.5, 0, 0, 0, 0, 0][q] if lv.price_cap else 0.0
        trade = 0.0
        if lv.stance == "sanction" and t >= 2:
            trade += 0.25
        if lv.stance == "neutral" and t <= 6:
            trade -= 0.4 * export_sens
        if t <= 6:
            trade += lv.trade - 0.012 * max(tariff_t, 0.0)  # tariffs invite retaliation
        layoff_drag = [1.0, 0.8, 0.4, 0.1, 0, 0, 0, 0][q] if lv.company == "let_fail" else 0.0
        reform_boost = 0.2 if lv.company == "restructure" and t >= 4 else 0.0
        competitiveness = _clamp(0.03 * (100 - currency) * export_sens, -1.0, 1.5)
        reserve_crunch = 1.0 if reserves < 0.5 else 0.0  # can't pay for imports any more
        # The crisis itself: lost spending, scarce goods, emergency spending, and what you did about it
        crisis = (demand_t - 0.3 * supply_t + 0.3 * fiscal_t - lv.drag_now * FADE[q]
                  + (0.4 * lv.confidence if t <= 4 else 0.0) + (0.15 * lv.credit if t >= 2 else 0.0))
        gap = _clamp(
            0.55 * gap + stimulus + fiscal - rate_drag - supply_drag - strike_drag - shortage_drag
            + trade - layoff_drag + reform_boost + competitiveness - reserve_crunch + crisis,
            -9.0, 6.0,
        )

        # ---- Inflation: break it into its causes (the report shows this breakdown)
        demand_pull = 0.35 * gap
        fuel_push = oil_t * fuel_dep * 0.10 * (1 - subsidy_cover)
        if t == 5 and lv.fuel_subsidy:
            fuel_push += oil[3] * oil_mult * fuel_dep * 0.06 * lv.fuel_subsidy  # subsidy ends: catch-up
        food_mult = 0.75 if lv.tariff_cut else 1.0
        if lv.price_cap:
            food_mult *= [0.3, 0.3, 1.6, 1.4, 1.0, 1.0, 1.0, 1.0][q]
        food_push = grain_t * (0.3 + food_dep * 0.5) * 0.12 * food_mult
        yoy_depreciation = max(0.0, (currency_year_ago[0] - currency) / currency_year_ago[0] * 100)
        import_push = 0.3 * (1 - 0.5 * cred) * import_share * yoy_depreciation
        money_push = 4 * lv.print_pct * 1.5 * (1.3 - cred) * PRINT_WEIGHTS[q]
        # When people can't spend (lockdown) or banks won't lend, new money mostly sits in bank accounts
        money_push *= _clamp(1 + 0.1 * demand_t + 0.06 * credit_t, 0.25, 1.0)
        supply_push = supply_t + lv.supply_push * EASE[q] + 0.04 * tariff_t * import_share
        wage_push = max(0.0, lv.wage_push - pi0) * 0.25 * [0.4, 0.6, 0.5, 0.3, 0.2, 0.1, 0, 0][q]
        if lv.wage_push >= 15 and pi_prev > pi0 + 4:
            wage_push += 0.15 * (pi_prev - pi0)  # indexation: the wage-price spiral
        causes = {
            "expectations": expected,
            "demand": demand_pull,
            "fuel": fuel_push,
            "food": food_push,
            "currency": import_push,
            "printing": money_push,
            "wages": wage_push,
            "supply": supply_push,
        }
        inflation = _clamp(sum(causes.values()), -3.0, 400.0)

        # ---- Unemployment
        # Wage schemes keep people on the payroll while spending is down
        protect = 1 - 0.6 * _clamp(lv.job_protect, 0, 1) if gap < 0 and t <= 4 else 1.0
        unemployment = _clamp(
            u0 - 0.45 * gap * protect + layoffs_t
            + ([0.6, 0.5, 0.3, 0.1, 0, 0, 0, 0][q] if lv.company == "let_fail" else 0.0),
            1.5, 45.0,
        )

        # ---- Money: banks create most of it by lending; printing adds central-bank money
        credit_growth = (pi0 + 2.5) - 2.5 * (policy_rate - i0) * RATE_RAMP[q] + 1.5 * gap + credit_t
        credit_growth += 2 * lv.credit if t >= 2 else 0.0
        bank_money *= 1 + max(-10.0, credit_growth) / 400
        cb_money *= 1 + (pi0 + 2.5) / 400
        cb_money += lv.print_pct / 0.6 * PRINT_WEIGHTS[q]  # money stock is ~60% of GDP

        # ---- Currency
        world_inflation = 3.0 + oil[q] * 0.05 + grain_t * 0.02
        d_currency = (
            0.3 * (policy_rate - i0)
            - 0.8 * (inflation - world_inflation) / 4
            - risk_t * (1 - cred)
            - (0.8 if lv.stance == "neutral" and t <= 4 else 0.0)
            + 1.2 * lv.fx_support * FADE[q]
            - 0.5 * lv.print_pct * PRINT_WEIGHTS[q]
            + ([1.5, 1.0, 0, 0, 0, 0, 0, 0][q] if lv.un_package else 0.0)
            - 0.04 * oil_t * fuel_dep
            - (6.0 if reserves < 0.5 else 0.0)
        )
        d_currency = _clamp(d_currency, -30.0, 10.0)
        currency = _clamp(currency * (1 + d_currency / 100), 3.0, 180.0)
        currency_year_ago = currency_year_ago[1:] + [currency]

        # ---- Reserves (months of imports the central bank could pay for)
        reserves += (
            0.15
            - 0.012 * oil_t * fuel_dep
            - 0.006 * grain_t * food_dep * (1.2 if lv.tariff_cut else 1.0)
            - (0.1 * abs(d_currency) if d_currency < -3 and reserves > 0 and not lv.capital_controls else 0.0)
            + (0.05 * max(0.0, competitiveness))
        )
        reserves = max(0.0, reserves)

        # ---- Government debt (% of GDP)
        deficit = (
            (lv.fuel_subsidy * oil_t * fuel_dep * 0.025 if subsidy_on else 0.0)
            + (lv.fiscal / 2 if t <= 4 else 0.0)
            + (0.15 if lv.food_stamps and t <= 4 else 0.0)
            + lv.green_invest / 4
            + fiscal_t
            - (0.25 * lv.austerity if t >= 2 else 0.0)
            - 0.15 * gap
        )
        debt += deficit - debt * (inflation / 400) * 0.5 + foreign_debt_share * debt * (-d_currency / 100)
        debt = max(0.0, debt)

        # ---- The island's big company
        if t == 1:
            company -= 12  # the crisis it walked in with
            company += {"bailout": 25, "restructure": 12, "let_fail": -30}.get(lv.company, 0)
            if lv.wage_push >= 15:
                company -= 4
            if lv.strike:
                company -= 6
            if island["company"]["sector"] == "finance" and lv.stance == "sanction":
                company -= 8  # loans to Petra frozen
            company -= 1.0 * (policy_rate - i0)
        company += 0.8 * gap
        if island["company"]["sector"] != "finance":
            company -= 0.05 * oil_t * fuel_dep
            company += _clamp(0.1 * (100 - currency) * export_sens, -2, 3)
        company += {"bailout": -1.0, "restructure": 2.0 if t >= 3 else 0.0, "let_fail": 3.0}.get(lv.company, 0.0)
        company = _clamp(company, 0, 100)

        # ---- Environment
        if lv.green_invest and t >= 3:
            env += 2.0 * lv.green_invest / 1.5
        if subsidy_on and lv.fuel_subsidy:
            env -= 0.6 * lv.fuel_subsidy
        env = _clamp(env, 0, 100)

        # ---- Approval: the day's cheers fade, while prices and jobs are felt every week
        approval_target = (
            approval_base
            - 1.6 * max(inflation - pi0, 0)
            - 2.2 * max(unemployment - u0, 0)
            + 0.8 * min(gap, 2)
            - (6 if lv.price_cap and t in (2, 3) else 0)
            - (4 if lv.strike and t == 1 else 0)
            + (3 if t == end else 0)
        )
        approval = _clamp(0.65 * approval + 0.35 * approval_target, 0, 100)

        # ---- Prices, wages, savings
        price_level *= 1 + inflation / 400
        wage_growth = 0.6 * pi_prev + 0.4 * pi0
        wage_level *= 1 + wage_growth / 400
        if t == 1:
            wage_level *= 1 + 0.6 * lv.wage_push / 100
        real_wage = wage_level / price_level * 100
        deposit_rate = max(0.0, policy_rate - 1.0)
        real_savings *= 1 + (deposit_rate - inflation) / 400
        loan_rate = policy_rate + 3
        farmer_debt_real *= 1 + (loan_rate - inflation) / 400

        fuel_price_pct = oil_t * (1 - subsidy_cover) * 0.6
        basket = {
            "bread": BASKET[0]["base"] * price_level / 100 * (1 + grain_t * food_mult / 200),
            "fuel": BASKET[1]["base"] * price_level / 100 * (1 + fuel_price_pct / 100),
            "rent": BASKET[2]["base"] * price_level / 100,
            "phone": BASKET[3]["base"] * price_level / 100 * (100 / currency) ** 0.6,
        }

        sustainability = sustainability_index(env, debt, reserves, company, unemployment, inflation, target, cred)

        citizens = {
            "saver": _clamp(50 + (real_savings - 100) * 2.5, 0, 100),
            "driver": _clamp(55 - fuel_price_pct * 0.5 + (real_wage - 100) * 1.5 - max(0, unemployment - u0) * 2, 0, 100),
            "farmer": _clamp(
                50 + grain_t * (0.3 if not lv.price_cap else -0.2) + (100 - farmer_debt_real) * 1.2
                - (8 if lv.tariff_cut else 0) - 1.5 * (policy_rate - i0) - oil_t * 0.08, 0, 100),
            "shop": _clamp(55 + 3 * gap - (25 if lv.price_cap and t <= 3 else 0)
                           - max(0, 100 - currency) * 0.4, 0, 100),
            "worker": _clamp(25 + company * 0.4 + (real_wage - 100) * 1.5 - max(0, unemployment - u0) * 2.5, 0, 100),
        }

        timeline.append({
            "quarter": t,
            "months": t * 3,
            "active": active,
            "ended_now": t == end,
            "oil_shock": round(oil_t, 1),
            "grain_shock": round(grain_t, 1),
            "inflation": round(inflation, 2),
            "inflation_causes": {k: round(v, 2) for k, v in causes.items()},
            "unemployment": round(unemployment, 2),
            "output_gap": round(gap, 2),
            "interest_rate": round(policy_rate, 2),
            "currency_index": round(currency, 1),
            "reserves_months": round(reserves, 2),
            "debt_to_gdp": round(debt, 1),
            "approval": round(approval, 1),
            "sustainability": round(sustainability, 1),
            "environment": round(env, 1),
            "company_health": round(company, 1),
            "credibility": round(cred, 3),
            "money": {"bank": round(bank_money, 1), "central": round(cb_money, 1)},
            "price_level": round(price_level, 2),
            "real_wage": round(real_wage, 1),
            "real_savings": round(real_savings, 1),
            "basket": {k: round(v, 2) for k, v in basket.items()},
            "citizens": {k: round(v, 1) for k, v in citizens.items()},
        })
        pi_prev = inflation

    return {
        "target_inflation": target,
        "end_quarter": end,
        "start": {
            **s,
            "sustainability": start_sustainability(island),
            "approval_after_day": round(_clamp(s["approval"] + lv.today["approval"], 0, 100), 1),
            "company_health": island["company"]["health"],
            "basket": {b["id"]: b["base"] for b in BASKET},
            "money": {"bank": 85.0, "central": 15.0},
        },
        "timeline": timeline,
    }


def summarize(island: dict, sim: dict) -> dict:
    tl = sim["timeline"]
    s = sim["start"]
    last = tl[-1]
    return {
        "peak_inflation": max(q["inflation"] for q in tl),
        "end_inflation": last["inflation"],
        "avg_unemployment": sum(q["unemployment"] for q in tl) / len(tl),
        "peak_unemployment": max(q["unemployment"] for q in tl),
        "currency_change": last["currency_index"] - s["currency_index"],
        "debt_change": last["debt_to_gdp"] - s["debt_to_gdp"],
        "reserves_end": last["reserves_months"],
        "approval_end": last["approval"],
        "sustainability_end": last["sustainability"],
        "company_end": last["company_health"],
        "price_rise": last["price_level"] - 100,
    }


IMPACT_KEYS = [
    ("peak_inflation", "Peak inflation", "pts", -1),
    ("avg_unemployment", "Unemployment", "pts", -1),
    ("currency_change", "Currency", "pts", 1),
    ("debt_change", "Debt", "% GDP", -1),
    ("reserves_end", "Reserves", "months", 1),
    ("approval_end", "Approval", "pts", 1),
    ("sustainability_end", "Sustainability", "pts", 1),
]


def _impact(base: dict, alt: dict) -> list[dict]:
    """Difference between two runs, as signed chips. `good` tells the UI which way is better."""
    out = []
    for key, label, unit, better in IMPACT_KEYS:
        delta = base[key] - alt[key]
        if abs(delta) < 0.15:
            continue
        out.append({"key": key, "label": label, "unit": unit, "delta": round(delta, 1), "good": delta * better > 0})
    return out


def _score(island: dict, summary: dict, target: float) -> int:
    s = {**island["start"], "sustainability": start_sustainability(island)}
    infl = _clamp(100 - 6 * max(0, summary["peak_inflation"] - target) - 8 * max(0, summary["end_inflation"] - target), 0, 100)
    jobs = _clamp(100 - 12 * max(0, summary["avg_unemployment"] - s["unemployment"]), 0, 100)
    fx = _clamp(100 + 2 * min(0, summary["currency_change"]), 0, 100)
    sust = _clamp(50 + 3 * (summary["sustainability_end"] - s["sustainability"]), 0, 100)
    appr = _clamp(summary["approval_end"] * 1.5, 0, 100)
    return int(round(2.5 * infl + 2.0 * jobs + 1.5 * fx + 2.0 * sust + 2.0 * appr))


def _ending(chosen: dict[str, str], options: list[dict], summary: dict, island: dict, target: float) -> dict:
    s = {**island["start"], "sustainability": start_sustainability(island)}
    printed = any(o.get("levers", {}).get("print_pct", 0) > 0 for o in options)
    if summary["peak_inflation"] > 40:
        return {"title": "The Printing Press",
                "text": "Prices ran away from you. Once people stop trusting money, they spend it as fast as they "
                        "can, and that makes prices rise even faster."}
    if summary["reserves_end"] < 0.5:
        return {"title": "Running on Empty",
                "text": f"{island['name']} ran out of foreign savings. With no reserves left, nobody would sell it "
                        "fuel on credit and the currency had nothing behind it."}
    if printed and summary["approval_end"] < s["approval"]:
        return {"title": "The Crowd Pleaser",
                "text": "The cheers were loud on day one and gone by year two. Free money felt like a gift, but it "
                        "was paid for with higher prices."}
    if chosen.get("rates") == "hike_big" and summary["avg_unemployment"] - s["unemployment"] > 1.5:
        return {"title": "The Iron Governor",
                "text": "You broke inflation's back and some jobs with it. History may thank you; this year's "
                        "voters won't."}
    if summary["sustainability_end"] - s["sustainability"] >= 3:
        return {"title": "The Architect",
                "text": "You used the crisis to build something. The island is stronger now than when the crisis "
                        "began."}
    if summary["peak_inflation"] <= target + 4 and summary["approval_end"] >= s["approval"] - 3:
        return {"title": "The Steady Hand",
                "text": "No miracles and no disasters. You took the shock, kept trust, and the island came "
                        "through."}
    return {"title": "The Survivor",
            "text": "You got through it, with some scars. The crisis hit hard, and some of your choices made it "
                    "hurt more than it had to."}


CITIZEN_QUOTES = {
    "saver": ["My savings melted. Forty years of work, and it buys half what it did.",
              "I'm a bit poorer, but my savings held up better than I feared.",
              "My savings kept their value. In a crisis, that's everything."],
    "driver": ["I spend more on fuel than I take home. I'm thinking of selling the car.",
               "It's tight. Every fare goes straight into the tank.",
               "Fuel's settled down, and so has my stomach."],
    "farmer": ["The bank is squeezing me and costs are crushing me. I may lose the farm.",
               "Some good seasons, some bad. The loan is still there.",
               "Good prices for my crops, and the loan feels smaller every year."],
    "shop": ["Half my shelves are empty and customers think I'm a thief.",
             "Customers buy less and complain more, but I'm open.",
             "Business is steady. People are spending again."],
    "worker": ["The company let me go. Nobody's hiring.",
               "I kept my job, but my pay buys less every month.",
               "Job's safe and my pay is keeping up. Can't complain."],
}


def build_report(island: dict, scenario: dict, decisions: list[tuple[str, str]]) -> dict:
    """Full end-of-term report: timeline, consequence map, what-ifs, citizens and ending."""
    cards = get_cards(island, scenario)
    by_id = {c["id"]: c for c in cards}
    chosen = dict(decisions)
    options = [next(o for o in by_id[cid]["options"] if o["id"] == oid) for cid, oid in decisions]

    sim = simulate(island, options, scenario)
    summary = summarize(island, sim)
    target = sim["target_inflation"]

    consequence_map = []
    for idx, (cid, oid) in enumerate(decisions):
        card = by_id[cid]
        option = options[idx]
        base_opt = baseline_option(card)

        def run_with(alt_opt: dict) -> dict:
            swapped = options[:idx] + [alt_opt] + options[idx + 1:]
            return summarize(island, simulate(island, swapped, scenario))

        entry = {
            "card_id": cid,
            "time": card["time"],
            "card_title": card["title"],
            "option_id": oid,
            "option_title": option["title"],
            "icon": option["icon"],
            "chain": option["chain"],
            "history": option["history"],
            "today": option["today"],
            "was_baseline": bool(option.get("baseline")),
        }
        if not option.get("baseline"):
            entry["impact"] = _impact(summary, run_with(base_opt))
            entry["compared_to"] = base_opt["title"]
        else:
            entry["impact"] = []
        # The most dramatic road not taken
        best = None
        for alt in card["options"]:
            if alt["id"] == oid:
                continue
            alt_summary = run_with(alt)
            swing = abs(alt_summary["peak_inflation"] - summary["peak_inflation"]) + abs(
                alt_summary["avg_unemployment"] - summary["avg_unemployment"]) + abs(
                alt_summary["approval_end"] - summary["approval_end"]) / 5
            if best is None or swing > best[0]:
                best = (swing, alt, alt_summary)
        if best:
            _, alt, alt_summary = best
            entry["what_if"] = {
                "option_title": alt["title"],
                "icon": alt["icon"],
                "impact": _impact(alt_summary, summary),
            }
        consequence_map.append(entry)

    # Where did inflation come from at its peak?
    peak_q = max(sim["timeline"], key=lambda q: q["inflation"])

    citizens = []
    for c in CITIZENS:
        final = sim["timeline"][-1]["citizens"][c["id"]]
        band = 0 if final < 38 else (1 if final < 62 else 2)
        citizens.append({**c, "wellbeing": final, "quote": CITIZEN_QUOTES[c["id"]][band],
                         "series": [q["citizens"][c["id"]] for q in sim["timeline"]]})

    ending = _ending(chosen, options, summary, island, target)
    return {
        "scenario": public_scenario(scenario, island),
        "island": {k: island[k] for k in ("id", "name", "tier", "tier_label", "currency", "currency_code", "company", "art")},
        "simulation": sim,
        "summary": {k: round(v, 2) for k, v in summary.items()},
        "score": _score(island, summary, target),
        "ending": ending,
        "peak": {"quarter": peak_q["quarter"], "inflation": peak_q["inflation"], "causes": peak_q["inflation_causes"]},
        "consequence_map": consequence_map,
        "citizens": citizens,
        "headlines": headlines(island, scenario, sim, options),
    }


def headlines(island: dict, scenario: dict, sim: dict, options: list[dict]) -> list[dict]:
    """One to three newspaper headlines per quarter, generated from what happened.

    Every quarter carries a story about the crisis itself (how it unfolds, then the recovery), plus the
    biggest moves in prices, jobs, the currency and the Governor's standing, and the fallout of the
    player's own choices.
    """
    name = island["name"]
    cur = island["currency"]
    news = scenario["news"]
    during = [fmt(text, island) for text in news["during"]]
    after = [fmt(text, island) for text in news["after"]]
    ended = fmt(news["end"], island)
    end = sim["end_quarter"]
    from_choices: dict[int, list[tuple[str, str]]] = {}
    for opt in options:
        for q, tone, text in opt.get("news", []):
            from_choices.setdefault(q, []).append((tone, text))

    out: list[dict] = []
    prev = {"inflation": island["start"]["inflation"], "currency_index": island["start"]["currency_index"],
            "unemployment": island["start"]["unemployment"], "reserves_months": island["start"]["reserves_months"],
            "approval": sim["start"]["approval_after_day"], "debt_to_gdp": island["start"]["debt_to_gdp"]}
    for q in sim["timeline"]:
        t = q["quarter"]
        story = None
        if q["active"]:
            story = ("bad", during[min(t, len(during)) - 1])
        elif t > end and t - end - 1 < len(after):
            story = ("neutral", after[t - end - 1])

        items: list[tuple[str, str]] = []  # (tone, text), most important first
        if q["ended_now"]:
            items.append(("good", ended))
        d_infl = q["inflation"] - prev["inflation"]
        if q["inflation"] >= 40:
            items.append(("bad", f"Prices doubling fast: shops change price tags twice a day ({q['inflation']:.0f}% inflation)"))
        elif d_infl >= 2:
            items.append(("bad", f"Inflation jumps to {q['inflation']:.1f}%: highest in years"))
        elif d_infl >= 0.6:
            items.append(("bad", f"Prices creep up: inflation reaches {q['inflation']:.1f}%"))
        elif d_infl <= -1.5:
            items.append(("good", f"Prices cooling: inflation eases to {q['inflation']:.1f}%"))
        elif d_infl <= -0.6:
            items.append(("good", f"Shoppers get some relief: inflation slows to {q['inflation']:.1f}%"))
        if q["reserves_months"] < 0.5 <= prev["reserves_months"]:
            items.append(("bad", f"{name} RUNS OUT OF DUCATS: fuel ships turned away"))
        d_jobs = q["unemployment"] - prev["unemployment"]
        if d_jobs >= 1:
            items.append(("bad", f"Jobless rate climbs to {q['unemployment']:.1f}%"))
        elif d_jobs >= 0.4:
            items.append(("bad", f"More layoffs: unemployment edges up to {q['unemployment']:.1f}%"))
        elif d_jobs <= -0.5:
            items.append(("good", f"Hiring picks up: unemployment falls to {q['unemployment']:.1f}%"))
        d_cur = (q["currency_index"] - prev["currency_index"]) / prev["currency_index"] * 100
        if d_cur <= -5:
            items.append(("bad", f"{cur} tumbles {abs(d_cur):.0f}% as investors flee"))
        elif d_cur <= -2:
            items.append(("bad", f"{cur} slips {abs(d_cur):.0f}%: imports get dearer"))
        elif d_cur >= 3:
            items.append(("good", f"{cur} strengthens: imports get cheaper"))
        elif d_cur >= 1.5:
            items.append(("good", f"{cur} edges up as nerves calm"))
        items.extend(from_choices.get(t, []))
        if q["debt_to_gdp"] - prev["debt_to_gdp"] >= 3:
            items.append(("bad", f"Government debt climbs to {q['debt_to_gdp']:.0f}% of the economy"))
        d_appr = q["approval"] - prev["approval"]
        if q["approval"] < 30 and t in (4, 8):
            items.append(("bad", "Protesters gather outside the Town Hall"))
        elif d_appr <= -4:
            items.append(("bad", f"Poll: Governor's approval slides to {q['approval']:.0f}%"))
        elif d_appr >= 4:
            items.append(("good", f"Poll: Governor's approval rises to {q['approval']:.0f}%"))

        # The crisis story always makes the front page; the rest compete for the other slots.
        if story:
            items = [story] + items[:2] if t == 1 else items[:2] + [story]
        if not items:
            items.append(("neutral", f"Steady quarter: inflation {q['inflation']:.1f}%, unemployment {q['unemployment']:.1f}%"))
        out.append({"quarter": t, "items": [{"tone": tone, "text": text} for tone, text in items[:3]]})
        prev = q
    return out
