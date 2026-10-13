"""Internal affairs: hidden government debt is exposed. Trust collapses at home and in the bond market."""

from .common import company_card, finalize, finance_option, rates_card

SCENARIO = {
    "id": "hidden_debt",
    "category": "Internal affairs",
    "icon": "🗂️",
    "title": "The Hidden Debt",
    "tagline": "A leak reveals the last government hid a mountain of debt.",
    "intro": (
        "At dawn, a newspaper publishes leaked documents: the last government secretly borrowed billions and "
        "hid it off the books. {island}'s real debt is far bigger than anyone was told. Protesters are "
        "already gathering, and the bond markets open in an hour. Every decision you make today will echo "
        "through the next two years."
    ),
    "briefing": [
        "📄 Real debt is 15% of GDP higher than reported",
        "📉 Lenders want much higher interest to keep lending",
        "✊ Crowds fill the main square demanding answers",
        "🏦 Money is quietly leaving for Aurum",
    ],
    "teaches": "Trust: why a government's honesty about money decides how much it costs to borrow.",
    "map": None,
    "status": {"active": "✊ Crisis of trust", "over": "🤝 Trust returning"},
    "causes": {},
    "news": {
        # one story per quarter while the crisis lasts, then the recovery
        "during": [
            "HIDDEN DEBT: {island}'s real borrowing far higher than reported",
            "Auditors find more loans kept off the books",
            "Ratings agencies keep {island} on 'junk' watch",
            "Former ministers questioned by investigators",
            "Lenders still demand a steep premium to lend to {island}",
        ],
        "end": "Bond buyers return as {island}'s borrowing costs fall",
        "after": [
            "Former finance minister goes on trial",
            "Ratings agencies lift {island} off 'junk' watch",
            "Two years on: can {island} trust its government again?",
        ],
    },
    "shock": {
        "risk": [4.0, 3.0, 2.0, 1.2, 0.6, 0.2, 0.0, 0.0],
        "demand": [-2.0, -2.4, -1.8, -1.0, -0.4, 0.0, 0.0, 0.0],
        "layoffs": [0.6, 1.2, 1.2, 0.8, 0.4, 0.0, 0.0, 0.0],
        "exposure": None,
        "ends": 5,
        "start": {"debt_to_gdp": 15.0, "approval": -8.0, "currency_index": -3.0},
        "credibility": -0.08,
    },
}


