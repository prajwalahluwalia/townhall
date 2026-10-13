"""External affairs: Aurum and Forge start a trade war, and every small island is caught in between."""

from .common import company_card, finalize, future_card, rates_card

SCENARIO = {
    "id": "tariff_wall",
    "category": "External affairs",
    "icon": "🧱",
    "title": "The Tariff Wall",
    "tagline": "The two biggest powers start a trade war. Small islands are caught in the middle.",
    "intro": (
        "This morning Aurum put a 35% tax on everything it imports. Forge struck back within hours. The two "
        "giants buy most of the world's goods, and both want {island} on their side. Every decision you make "
        "today will echo through the next two years."
    ),
    "briefing": [
        "📦 Exports to Aurum now cost buyers 35% more",
        "💻 Forge's electronics and parts get pricier",
        "💵 Money rushes into Aurum's ducats, so the {currency} slides",
        "🤝 Both giants demand you pick a side",
    ],
    "teaches": "Trade: who really pays for tariffs, and why exporters suffer when the giants fight.",
    "map": "trade",
    "status": {"active": "🧱 Trade war", "over": "🤝 Trade truce"},
    "causes": {
        "supply": ["Pricier imports from tariffs", "Tariffs and tangled supply chains made imported goods cost more."],
    },
    "news": {
        # one story per quarter while the crisis lasts, then the recovery
        "during": [
            "Aurum's tariff wall goes up: container ships turn back mid-ocean",
            "Ports quiet as orders from Aurum dry up",
            "Forge hits back with its own tariffs, and world trade slows",
            "Factories on the move: islands scramble to win them",
            "Shipping lines cut routes as world trade shrinks",
            "Talks between Aurum and Forge collapse again",
            "Rumours of a deal between the giants",
        ],
        "end": "TRADE TRUCE: Aurum and Forge agree to cut tariffs",
        "after": [
            "Container ships return to their old routes",
            "Two years on: the world trades again, but warily",
        ],
    },
    "shock": {
        "risk": [2.0, 1.5, 1.2, 1.0, 0.6, 0.4, 0.2, 0.0],
        "demand": [-1.0, -2.0, -2.5, -2.3, -1.8, -1.2, -0.5, 0.0],
        "supply": [0.6, 1.0, 1.1, 1.0, 0.8, 0.5, 0.2, 0.0],
        "layoffs": [0.4, 1.0, 1.6, 1.7, 1.4, 1.0, 0.5, 0.0],
        "exposure": "exports",
        "ends": 7,
    },
}


