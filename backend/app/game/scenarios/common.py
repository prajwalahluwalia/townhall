"""Building blocks shared by every scenario.

Each option carries:
  today    - what happens right away (crowd reaction, markets, treasury). Shown immediately.
  levers   - what it changes inside the economy. Only shows up later, when the
             simulation fast-forwards. See `engine.Levers` for the full list.
  chain    - the cause-and-effect story for the consequence map, in plain words.
  history  - a real-world example of the same choice.
  news     - optional [quarter, tone, headline] items for the fast-forward newspaper.
One option per card is marked `baseline` (roughly "do nothing / middle road"). The
report measures every decision against that baseline.
"""

from copy import deepcopy


def fmt(text: str, island: dict) -> str:
    return text.format(
        island=island["name"],
        company=island["company"]["name"],
        crisis=island["company"]["crisis"],
        currency=island["currency"],
        workers=island["company"]["workers"],
    )


def finalize(cards: list[dict], island: dict) -> list[dict]:
    """Fill the island's names into every piece of text on the cards."""
    for card in cards:
        card["title"] = fmt(card["title"], island)
        card["situation"] = fmt(card["situation"], island)
        for option in card["options"]:
            option["title"] = fmt(option["title"], island)
            option["summary"] = fmt(option["summary"], island)
            option["chain"] = [fmt(step, island) for step in option["chain"]]
            option["news"] = [[q, tone, fmt(text, island)] for q, tone, text in option.get("news", [])]
    return cards


def finance_option(island: dict) -> dict:
    """Emergency money from abroad: a UN/IMF package for islands that qualify, foreign bonds otherwise."""
    if island["un_eligible"]:
        return {
            "id": "un_package",
            "title": "Accept the UN / IMF rescue package",
            "icon": "🇺🇳",
            "summary": "You get emergency ducats and expert help. In return you must cut spending and raise rates.",
            "today": {"approval": -5, "reserves": 4.0, "debt": 3.0, "currency": 4.0, "crowd": "mixed",
                      "quote": "\"Foreigners are telling us how to run our home now?\""},
            "levers": {"un_package": True, "austerity": 0.6, "rate_change": 1.0, "credibility": 0.15},
            "chain": [
                "You accepted the rescue package",
                "Ducats arrived and the central bank's reserves were refilled",
                "Investors stopped fearing a collapse, so the currency steadied",
                "The conditions meant spending cuts and higher rates, so growth slowed",
            ],
            "history": "Sri Lanka (2023) and Ghana (2023) took IMF programmes after their currencies crashed.",
            "news": [[1, "good", "UN and IMF funds land, and the currency steadies"]],
        }
    return {
        "id": "bonds",
        "title": "Borrow abroad to rebuild reserves",
        "icon": "📜",
        "summary": "Sell bonds to foreign investors. You get cash now and owe it in foreign money later.",
        "today": {"approval": 1, "reserves": 2.5, "debt": 4.0, "currency": 1.5, "crowd": "mixed",
                  "quote": "\"More debt? Fine, as long as someone else pays it back.\""},
        "levers": {"foreign_borrow": 4.0},
        "chain": [
            "You borrowed from foreign investors",
            "Reserves grew, so you had more firepower to defend the currency",
            "But the debt is owed in foreign money",
            "If your currency falls, that debt grows in local terms",
        ],
        "history": "Many emerging economies borrowed in dollars in the 1990s. When their currencies fell in 1997, the debt doubled.",
    }