def cards(island: dict) -> list[dict]:
    return finalize([
        {
            "id": "leak",
            "time": "08:00",
            "speaker": "Chief of Staff",
            "speaker_icon": "press",
            "title": "The leak",
            "situation": (
                "Every newspaper on {island} has the documents. Journalists are outside asking one question: "
                "what else is the government hiding? Your Chief of Staff has drafted three statements."
            ),
            "options": [
                {
                    "id": "publish",
                    "title": "Publish everything and order an audit",
                    "icon": "📂",
                    "summary": "Release every account. Independent auditors check the books and report publicly.",
                    "today": {"approval": -3, "reserves": 0.0, "debt": 0.0, "currency": 1.0, "crowd": "mixed",
                              "quote": "\"At least someone's finally being straight with us.\""},
                    "levers": {"credibility": 0.12, "contain": 0.3},
                    "chain": [
                        "You opened the books to independent auditors",
                        "The full picture was painful, but there were no more surprises",
                        "Lenders could price the risk, so the panic calmed sooner",
                    ],
                    "history": "After Mozambique's $2 billion of hidden loans came out in 2016, donors froze aid until an independent audit was published.",
                },
                {
                    "id": "deny",
                    "title": "Deny it and blame the leakers",
                    "icon": "🙅",
                    "summary": "Call the documents fake and launch a hunt for whoever leaked them.",
                    "today": {"approval": 3, "reserves": 0.0, "debt": 0.0, "currency": -2.0, "crowd": "mixed",
                              "quote": "\"Fake? Then why do they look so real?\""},
                    "levers": {"credibility": -0.12, "contain": -0.4},
                    "chain": [
                        "You denied the leak",
                        "Some supporters believed you",
                        "Lenders assumed the worst, so borrowing costs rose further",
                        "When more documents came out, trust fell even lower",
                    ],
                    "history": "Greece understated its deficits for years. When the truth came out in 2009, markets punished it far more harshly.",
                    "news": [[2, "bad", "Second leak: more hidden loans found"]],
                },
                {
                    "id": "sack",
                    "title": "Sack the officials responsible",
                    "icon": "🚪",
                    "summary": "The head of the debt office and two advisers resign today. A review will follow.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Heads rolled. Doesn't fix the debt.\""},
                    "levers": {"credibility": 0.02},
                    "baseline": True,
                    "chain": [
                        "You sacked the officials responsible",
                        "It bought a few days of calm",
                        "Lenders still waited for real numbers before trusting {island} again",
                    ],
                    "history": "Sacking officials buys a few days of calm. Markets want numbers, not resignations.",
                },
            ],
        },
        {
            "id": "protests",
            "time": "10:00",
            "speaker": "Police Chief",
            "speaker_icon": "police",
            "title": "The square is full",
            "situation": (
                "Fifty thousand people are in the main square chanting \"Where did the money go?\" Some have "
                "started blocking the roads to the port. The Police Chief wants your orders."
            ),
            "options": [
                {
                    "id": "crackdown",
                    "title": "Clear the square by force",
                    "icon": "🛡️",
                    "summary": "Riot police, tear gas, arrests. Order is restored by tonight.",
                    "today": {"approval": -8, "reserves": 0.0, "debt": 0.0, "currency": -1.0, "crowd": "boo",
                              "quote": "\"They gassed my daughter. For asking a question.\""},
                    "levers": {"confidence": -0.3, "credibility": -0.04, "drag_now": 0.4},
                    "chain": [
                        "You cleared the square by force",
                        "Footage spread across every island",
                        "Protests grew instead of shrinking",
                        "Investors saw instability and pulled more money out",
                    ],
                    "history": "In Sri Lanka in 2022, attacks on protesters over the economic collapse made the protests grow, and the president fled the country.",
                    "news": [[1, "bad", "Tear gas in the square: protests spread to every town"]],
                },
                {
                    "id": "commission",
                    "title": "An anti-corruption commission, with protesters on it",
                    "icon": "⚖️",
                    "summary": "Independent investigators with real powers. Protest leaders get seats on the board.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 0.3, "currency": 0.5, "crowd": "cheer",
                              "quote": "\"A seat at the table! Now we'll see who took what.\""},
                    "levers": {"credibility": 0.06, "confidence": 0.15, "fiscal": 0.1},
                    "chain": [
                        "You set up an independent anti-corruption commission",
                        "Protesters went home to watch it work",
                        "Investors saw a government willing to be checked",
                    ],
                    "history": "Hong Kong's ICAC, set up in 1974 after protests about police corruption, helped make it one of the cleanest cities in Asia.",
                },
                {
                    "id": "elections",
                    "title": "Call early elections",
                    "icon": "🗳️",
                    "summary": "Let the people decide who should clean this up. Voting in three months.",
                    "today": {"approval": 3, "reserves": 0.0, "debt": 0.2, "currency": -1.0, "crowd": "mixed",
                              "quote": "\"An election? Fine. But who do we vote for?\""},
                    "levers": {"credibility": 0.02, "confidence": -0.15},
                    "chain": [
                        "You called early elections",
                        "Protesters stood down to campaign",
                        "Investors waited for the result before doing anything",
                    ],
                    "history": "Early elections can reset trust, but months of uncertainty make investors wait.",
                },
                {
                    "id": "wait",
                    "title": "Let them protest",
                    "icon": "⏳",
                    "summary": "Protest is a right. They'll go home when they're tired.",
                    "today": {"approval": -3, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"We'll be here tomorrow, and the day after.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You let the protests run their course",
                        "Roads were blocked on and off for weeks",
                        "The anger slowly faded",
                    ],
                    "history": "Most protests over scandals fade within weeks if nothing new comes out.",
                },
            ],
        },
        {
            "id": "debt",
            "time": "12:00",
            "speaker": "Head of the Debt Office",
            "speaker_icon": "finance",
            "title": "Lenders want 12%",
            "situation": (
                "{island} must repay a large loan next month and has to borrow again to do it. Lenders who "
                "charged 5% last year now want 12%. The new head of the debt office lays out the options."
            ),
            "options": [
                finance_option(island),
                {
                    "id": "restructure",
                    "title": "Ask lenders to accept less",
                    "icon": "✂️",
                    "summary": "Stop paying and negotiate: lenders get back less than they're owed, over a longer time.",
                    "today": {"approval": 4, "reserves": 0.8, "debt": -12.0, "currency": -4.0, "crowd": "cheer",
                              "quote": "\"Why should we pay for their lies?\""},
                    "levers": {"credibility": -0.12, "confidence": -0.4},
                    "chain": [
                        "You stopped paying and asked lenders to take a loss",
                        "The debt shrank overnight",
                        "Lenders shunned {island}, and money fled",
                        "Borrowing stayed expensive for years",
                    ],
                    "history": "Ecuador (2020) and Ghana (2022) restructured their debts. Lenders took losses, and borrowing costs stayed high for years.",
                    "news": [[1, "bad", "{island} DEFAULTS: lenders to take losses"]],
                },
                {
                    "id": "cb_buys",
                    "title": "Have the central bank buy the bonds",
                    "icon": "🖨️",
                    "summary": "The central bank creates money to lend to the government at 5%.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.0, "currency": -3.0, "crowd": "mixed",
                              "quote": "\"So the bank prints, and we pay at the shops?\""},
                    "levers": {"print_pct": 2.5, "credibility": -0.1},
                    "chain": [
                        "The central bank printed money to lend to the government",
                        "Borrowing stayed cheap on paper",
                        "The new money pushed prices up",
                        "People saw the central bank doing the government's bidding, so trust fell",
                    ],
                    "history": "Argentina's central bank funded government deficits for years. Inflation passed 200% in 2023.",
                },
                {
                    "id": "pay_up",
                    "title": "Pay the 12%",
                    "icon": "💸",
                    "summary": "Painful, but {island} keeps its word and keeps borrowing.",
                    "today": {"approval": -2, "reserves": 0.0, "debt": 2.0, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Twelve percent of what? Of our future, that's what.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You paid the higher rate",
                        "Interest costs ate into the budget",
                        "{island} kept its record of always paying",
                    ],
                    "history": "Italy paid over 7% on its bonds in 2011 rather than default, until the ECB stepped in.",
                },
            ],
        },
        rates_card("14:00", (
            "Money is leaving {island}, the {currency} is falling, and lenders are nervous. Shops are quiet as "
            "people wait to see what happens."
        ), {
            "hike_big": {"summary": "Stop the money leaving and prove the central bank is serious, even if it hurts."},
        }),
        {
            "id": "public_pay",
            "time": "16:00",
            "speaker": "Teachers' and Nurses' Union",
            "speaker_icon": "union",
            "title": "The promised pay rise",
            "situation": (
                "The last government promised teachers and nurses a 10% raise this month. With the hidden debt "
                "exposed, the money isn't there. The unions say a promise is a promise."
            ),
            "options": [
                {
                    "id": "pay_10",
                    "title": "Pay the full 10%",
                    "icon": "🤝",
                    "summary": "A promise is a promise. The debt will have to wait.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 1.2, "currency": -1.0, "crowd": "cheer",
                              "quote": "\"Thank you! We kept the hospitals open through all this.\""},
                    "levers": {"wage_push": 10.0, "fiscal": 0.3, "credibility": -0.03},
                    "chain": [
                        "You paid the promised raise",
                        "Public workers kept their buying power",
                        "The deficit grew, and lenders noticed",
                        "Private employers felt pressure to match it",
                    ],
                    "history": "Greece raised public wages fast in the 2000s. When its crisis hit in 2010, they were cut by up to a third.",
                },
                {
                    "id": "freeze",
                    "title": "Freeze all public pay for a year",
                    "icon": "🧊",
                    "summary": "No raise for anyone until the books are fixed.",
                    "today": {"approval": -7, "reserves": 0.0, "debt": -0.5, "currency": 1.0, "crowd": "boo",
                              "quote": "\"We pay for their lies, again.\""},
                    "levers": {"austerity": 0.5, "credibility": 0.05},
                    "chain": [
                        "You froze public pay",
                        "Public workers' real pay fell as prices rose",
                        "Lenders saw a government getting serious",
                        "Less spending meant a slower economy",
                    ],
                    "history": "Ireland cut public pay by 5–15% in 2009–10. It hurt, but it helped win back the bond market.",
                },
                {
                    "id": "cut_top",
                    "title": "Cut ministers' pay 30%, give workers 4%",
                    "icon": "🎩",
                    "summary": "Leaders take the hit first. Workers get a smaller raise.",
                    "today": {"approval": 7, "reserves": 0.0, "debt": 0.2, "currency": 0.5, "crowd": "cheer",
                              "quote": "\"Ministers taking a pay cut? Now that's new.\""},
                    "levers": {"wage_push": 4.0, "credibility": 0.04},
                    "chain": [
                        "You cut top officials' pay and gave workers a small raise",
                        "It saved little money, but bought a lot of trust",
                        "Workers accepted less than they'd been promised",
                    ],
                    "history": "Leaders in Portugal, Ireland and Greece cut their own pay during their debt crises. It cost little and bought trust.",
                },
                {
                    "id": "half",
                    "title": "Pay 5% now, 5% next year",
                    "icon": "📝",
                    "summary": "Keep the promise, but stretch it out.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 0.6, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Half now. We'll be counting.\""},
                    "levers": {"wage_push": 5.0},
                    "baseline": True,
                    "chain": [
                        "You split the raise over two years",
                        "Workers lost a little buying power",
                        "The budget took a smaller hit",
                    ],
                    "history": "Spreading a raise over time is the usual compromise: workers lose a little, budgets survive.",
                },
            ],
        },
        company_card(island, "18:00"),
        {
            "id": "reform",
            "time": "20:00",
            "speaker": "Planning Minister" if not island["un_eligible"] else "UN Envoy",
            "speaker_icon": "planner" if not island["un_eligible"] else "envoy",
            "title": "Never again",
            "situation": (
                "Before the day ends, you can sign one reform so that no government can hide debt or abuse "
                "{island}'s money again. Which one?"
            ),
            "options": [
                {
                    "id": "independent_cb",
                    "title": "Make the central bank independent",
                    "icon": "🏛️",
                    "summary": "By law, no government can order the central bank to print money or set rates.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": 2.0, "crowd": "mixed",
                              "quote": "\"Sounds dull. Is it important?\""},
                    "levers": {"credibility": 0.15},
                    "chain": [
                        "You made the central bank independent",
                        "People believed it would fight inflation, whoever was in power",
                        "That belief alone kept inflation lower",
                    ],
                    "history": "New Zealand made its central bank independent with an inflation target in 1989. Many countries copied it.",
                },
                {
                    "id": "fiscal_rule",
                    "title": "A debt limit with a watchdog",
                    "icon": "📏",
                    "summary": "A legal limit on borrowing, checked by an independent budget office.",
                    "today": {"approval": -1, "reserves": 0.0, "debt": -0.5, "currency": 1.0, "crowd": "mixed",
                              "quote": "\"A rule they can't break? We'll see.\""},
                    "levers": {"credibility": 0.1, "austerity": 0.3},
                    "chain": [
                        "You passed a debt limit with an independent watchdog",
                        "Lenders trusted the numbers again",
                        "Spending was held back a little",
                    ],
                    "history": "Chile's budget rule (2001) made it save during copper booms and spend in busts.",
                },
                {
                    "id": "amnesty",
                    "title": "A tax amnesty: bring hidden money home",
                    "icon": "🧳",
                    "summary": "Anyone who declares money hidden abroad pays a small fine instead of going to prison.",
                    "today": {"approval": -2, "reserves": 1.0, "debt": -2.0, "currency": 1.0, "crowd": "mixed",
                              "quote": "\"So the cheats get off lightly. Typical.\""},
                    "levers": {"credibility": -0.04},
                    "chain": [
                        "You offered a tax amnesty",
                        "Hidden money came home and paid a little tax",
                        "Reserves rose and the debt fell slightly",
                        "Honest taxpayers learned that cheating pays",
                    ],
                    "history": "Indonesia's 2016 tax amnesty brought large hidden fortunes onto the books, but amnesties teach people to wait for the next one.",
                },
                {
                    "id": "postpone",
                    "title": "Postpone it",
                    "icon": "⏳",
                    "summary": "Fix the crisis first. Reforms can wait.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"They always say 'later'.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You put off reform",
                        "The rules that let debt be hidden stayed in place",
                    ],
                    "history": "Scandals often fade before reforms pass, and the same problems come back.",
                },
            ],
        },
    ], island)