def cards(island: dict) -> list[dict]:
    return finalize([
        {
            "id": "sides",
            "time": "08:00",
            "speaker": "Foreign Minister",
            "speaker_icon": "diplomat",
            "title": "Aurum's ultimatum",
            "situation": (
                "Aurum will spare {island}'s goods from its tariffs if you ban Forge's electronics and "
                "phone networks. Forge says that if you do, it will stop selling you parts and machines. "
                "Both ambassadors want an answer by noon."
            ),
            "options": [
                {
                    "id": "aurum",
                    "title": "Take Aurum's deal, ban Forge tech",
                    "icon": "💵",
                    "summary": "Your exports get into Aurum tariff-free. Replacing every Forge network and machine will be costly.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.5, "currency": 1.5, "crowd": "mixed",
                              "quote": "\"Our exports are saved! My new phone just got dearer.\""},
                    "levers": {"trade": 0.6, "supply_push": 1.0},
                    "chain": [
                        "You sided with Aurum and banned Forge's technology",
                        "Your exports kept flowing into Aurum",
                        "Ripping out and replacing Forge equipment cost a fortune",
                        "Electronics and machines got pricier",
                    ],
                    "history": "Many countries removed Chinese telecom equipment under US pressure after 2019. Britain's Huawei ban cost about £2 billion.",
                },
                {
                    "id": "forge",
                    "title": "Side with Forge",
                    "icon": "🏭",
                    "summary": "Cheap Forge goods keep flowing. Aurum's tariffs hit your exports in full.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": -2.0, "crowd": "mixed",
                              "quote": "\"Cheap goods are nice. Losing Aurum's market isn't.\""},
                    "levers": {"trade": -0.4, "supply_push": -0.5, "confidence": -0.2},
                    "chain": [
                        "You sided with Forge",
                        "Forge's goods stayed cheap, which kept a lid on prices",
                        "Aurum's buyers turned away from {island}",
                        "Investors who rely on Aurum's ducats got nervous",
                    ],
                    "history": "Hungary courted Chinese factories while staying in the EU. It won investment but strained ties with its allies.",
                },
                {
                    "id": "neutral",
                    "title": "Stay neutral, trade with both",
                    "icon": "⚖️",
                    "summary": "Refuse to pick a side. Neither giant is pleased, but neither is shut out.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Friends with everyone. Can that last?\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You stayed neutral",
                        "Both giants kept trading with you, a bit grudgingly",
                        "Some factories moved to {island} to dodge the tariffs",
                    ],
                    "history": "Vietnam and Mexico gained factories from the 2018–19 US–China trade war by staying open to both sides.",
                },
                {
                    "id": "bloc",
                    "title": "Unite the small islands into a trading bloc",
                    "icon": "🌐",
                    "summary": "Together, the small islands are a market big enough for the giants to respect.",
                    "today": {"approval": 4, "reserves": -0.1, "debt": 0.2, "currency": 0.5, "crowd": "cheer",
                              "quote": "\"Strength in numbers!\""},
                    "levers": {"trade": 0.2, "shorten_if_trusted": 1},
                    "chain": [
                        "You rallied the small islands into a bloc",
                        "Trade between the small islands grew",
                        "If {island} was trusted enough, the bloc pushed the giants to a truce sooner",
                    ],
                    "history": "ASEAN and the EU let small economies negotiate trade as one big market.",
                },
            ],
        },
        {
            "id": "retaliate",
            "time": "10:00",
            "speaker": "Trade Minister",
            "speaker_icon": "trade",
            "title": "Hit back?",
            "situation": (
                "{island}'s exporters are furious. The opposition says {island} looks weak and should put its "
                "own tariffs on Aurum's goods. The Trade Minister has drafted three plans."
            ),
            "options": [
                {
                    "id": "match",
                    "title": "Matching 35% tariffs on Aurum's goods",
                    "icon": "🧱",
                    "summary": "Tax everything from Aurum. Show {island} can't be pushed around.",
                    "today": {"approval": 8, "reserves": 0.3, "debt": -0.3, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"Two can play that game!\""},
                    "levers": {"tariff": 35.0},
                    "chain": [
                        "You put a 35% tax on Aurum's goods",
                        "Importers paid the tax and passed it on in their prices",
                        "Aurum punished {island}'s exporters even harder",
                        "{island}'s shoppers paid most of the cost",
                    ],
                    "history": "When the US raised tariffs in 2018, China and the EU hit back. Studies found that consumers on both sides paid most of the cost.",
                    "news": [[2, "bad", "Aurum goods 35% dearer: shoppers feel the tariff"]],
                },
                {
                    "id": "negotiate",
                    "title": "Negotiate quietly",
                    "icon": "🤫",
                    "summary": "No tariffs. Send envoys to Aurum to ask for exemptions.",
                    "today": {"approval": -3, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"Begging for scraps. Pathetic.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You negotiated instead of retaliating",
                        "Prices at home didn't get an extra push",
                        "A few exporters won exemptions",
                    ],
                    "history": "Many smaller economies negotiated exemptions from the 2018 US tariffs instead of fighting back.",
                },
                {
                    "id": "open_up",
                    "title": "Cut tariffs for everyone else",
                    "icon": "🚢",
                    "summary": "Make {island} the easiest place to trade with. Find new partners for imports and exports.",
                    "today": {"approval": -1, "reserves": -0.2, "debt": 0.3, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Cheaper imports, yes. My farm can't compete with that.\""},
                    "levers": {"tariff": -10.0, "trade": 0.3},
                    "chain": [
                        "You cut tariffs on imports from everyone except the giants",
                        "Cheaper imports took the edge off prices",
                        "New partners started buying {island}'s goods",
                        "Some local producers lost out to the competition",
                    ],
                    "history": "New Zealand and Chile cut their own tariffs without waiting for others, and found new markets across Asia.",
                },
            ],
        },
        {
            "id": "currency",
            "time": "12:00",
            "speaker": "Central Bank Governor",
            "speaker_icon": "banker",
            "title": "The {currency} is sliding",
            "situation": (
                "Money is rushing into Aurum's ducats, the world's safe place in a storm. The {currency} has "
                "lost 6% this week. Importers are panicking about the price of fuel and parts."
            ),
            "options": [
                {
                    "id": "defend",
                    "title": "Spend reserves to defend it",
                    "icon": "🛡️",
                    "summary": "Sell ducats from the reserves to buy {currency}s and hold its value up.",
                    "today": {"approval": 2, "reserves": -1.5, "debt": 0.0, "currency": 2.5, "crowd": "mixed",
                              "quote": "\"Good. My imports were getting too expensive.\""},
                    "levers": {"fx_support": 2.0},
                    "chain": [
                        "You sold reserves to prop up the {currency}",
                        "The slide stopped for a while",
                        "Imports stayed cheaper",
                        "But reserves fell, leaving less cushion for the next shock",
                    ],
                    "history": "In 1992, the Bank of England spent billions defending the pound, then gave up on 'Black Wednesday'.",
                },
                {
                    "id": "float",
                    "title": "Let it fall",
                    "icon": "🪂",
                    "summary": "A cheaper {currency} makes exports cheaper abroad, which softens the tariff.",
                    "today": {"approval": -2, "reserves": 0.0, "debt": 0.0, "currency": -1.0, "crowd": "mixed",
                              "quote": "\"My holiday abroad just got a lot more expensive.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You let the {currency} find its own level",
                        "Exports got cheaper for foreign buyers",
                        "Imports cost more, which pushed prices up",
                    ],
                    "history": "A cheaper currency often softens a trade war for exporters, but makes imports dearer at home.",
                },
                {
                    "id": "controls",
                    "title": "Limit money leaving the island",
                    "icon": "🚧",
                    "summary": "Capital controls: nobody can move more than a small amount abroad without permission.",
                    "today": {"approval": -1, "reserves": 0.5, "debt": 0.0, "currency": 1.0, "crowd": "mixed",
                              "quote": "\"So my money is stuck here now?\""},
                    "levers": {"capital_controls": True, "credibility": -0.06},
                    "chain": [
                        "You blocked money from leaving {island}",
                        "The slide in the {currency} slowed",
                        "Foreign investors grew wary of putting money in",
                    ],
                    "history": "Malaysia imposed capital controls in 1998. They worked for a while, but investors stayed wary.",
                },
            ],
        },
        rates_card("14:00", (
            "Exporters are losing orders, but imports are getting pricier as the {currency} slides. The "
            "committee is split."
        ), {
            "hold": {"summary": "The slowdown and the price rises roughly cancel out. You wait."},
        }),
        {
            "id": "industry",
            "time": "16:00",
            "speaker": "Industry Minister",
            "speaker_icon": "ceo",
            "title": "Factories want help",
            "situation": (
                "Factories that sold to Aurum are cutting shifts. Their owners want the government to step in "
                "before the layoffs start."
            ),
            "options": [
                {
                    "id": "subsidy",
                    "title": "Subsidise exporters",
                    "icon": "💰",
                    "summary": "The government covers part of the tariff so exporters can keep their prices down.",
                    "today": {"approval": 4, "reserves": 0.0, "debt": 1.5, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"Orders are back on! For now.\""},
                    "levers": {"fiscal": 0.4, "trade": 0.3},
                    "chain": [
                        "You paid part of the tariff for exporters",
                        "Factories kept their orders and their workers",
                        "The cost went onto the debt",
                        "Aurum complained about unfair subsidies",
                    ],
                    "history": "China supported its exporters to ride out US tariffs in 2018–19, and drew more trade complaints.",
                },
                {
                    "id": "new_markets",
                    "title": "Find new markets",
                    "icon": "🧭",
                    "summary": "Trade missions and new trade deals with islands beyond the two giants.",
                    "today": {"approval": 1, "reserves": -0.1, "debt": 0.3, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"New buyers? Takes years to win them.\""},
                    "levers": {"trade": 0.25},
                    "chain": [
                        "You sent trade missions to new markets",
                        "It took time, but new buyers appeared",
                        "{island} became less dependent on Aurum",
                    ],
                    "history": "When China blocked Australian coal and barley in 2020, exporters found new buyers in India and elsewhere within a couple of years.",
                },
                {
                    "id": "retrain",
                    "title": "Help workers move to new jobs",
                    "icon": "🎓",
                    "summary": "Let the weakest factories shrink, and pay workers while they retrain.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.8, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Retrain for what, exactly?\""},
                    "levers": {"job_protect": 0.4, "fiscal": 0.25},
                    "chain": [
                        "You paid workers to retrain instead of saving their factories",
                        "Fewer people ended up long-term unemployed",
                        "The weakest factories closed",
                    ],
                    "history": "Denmark's 'flexicurity' lets firms cut jobs easily, but pays generously to retrain workers.",
                },
                {
                    "id": "nothing",
                    "title": "Let them adjust",
                    "icon": "🤷",
                    "summary": "Businesses adapt. That's what businesses do.",
                    "today": {"approval": -5, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"Adjust? They mean fire us.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You left exporters to adapt on their own",
                        "Some found new buyers, others cut jobs",
                    ],
                    "history": "Without help, regions hit by import competition often take a decade or more to recover.",
                },
            ],
        },
        company_card(island, "18:00"),
        future_card(island, "20:00", (
            "Even if the giants make peace, trade walls may be here to stay. {island} still depends on others "
            "for fuel and has only a thin cushion of savings. How do you prepare for a more divided world?"
        )),
    ], island)