_RATES_OPTIONS = [
    {
        "id": "hike_big",
        "title": "Raise rates sharply (+3%)",
        "icon": "⏫",
        "summary": "Show the world you'll fight inflation whatever it costs. Loans and mortgages get expensive.",
        "today": {"approval": -8, "reserves": 0.3, "debt": 0.0, "currency": 4.0, "crowd": "boo",
                  "quote": "\"My mortgage just went up by a third!\""},
        "levers": {"rate_change": 3.0, "credibility": 0.1},
        "chain": [
            "You raised interest rates sharply",
            "Borrowing got expensive, so banks lent less and less new money was created",
            "Foreign savers wanted higher returns, so the {currency} rose and imports got cheaper",
            "Businesses cut back and some people lost jobs",
            "Over time, inflation came down",
        ],
        "history": "In 1980, Paul Volcker raised US rates to 20%. Inflation fell from 14% to 3%, but at the cost of a deep recession.",
    },
    {
        "id": "hike_small",
        "title": "Nudge rates up (+1%)",
        "icon": "🔼",
        "summary": "A cautious step. You signal concern without slamming on the brakes.",
        "today": {"approval": -2, "reserves": 0.1, "debt": 0.0, "currency": 1.2, "crowd": "mixed",
                  "quote": "\"Bit more on the loan. We'll manage.\""},
        "levers": {"rate_change": 1.0, "credibility": 0.03},
        "chain": [
            "You raised rates a little",
            "Lending slowed slightly",
            "The currency got a small boost",
            "It was a gentle brake on inflation, with little damage to jobs",
        ],
        "history": "Most central banks move in small 0.25–0.5% steps so they don't shock the economy.",
    },
    {
        "id": "hold",
        "title": "Hold steady",
        "icon": "⏸️",
        "summary": "Nobody knows yet how deep this goes, so you wait and watch.",
        "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": -0.5, "crowd": "mixed",
                  "quote": "\"Nothing changed? OK.\""},
        "levers": {},
        "baseline": True,
        "chain": [
            "You kept rates where they were",
            "Borrowing and lending carried on as before",
            "Whether inflation spread depended on whether people expected it to",
        ],
        "history": "In 2021, many central banks called inflation 'transitory' and waited. Some waited too long.",
    },
    {
        "id": "cut",
        "title": "Cut rates (−1%) to protect jobs",
        "icon": "🔽",
        "summary": "Make loans cheaper so businesses survive the shock. Easy money means more money.",
        "today": {"approval": 5, "reserves": -0.3, "debt": 0.0, "currency": -2.5, "crowd": "cheer",
                  "quote": "\"Cheaper loans! Time to expand the shop.\""},
        "levers": {"rate_change": -1.0, "credibility": -0.06},
        "chain": [
            "You cut interest rates",
            "Cheap loans meant banks lent more, and every new loan creates new money",
            "Businesses found it easier to keep going and keep staff",
            "The {currency} weakened because foreign savers left for higher returns elsewhere",
        ],
        "history": "In 2008 and 2020, central banks slashed rates to keep firms alive while spending collapsed.",
    },
]


def rates_card(time: str, situation: str, overrides: dict[str, dict] | None = None) -> dict:
    """The interest-rate meeting. Every crisis has one, but the right answer depends on the crisis."""
    options = deepcopy(_RATES_OPTIONS)
    for option in options:
        option.update((overrides or {}).get(option["id"], {}))
    return {
        "id": "rates",
        "time": time,
        "speaker": "Deputy Governor",
        "speaker_icon": "banker",
        "title": "The interest rate meeting",
        "situation": (
            situation + " The interest rate is what banks charge for loans. A higher rate means fewer loans, less "
            "new money created and less spending. A lower rate means more of all three. What rate do you set?"
        ),
        "options": options,
    }


