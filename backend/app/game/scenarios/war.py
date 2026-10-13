"""War: Petra invades Granara and the Strait of Teeth closes. A supply shock to oil and grain."""

from .common import company_card, finalize, future_card, rates_card

SCENARIO = {
    "id": "strait_crisis",
    "category": "War",
    "icon": "⚔️",
    "title": "The Strait Crisis",
    "tagline": "Two neighbours go to war and the world's oil and grain route closes.",
    "intro": (
        "At dawn on your first day as Governor, Petra and Granara go to war. The Strait of Teeth, "
        "which carries the world's oil and grain, is closed. Every decision you make today will "
        "echo through the next two years."
    ),
    "briefing": [
        "⛽ Oil prices jump 45% overnight",
        "🌾 Grain from Granara stops arriving",
        "💸 Scared investors pull money into Aurum's safe ducats",
    ],
    "teaches": "Supply shocks: prices rise because things got scarce, not because people are spending more.",
    "map": "war",
    "status": {"active": "⚔️ War continues", "over": "🕊️ Peace"},
    "causes": {
        "fuel": ["Fuel prices (the war)", "Oil from the strait got scarce and expensive. That cost travels into transport, farming and factories."],
        "food": ["Food prices (the war)", "Granara's grain fields became a battlefield."],
    },
    "news": {
        # one story per quarter while the crisis lasts, then the recovery
        "during": [
            "Tankers stuck at the Strait of Teeth as war drags on",
            "Petra's army digs in; tankers still queue outside the strait",
            "Fighting intensifies around Granara's grain ports",
            "Peace envoys shuttle between Petra and Granara",
            "No end in sight: the strait stays shut for another season",
        ],
        "end": "CEASEFIRE: Petra and Granara sign truce, strait reopens",
        "after": [
            "First grain ships from Granara in a year dock at {island}",
            "Oil prices drift back towards pre-war levels",
            "Granara replants its scorched fields",
            "Two years on: {island} counts the cost of the war",
        ],
    },
    "shock": {
        "oil": [45, 55, 40, 28, 15, 8, 4, 2],
        "grain": [25, 32, 28, 18, 10, 5, 2, 0],
        "risk": [3.0, 2.5, 1.5, 1.0, 0.5, 0.0, 0.0, 0.0],
        "ends": 5,
    },
}


def cards(island: dict) -> list[dict]:
    return finalize([
        {
            "id": "war",
            "time": "08:00",
            "speaker": "Foreign Minister",
            "speaker_icon": "diplomat",
            "title": "The Strait of Teeth is closed",
            "situation": (
                "Petra has invaded Granara's northern farmlands. Tankers and grain ships are stuck outside "
                "the strait. Aurum and Forge are demanding that everyone sanction Petra. Petra is offering "
                "cheap oil to anyone who stays neutral. What is {island}'s position?"
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
                    "levers": {"stance": "mediate", "shorten_if_trusted": 1},
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
            "situation": (
                "Petrol is up 40% overnight. Taxi drivers have blocked the main bridge, fishermen can't afford "
                "diesel, and the evening news is calling it a crisis. People want you to do something now."
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
                    "news": [[5, "bad", "Treasury can't afford fuel subsidy any longer, so pump prices jump"]],
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
                    "news": [[2, "bad", "\"Where did all this money come from?\" Shops raise prices on everything"]],
                },
            ],
        },
        rates_card("12:00", "The Monetary Policy Committee is waiting for you. The markets are watching.", {
            "hold": {"summary": "This is a supply shock and rates can't make oil flow, so you wait and watch."},
            "cut": {
                "chain": [
                    "You cut interest rates",
                    "Cheap loans meant banks lent more, and every new loan creates new money",
                    "Spending rose on top of a supply shock",
                    "The {currency} weakened because foreign savers left for higher returns elsewhere",
                    "Inflation got fuel and a weaker currency at the same time",
                ],
                "history": "Turkey cut rates during high inflation in 2021. The lira lost about 44% of its value that year.",
            },
        }),
        {
            "id": "food",
            "time": "14:00",
            "speaker": "Trade Minister",
            "speaker_icon": "trade",
            "title": "Queues outside the bakeries",
            "situation": (
                "Granara's grain fields are a battlefield. Bread and rice prices on {island} are up 25% and "
                "climbing. Families are queueing from dawn, and shopkeepers are being accused of hoarding."
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
                    "news": [[2, "bad", "Empty bakery shelves: price cap sparks black market bread"]],
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
            "situation": (
                "Prices are up and wages aren't. The national workers' union is demanding a 20% raise for "
                "all public and port workers, and threatening a general strike by tomorrow."
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
                    "news": [[1, "bad", "General strike shuts the port"]],
                },
            ],
        },
        company_card(island, "18:00"),
        future_card(island, "20:00", (
            "The day is ending. The crisis will pass eventually, but {island} will still burn imported fuel "
            "and still have only a thin cushion of savings. How do you prepare {island} for the next shock?"
        )),
    ], island)
