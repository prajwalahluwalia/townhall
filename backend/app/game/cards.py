"""Decision cards for the 'Strait Crisis' scenario: your first day in office.

Each option carries three things:
  today    - what happens right away (crowd reaction, markets, treasury). Shown immediately.
  levers   - what it changes inside the economy. Only shows up later, when the
             simulation fast-forwards.
  chain    - the cause-and-effect story for the consequence map, in plain words.
One option per card is marked `baseline` (roughly "do nothing / middle road"). The
report measures every decision against that baseline.
"""

SCENARIO_ID = "strait_crisis"

SCENARIO = {
    "id": SCENARIO_ID,
    "title": "The Strait Crisis",
    "intro": (
        "At dawn on your first day as Governor, Petra and Granara go to war. The Strait of Teeth, "
        "which carries the world's oil and grain, is closed. Every decision you make today will "
        "echo through the next two years."
    ),
    "quarters": 8,
}


def _fmt(text: str, island: dict) -> str:
    return text.format(
        island=island["name"],
        company=island["company"]["name"],
        crisis=island["company"]["crisis"],
        currency=island["currency"],
        workers=island["company"]["workers"],
    )


def _future_card(island: dict) -> dict:
    finance_option = (
        {
            "id": "un_package",
            "title": "Accept the UN / IMF rescue package",
            "icon": "🇺🇳",
            "summary": "You get emergency dollars and expert help. In return you must cut spending and raise rates.",
            "today": {"approval": -5, "reserves": 4.0, "debt": 3.0, "currency": 4.0, "crowd": "mixed",
                      "quote": "\"Foreigners are telling us how to run our home now?\""},
            "levers": {"un_package": True, "austerity": 0.6, "rate_change": 1.0, "credibility": 0.15},
            "chain": [
                "You accepted the rescue package",
                "Dollars arrived and the central bank's reserves were refilled",
                "Investors stopped fearing a collapse, so the currency steadied",
                "The conditions meant spending cuts and higher rates, so growth slowed",
            ],
            "history": "Sri Lanka (2023) and Ghana (2023) took IMF programmes after their currencies crashed.",
        }
        if island["un_eligible"]
        else {
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
    )
    return {
        "id": "future",
        "time": "20:00",
        "speaker": "Planning Minister" if not island["un_eligible"] else "UN Envoy",
        "speaker_icon": "planner" if not island["un_eligible"] else "envoy",
        "title": "The long game",
        "situation": _fmt(
            "The day is ending. The crisis will pass eventually, but {island} will still burn imported fuel "
            "and still have only a thin cushion of savings. How do you prepare {island} for the next shock?",
            island,
        ),
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
            },
            finance_option,
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


def get_cards(island: dict) -> list[dict]:
    cards = [
        {
            "id": "war",
            "time": "08:00",
            "speaker": "Foreign Minister",
            "speaker_icon": "diplomat",
            "title": "The Strait of Teeth is closed",
            "situation": _fmt(
                "Petra has invaded Granara's northern farmlands. Tankers and grain ships are stuck outside "
                "the strait. Aurum and Forge are demanding that everyone sanction Petra. Petra is offering "
                "cheap oil to anyone who stays neutral. What is {island}'s position?",
                island,
            ),
            "options": [
                {
                    "id": "sanction",
                    "title": "Join the sanctions on Petra",
                    "icon": "🚫",
                    "summary": "Stand with Aurum and Forge. No more Petran oil, so you'll pay much more for fuel from elsewhere.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 0.0, "currency": 1.5, "crowd": "cheer",
                              "quote": "\"For once we're on the right side of history!\""},
                    "levers": {"stance": "sanction", "credibility": 0.05},
                    "chain": [
                        "You cut off Petran oil",
                        "{island} had to buy fuel from distant suppliers at much higher prices",
                        "Transport, farming and factories all got more expensive",
                        "Aurum and Forge rewarded your loyalty with steadier trade and investment",
                    ],
                    "history": "In 2022, Europe cut Russian gas. Energy prices hit records, but its alliances held together.",
                },
                {
                    "id": "neutral",
                    "title": "Stay neutral, buy cheap Petran oil",
                    "icon": "⚖️",
                    "summary": "Keep the fuel flowing at a discount. Aurum and Forge won't be happy.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.0, "currency": -1.5, "crowd": "mixed",
                              "quote": "\"Cheap petrol is cheap petrol.\""},
                    "levers": {"stance": "neutral"},
                    "baseline": True,
                    "chain": [
                        "You kept buying discounted Petran oil",
                        "Fuel prices rose less than in other islands",
                        "Aurum and Forge quietly bought fewer of your exports",
                        "Investors saw you as riskier, so the currency came under pressure",
                    ],
                    "history": "India and Turkey bought discounted Russian oil in 2022 and softened the energy shock at home.",
                },
                {
                    "id": "mediate",
                    "title": "Offer to broker peace talks",
                    "icon": "🕊️",
                    "summary": "Host the two sides at {island}'s Town Hall. Whether they listen depends on how much the world trusts you.",
                    "today": {"approval": 4, "reserves": -0.1, "debt": 0.0, "currency": 0.5, "crowd": "cheer",
                              "quote": "\"Imagine, peace signed in our Town Hall!\""},
                    "levers": {"stance": "mediate"},
                    "chain": [
                        "You offered to host peace talks",
                        "How much it mattered depended on {island}'s standing in the world",
                        "Fuel and grain stayed expensive until the war ended",
                    ],
                    "history": "Small states such as Norway (the Oslo Accords) have brokered peace. Larger powers usually decide whether it works.",
                },
            ],
        },
        {
            "id": "fuel",
            "time": "10:00",
            "speaker": "Finance Minister",
            "speaker_icon": "finance",
            "title": "Riots at the petrol pumps",
            "situation": _fmt(
                "Petrol is up 40% overnight. Taxi drivers have blocked the main bridge, fishermen can't afford "
                "diesel, and the evening news is calling it a crisis. People want you to do something now.",
                island,
            ),
            "options": [
                {
                    "id": "subsidy",
                    "title": "Subsidise fuel",
                    "icon": "⛽",
                    "summary": "The government pays part of every litre. Prices at the pump stay low and the treasury takes the hit.",
                    "today": {"approval": 10, "reserves": -0.6, "debt": 1.5, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Finally, a government that listens!\""},
                    "levers": {"fuel_subsidy": 0.6},
                    "chain": [
                        "You paid part of every litre of fuel",
                        "Pump prices stayed low, so inflation looked calmer at first",
                        "The bill landed on the government's budget, so the debt grew",
                        "People kept using as much fuel as before, so imports and the bill stayed high",
                    ],
                    "history": "Egypt and Indonesia spent more on fuel subsidies than on health for years.",
                },
                {
                    "id": "targeted",
                    "title": "Let prices rise, protect the poorest",
                    "icon": "🎟️",
                    "summary": "Pump prices follow the market. Bus passes and diesel vouchers go to fishermen and low-income workers.",
                    "today": {"approval": -3, "reserves": -0.1, "debt": 0.4, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"I get a bus pass. My neighbour with the car is furious.\""},
                    "levers": {"fuel_subsidy": 0.15, "fiscal": 0.3},
                    "baseline": True,
                    "chain": [
                        "You let fuel prices rise but helped the poorest",
                        "High prices made people drive less and use less fuel",
                        "Inflation went up for a while, but the budget stayed under control",
                    ],
                    "history": "Iran's 2010 reform replaced fuel subsidies with cash transfers to households.",
                },
                {
                    "id": "print_cash",
                    "title": "Print money, give everyone cash",
                    "icon": "💵",
                    "summary": "The central bank creates new {currency}s and every adult gets a cheque this week.",
                    "today": {"approval": 15, "reserves": 0.0, "debt": 0.0, "currency": -4.0, "crowd": "cheer",
                              "quote": "\"Free money! Best Governor ever!\""},
                    "levers": {"print_pct": 4.0, "credibility": -0.12},
                    "chain": [
                        "You printed new money and handed it out",
                        "People had more cash, but there were no more goods to buy",
                        "Too much money chased too few goods, so shops raised prices",
                        "Foreigners trusted the {currency} less, so it fell and imports got even pricier",
                        "Savers saw the value of their savings shrink",
                    ],
                    "history": "Zimbabwe (2007) and Weimar Germany (1923) printed money to pay bills. Prices ended up doubling every day.",
                },
            ],
        },
        {
            "id": "rates",
            "time": "12:00",
            "speaker": "Deputy Governor",
            "speaker_icon": "banker",
            "title": "The interest rate meeting",
            "situation": _fmt(
                "The Monetary Policy Committee is waiting for you. The interest rate is what banks charge for "
                "loans. A higher rate means fewer loans, less new money created and less spending. A lower rate "
                "means more of all three. The markets are watching. What rate do you set?",
                island,
            ),
            "options": [
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
                    "summary": "This is a supply shock and rates can't make oil flow, so you wait and watch.",
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
                        "Spending rose on top of a supply shock",
                        "The {currency} weakened because foreign savers left for higher returns elsewhere",
                        "Inflation got fuel and a weaker currency at the same time",
                    ],
                    "history": "Turkey cut rates during high inflation in 2021. The lira lost about 44% of its value that year.",
                },
            ],
        },
        {
            "id": "food",
            "time": "14:00",
            "speaker": "Trade Minister",
            "speaker_icon": "trade",
            "title": "Queues outside the bakeries",
            "situation": _fmt(
                "Granara's grain fields are a battlefield. Bread and rice prices on {island} are up 25% and "
                "climbing. Families are queueing from dawn, and shopkeepers are being accused of hoarding.",
                island,
            ),
            "options": [
                {
                    "id": "price_cap",
                    "title": "Cap bread prices by law",
                    "icon": "🔒",
                    "summary": "Bakers can't charge more than last month's price. Anyone caught breaking the law is fined.",
                    "today": {"approval": 9, "reserves": 0.0, "debt": 0.0, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Bread at the old price! Thank you, Governor!\""},
                    "levers": {"price_cap": True},
                    "chain": [
                        "You capped bread prices",
                        "Bakers were selling below what the flour cost them, so many stopped baking",
                        "Shelves emptied and a black market appeared at even higher prices",
                        "When the cap was lifted, prices jumped to catch up",
                    ],
                    "history": "Venezuela capped food prices in the 2010s. Shelves emptied and queues became part of daily life.",
                },
                {
                    "id": "food_stamps",
                    "title": "Food vouchers for poor families",
                    "icon": "🧺",
                    "summary": "Prices stay at market level. The poorest 30% get monthly food vouchers.",
                    "today": {"approval": 4, "reserves": 0.0, "debt": 0.6, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"It's not much, but my kids are eating.\""},
                    "levers": {"food_stamps": True},
                    "chain": [
                        "You gave food vouchers to the poorest families",
                        "Prices kept signalling the shortage, so farmers planted more",
                        "The poorest were protected, at a modest cost to the budget",
                    ],
                    "history": "India's Public Distribution System and America's SNAP shield poor families from food price spikes.",
                },
                {
                    "id": "tariff_cut",
                    "title": "Scrap import taxes on food",
                    "icon": "🚢",
                    "summary": "Let cheaper food in from anywhere. Local farmers will face tough competition.",
                    "today": {"approval": 3, "reserves": -0.3, "debt": 0.3, "currency": -0.3, "crowd": "mixed",
                              "quote": "\"Cheaper rice, but my uncle's farm is struggling.\""},
                    "levers": {"tariff_cut": True},
                    "chain": [
                        "You removed taxes on imported food",
                        "Cheaper food arrived from distant islands and took the edge off price rises",
                        "Local farmers lost sales to the imports",
                        "More imports meant more of {island}'s savings flowed abroad",
                    ],
                    "history": "Countries regularly cut grain tariffs during price spikes. India and Egypt both did it in 2022.",
                },
                {
                    "id": "nothing",
                    "title": "Let the market adjust",
                    "icon": "🤷",
                    "summary": "High prices will draw in new supply on their own. You do nothing.",
                    "today": {"approval": -6, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"Let them eat cake, is it?\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You left food prices to the market",
                        "Prices rose, and the poorest families felt it most",
                        "Over time, high prices drew in new supply",
                    ],
                    "history": "\"Let the market sort it out\" is often right in theory, but it can be politically brutal.",
                },
            ],
        },
        {
            "id": "wages",
            "time": "16:00",
            "speaker": "Union Leader",
            "speaker_icon": "union",
            "title": "The union is at the gate",
            "situation": _fmt(
                "Prices are up and wages aren't. The national workers' union is demanding a 20% raise for "
                "all public and port workers, and threatening a general strike by tomorrow.",
                island,
            ),
            "options": [
                {
                    "id": "grant",
                    "title": "Grant the full 20%",
                    "icon": "🤝",
                    "summary": "Workers get their raise. Businesses will have to pay for it somehow.",
                    "today": {"approval": 8, "reserves": 0.0, "debt": 1.0, "currency": -1.0, "crowd": "cheer",
                              "quote": "\"Twenty percent! Drinks are on me!\""},
                    "levers": {"wage_push": 20.0, "credibility": -0.05},
                    "chain": [
                        "You granted a 20% pay rise",
                        "Businesses passed the higher wage bill on as higher prices",
                        "Higher prices led workers to demand even more: the wage-price spiral",
                        "Everyone came to expect inflation, and that made it stick",
                    ],
                    "history": "Britain's 1970s wage-price spiral peaked at 25% inflation, followed by the 1978–79 'Winter of Discontent'.",
                },
                {
                    "id": "deal",
                    "title": "Offer 8% plus an inflation pledge",
                    "icon": "📝",
                    "summary": "A partial raise, plus your public promise to bring inflation back down.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 0.4, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Eight percent. We'll hold you to that promise.\""},
                    "levers": {"wage_push": 8.0, "credibility": 0.05},
                    "baseline": True,
                    "chain": [
                        "You offered a partial raise and a promise",
                        "Workers kept some of their buying power",
                        "Your promise steadied what people expected inflation to be",
                    ],
                    "history": "Ireland's social partnership deals (1987–2009) traded moderate raises for economic stability.",
                },
                {
                    "id": "refuse",
                    "title": "Refuse: wages must wait",
                    "icon": "✋",
                    "summary": "No raise. You can't fight inflation by adding to it.",
                    "today": {"approval": -9, "reserves": -0.2, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"GENERAL STRIKE! Shut down the port!\""},
                    "levers": {"wage_push": 0.0, "strike": True},
                    "chain": [
                        "You refused the pay rise",
                        "The union shut down the port for weeks",
                        "Goods piled up and the economy lost output",
                        "Wages didn't feed into prices, but workers' real pay fell",
                    ],
                    "history": "Thatcher refused the 1984–85 miners' demands. The strike lasted a year and its scars lasted decades.",
                },
            ],
        },
        {
            "id": "company",
            "time": "18:00",
            "speaker": f"CEO, {island['company']['name']}",
            "speaker_icon": "ceo",
            "title": f"{island['company']['name']} is in trouble",
            "situation": _fmt(
                "{company}, the island's biggest employer with {workers} workers, {crisis}. "
                "Its CEO is in your office saying the company will collapse within weeks without help.",
                island,
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
                },
            ],
        },
        _future_card(island),
    ]
    for card in cards:
        for option in card["options"]:
            option["summary"] = _fmt(option["summary"], island)
            option["chain"] = [_fmt(step, island) for step in option["chain"]]
    return cards


def find_option(cards: list[dict], card_id: str, option_id: str) -> dict | None:
    for card in cards:
        if card["id"] == card_id:
            return next((o for o in card["options"] if o["id"] == option_id), None)
    return None


def baseline_option(card: dict) -> dict:
    return next(o for o in card["options"] if o.get("baseline"))