def company_card(island: dict, time: str) -> dict:
    """The island's biggest employer is in trouble. What the trouble is depends on the scenario."""
    name = island["company"]["name"]
    return {
        "id": "company",
        "time": time,
        "speaker": f"CEO, {name}",
        "speaker_icon": "ceo",
        "title": f"{name} is in trouble",
        "situation": (
            "{company}, the island's biggest employer with {workers} workers, {crisis}. "
            "Its CEO is in your office saying the company will collapse within weeks without help."
        ),
        "options": [
            {
                "id": "bailout",
                "title": "Bail it out with new money",
                "icon": "🖨️",
                "summary": "The central bank creates money and buys the company's bad debts. Every job is saved, today.",
                "today": {"approval": 5, "reserves": 0.0, "debt": 0.0, "currency": -2.0, "crowd": "cheer",
                          "quote": "\"My job is safe! My dad's job is safe!\""},
                "levers": {"print_pct": 2.5, "company": "bailout", "credibility": -0.07},
                "chain": [
                    "You printed money to save {company}",
                    "Every job was saved immediately",
                    "The new money added to inflation and weakened the {currency}",
                    "The company learned it would always be rescued, so it didn't reform",
                ],
                "history": "Japan kept 'zombie' companies alive in the 1990s. That contributed to its 'lost decade'.",
            },
            {
                "id": "restructure",
                "title": "Rescue loan with conditions",
                "icon": "🛠️",
                "summary": "A government loan, but management must modernise, cut waste and pay it back.",
                "today": {"approval": 1, "reserves": 0.0, "debt": 1.2, "currency": 0.0, "crowd": "mixed",
                          "quote": "\"Some changes coming at work, but we're still open.\""},
                "levers": {"company": "restructure", "fiscal": 0.25},
                "chain": [
                    "You lent to {company} with strings attached",
                    "There was some short-term pain as the company restructured",
                    "It became more efficient and competitive",
                    "Taxpayers eventually got their money back",
                ],
                "history": "The US auto bailout in 2009 came with restructuring. GM and Chrysler repaid most of the money.",
                "news": [[4, "good", "Leaner {company} returns to profit"]],
            },
            {
                "id": "let_fail",
                "title": "Let the market decide",
                "icon": "📉",
                "summary": "No rescue. If it fails, its workers and assets will go somewhere more productive.",
                "today": {"approval": -8, "reserves": 0.0, "debt": 0.0, "currency": 0.5, "crowd": "boo",
                          "quote": "\"Twenty years I worked there. Twenty years.\""},
                "levers": {"company": "let_fail"},
                "baseline": True,
                "chain": [
                    "You let {company} sink or swim alone",
                    "Mass layoffs followed and unemployment jumped",
                    "Spending fell in the towns that depended on it",
                    "The budget and the currency were spared",
                ],
                "history": "Lehman Brothers was allowed to fail in 2008. Markets panicked, but no bailout precedent was set.",
                "news": [[1, "bad", "{company} announces mass layoffs"]],
            },
        ],
    }


def future_card(island: dict, time: str, situation: str) -> dict:
    """The last visitor of the day: how to prepare for the next shock."""
    return {
        "id": "future",
        "time": time,
        "speaker": "Planning Minister" if not island["un_eligible"] else "UN Envoy",
        "speaker_icon": "planner" if not island["un_eligible"] else "envoy",
        "title": "The long game",
        "situation": situation,
        "options": [
            {
                "id": "green",
                "title": "Launch a renewable energy programme",
                "icon": "☀️",
                "summary": "Spend now on solar, wind and storage, so the island needs less imported fuel in the future.",
                "today": {"approval": 3, "reserves": -0.3, "debt": 2.0, "currency": 0.0, "crowd": "cheer",
                          "quote": "\"My kids will thank you. My wallet, maybe not this year.\""},
                "levers": {"green_invest": 1.5},
                "chain": [
                    "You invested in home-grown renewable energy",
                    "It cost money upfront and added to the debt",
                    "After about a year, the island needed less imported fuel",
                    "The next oil shock hits {island} far less hard",
                ],
                "history": "Denmark built its wind industry after the 1973 oil shock and became an energy exporter.",
                "news": [[5, "good", "First solar farm switches on: {island} imports less fuel"]],
            },
            finance_option(island),
            {
                "id": "austerity",
                "title": "Tighten the belt",
                "icon": "✂️",
                "summary": "Cut government spending to pay down debt and rebuild savings.",
                "today": {"approval": -7, "reserves": 0.8, "debt": -2.0, "currency": 1.0, "crowd": "boo",
                          "quote": "\"They cut the bus route to my school. Again.\""},
                "levers": {"austerity": 1.0},
                "chain": [
                    "You cut government spending",
                    "There was less money moving around, so demand cooled",
                    "Inflation eased a little, but jobs were lost",
                    "The debt grew more slowly",
                ],
                "history": "Greece (2010–2015) made deep cuts. The debt was brought under control, but unemployment hit 27%.",
            },
            {
                "id": "postpone",
                "title": "Postpone it",
                "icon": "⏳",
                "summary": "Deal with the long term next year. Today has been long enough.",
                "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                          "quote": "\"Same as every government before.\""},
                "levers": {},
                "baseline": True,
                "chain": [
                    "You put off long-term planning",
                    "Nothing changed: same fuel dependence, same savings",
                    "{island} stays just as exposed to the next crisis",
                ],
                "history": "Most governments make this choice, which is why the same crises keep coming back.",
            },
        ],
    }
