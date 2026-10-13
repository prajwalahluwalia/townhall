"""Terrorism: bombs at the harbour. Tourists flee, investors panic, insurance and shipping get dearer."""

from .common import company_card, finalize, rates_card

SCENARIO = {
    "id": "harbour_attack",
    "category": "Terrorism",
    "icon": "🚨",
    "title": "Attack on the Harbour",
    "tagline": "Bombs at the harbour festival. Fear spreads faster than the smoke.",
    "intro": (
        "Last night, during the harbour festival, three bombs went off along {island}'s waterfront. Dozens "
        "are dead. The harbour is sealed, tourists are rushing to the airport, and the whole island is "
        "watching you. Every decision you make today will echo through the next two years."
    ),
    "briefing": [
        "🏨 Hotel bookings collapse overnight",
        "📉 Foreign investors pull their money out",
        "🛳️ Shipping insurers raise prices or walk away",
        "😠 Anger looks for someone to blame",
    ],
    "teaches": "Confidence: how fear alone can shrink an economy, and why calm, credible answers matter.",
    "map": None,
    "status": {"active": "🚨 Island on alert", "over": "🕊️ Calm returns"},
    "causes": {
        "supply": ["Security and insurance costs", "Shipping, insurance and security checks made everything imported cost a bit more."],
    },
    "news": {
        # one story per quarter while the crisis lasts, then the recovery
        "during": [
            "Tourists flee {island} after harbour bombings",
            "Armed patrols on the waterfront as the manhunt goes on",
            "Hotels half empty as fear lingers",
            "Last suspects arrested in dawn raids",
            "Travel warnings stay in place for another season",
        ],
        "end": "Harbour festival returns: crowds back on the waterfront",
        "after": [
            "Cruise ships return to {island}'s harbour",
            "Hotel bookings climb back towards normal",
            "Memorial garden opens on the rebuilt waterfront",
            "Two years on: {island} remembers, and moves on",
        ],
    },
    "shock": {
        "risk": [3.5, 2.0, 1.0, 0.5, 0.0, 0.0, 0.0, 0.0],
        "demand": [-4.2, -2.8, -1.5, -0.6, 0.0, 0.0, 0.0, 0.0],
        "supply": [0.7, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0, 0.0],
        "fiscal": [0.4, 0.3, 0.2, 0.1, 0.0, 0.0, 0.0, 0.0],
        "layoffs": [2.2, 1.6, 0.9, 0.4, 0.0, 0.0, 0.0, 0.0],
        "exposure": "tourism",
        "ends": 4,
        "start": {"approval": 4},
    },
}


def cards(island: dict) -> list[dict]:
    return finalize([
        {
            "id": "security",
            "time": "08:00",
            "speaker": "Security Chief",
            "speaker_icon": "security",
            "title": "The morning after",
            "situation": (
                "The attackers belonged to a small group based on a lawless islet across the water. Two of them "
                "are still free. The Security Chief wants your orders before the ten o'clock press conference."
            ),
            "options": [
                {
                    "id": "emergency",
                    "title": "Emergency powers and a curfew",
                    "icon": "🚔",
                    "summary": "Soldiers on the streets, a night curfew, and police can search without warrants.",
                    "today": {"approval": 7, "reserves": 0.0, "debt": 0.4, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Good. I want to see soldiers on every corner.\""},
                    "levers": {"contain": 0.4, "drag_now": 1.0, "credibility": -0.04},
                    "chain": [
                        "You declared emergency powers",
                        "People felt safer, and the threat shrank",
                        "The curfew shut restaurants and bars at night, so spending fell",
                        "Investors worried a little about the rule of law",
                    ],
                    "history": "France declared a state of emergency after the 2015 Paris attacks and kept it for two years.",
                },
                {
                    "id": "investigate",
                    "title": "Hunt the attackers, keep the island open",
                    "icon": "🔎",
                    "summary": "A focused police manhunt. No curfew. You tell people to carry on living normally.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.2, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Carry on as normal? Easy for you to say.\""},
                    "levers": {"contain": 0.2, "confidence": 0.1},
                    "baseline": True,
                    "chain": [
                        "You kept the island open while police hunted the attackers",
                        "Daily life and spending carried on",
                        "Fear faded at its own pace",
                    ],
                    "history": "Norway answered the 2011 Utøya attack with 'more democracy, more openness', and kept ordinary policing.",
                },
                {
                    "id": "strike",
                    "title": "Strike the group's base abroad",
                    "icon": "🎯",
                    "summary": "Send the navy to destroy the camp. Show the world {island} hits back.",
                    "today": {"approval": 11, "reserves": -0.4, "debt": 1.5, "currency": -1.5, "crowd": "cheer",
                              "quote": "\"Finally! Make them pay!\""},
                    "levers": {"fiscal": 0.5, "confidence": -0.3, "trade": -0.2},
                    "chain": [
                        "You launched a military strike abroad",
                        "The crowd loved it, and the group was weakened",
                        "But investors saw a small island heading into a war",
                        "Military costs added to the debt",
                    ],
                    "history": "After 9/11, the US went to war in Afghanistan and Iraq. The wars cost trillions of dollars over two decades.",
                    "news": [[2, "bad", "Navy still engaged abroad as costs mount"]],
                },
            ],
        },
        {
            "id": "tourism",
            "time": "10:00",
            "speaker": "Tourism Minister",
            "speaker_icon": "tourism",
            "title": "Cancellations are pouring in",
            "situation": (
                "Seven in ten hotel bookings for the season were cancelled overnight. Aurum has told its citizens "
                "not to travel to {island}. Hotels say they'll lay off staff next week."
            ),
            "options": [
                {
                    "id": "campaign",
                    "title": "Safety guarantee and a big campaign",
                    "icon": "📣",
                    "summary": "Armed guards at hotels, free cancellation insurance, and ads across every island.",
                    "today": {"approval": 3, "reserves": -0.3, "debt": 0.8, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Guards at the hotels? It's a start.\""},
                    "levers": {"fiscal": 0.2, "confidence": 0.4},
                    "chain": [
                        "You guaranteed tourists' safety and advertised it",
                        "Travellers felt reassured sooner",
                        "Bookings came back faster than they would have",
                    ],
                    "history": "Egypt and Tunisia ran big campaigns after attacks on tourists in 2015. Visitors took about three years to return.",
                },
                {
                    "id": "tax_cut",
                    "title": "Cut tourist taxes and airport fees",
                    "icon": "🏷️",
                    "summary": "Make {island} the cheapest holiday around until the fear fades.",
                    "today": {"approval": 4, "reserves": -0.2, "debt": 1.0, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"Cheap flights will bring them back!\""},
                    "levers": {"fiscal": 0.3, "confidence": 0.2},
                    "chain": [
                        "You cut taxes and fees on tourists",
                        "Bargain hunters came back first",
                        "The government gave up tax income it badly needed",
                    ],
                    "history": "After the 2002 Bali bombings, Indonesia cut fees and promoted the island. Tourist numbers recovered within about two years.",
                },
                {
                    "id": "retrain",
                    "title": "Pay tourism workers to retrain",
                    "icon": "🎓",
                    "summary": "Accept tourism will be slow. Help hotel staff train for new jobs.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.7, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"I've been a waiter for twenty years. Now what?\""},
                    "levers": {"job_protect": 0.5, "fiscal": 0.25},
                    "chain": [
                        "You paid tourism workers to retrain",
                        "Fewer people ended up unemployed",
                        "Tourism itself recovered at its own pace",
                    ],
                    "history": "Many tourist economies in crisis have paid hotel staff to train for other jobs. It protects people, but not the industry.",
                },
                {
                    "id": "wait",
                    "title": "Wait for the tourists to come back",
                    "icon": "⏳",
                    "summary": "Fear fades. Tourists always come back eventually.",
                    "today": {"approval": -4, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"Eventually? My hotel won't last till eventually.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You waited for tourists to return",
                        "Hotels cut staff while they waited",
                        "Bookings came back slowly",
                    ],
                    "history": "Tourism usually returns within one to three years after an attack, if there isn't another one.",
                },
            ],
        },
        {
            "id": "blame",
            "time": "12:00",
            "speaker": "Interior Minister",
            "speaker_icon": "police",
            "title": "Anger turns on outsiders",
            "situation": (
                "The attackers came from abroad. Now a crowd outside wants all 80,000 foreign workers expelled. "
                "Those workers run the docks, the kitchens and the building sites."
            ),
            "options": [
                {
                    "id": "expel",
                    "title": "Send the foreign workers home",
                    "icon": "🧳",
                    "summary": "Cancel their work permits. Jobs go to locals.",
                    "today": {"approval": 8, "reserves": 0.0, "debt": 0.0, "currency": -1.0, "crowd": "cheer",
                              "quote": "\"{island} jobs for {island} people!\""},
                    "levers": {"wage_push": 12.0, "supply_push": 1.2, "credibility": -0.05},
                    "chain": [
                        "You sent 80,000 foreign workers home",
                        "Docks, kitchens and building sites suddenly had nobody to do the work",
                        "Employers bid up wages to find staff, and passed the cost on",
                        "Building, eating out and shipping all got more expensive",
                    ],
                    "history": "After Brexit cut EU migration, Britain ran short of lorry drivers and fruit pickers in 2021, and wages and prices in those jobs jumped.",
                    "news": [[2, "bad", "Ships wait for days at {island}'s docks: 'Nobody left to unload them'"]],
                },
                {
                    "id": "protect",
                    "title": "Stand with them and prosecute hate crimes",
                    "icon": "🫱🏽‍🫲🏻",
                    "summary": "Make clear they are not to blame. Anyone attacking them will be arrested.",
                    "today": {"approval": -4, "reserves": 0.0, "debt": 0.0, "currency": 0.5, "crowd": "boo",
                              "quote": "\"You're defending *them*, today of all days?\""},
                    "levers": {"credibility": 0.02},
                    "baseline": True,
                    "chain": [
                        "You protected the foreign workers",
                        "The docks and kitchens kept running",
                        "The anger faded slowly, and it cost you support",
                    ],
                    "history": "New Zealand's leaders stood with the Muslim community after the 2019 Christchurch attack. Gun laws changed within a month.",
                },
                {
                    "id": "surveil",
                    "title": "A new surveillance law",
                    "icon": "📹",
                    "summary": "Cameras, phone tracking and new powers for the security service.",
                    "today": {"approval": 3, "reserves": 0.0, "debt": 0.4, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"If you've nothing to hide... right?\""},
                    "levers": {"contain": 0.15, "fiscal": 0.1, "credibility": -0.02},
                    "chain": [
                        "You passed a sweeping surveillance law",
                        "The security service found threats sooner",
                        "It cost money, and some investors worried about the rule of law",
                    ],
                    "history": "The US Patriot Act (2001) expanded surveillance quickly. The debate about its cost to privacy lasted for decades.",
                },
            ],
        },
        rates_card("14:00", (
            "Money is leaving {island} for safer places and the {currency} is sliding, but tourists' spending has "
            "dried up and shops are quiet."
        ), {
            "hold": {"summary": "The shock is fear, not overspending. You wait and see if it fades."},
            "hike_big": {"summary": "Defend the {currency} against fleeing money. Loans get expensive just as tourism collapses."},
        }),
        {
            "id": "insurance",
            "time": "16:00",
            "speaker": "Finance Minister",
            "speaker_icon": "finance",
            "title": "The insurers walk away",
            "situation": (
                "Insurers have cancelled terrorism cover for the port, the hotels and the ships that call at "
                "{island}. Without insurance, ships won't dock and banks won't lend."
            ),
            "options": [
                {
                    "id": "backstop",
                    "title": "The government insures the big losses",
                    "icon": "🛡️",
                    "summary": "If there's another attack, the state pays above a set amount. Insurers come back.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 0.6, "currency": 1.0, "crowd": "mixed",
                              "quote": "\"So taxpayers carry the risk. Again.\""},
                    "levers": {"confidence": 0.3, "supply_push": -0.5},
                    "chain": [
                        "You promised to cover extreme losses",
                        "Insurers returned at sensible prices",
                        "Ships kept docking and banks kept lending",
                        "Taxpayers now carry a hidden risk if there's another attack",
                    ],
                    "history": "After 9/11, the US created a federal terrorism insurance backstop (TRIA). Britain has had Pool Re since 1993.",
                },
                {
                    "id": "force",
                    "title": "Order insurers to cover at the old price",
                    "icon": "📜",
                    "summary": "A new law: no cancelling, no price rises.",
                    "today": {"approval": 5, "reserves": 0.0, "debt": 0.0, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Good. Make them honour their promises.\""},
                    "levers": {"supply_push": 0.5, "credibility": -0.04},
                    "chain": [
                        "You ordered insurers to keep covering at old prices",
                        "Several insurers left {island} altogether",
                        "Cover got harder to find, and shipping costs still rose",
                    ],
                    "history": "After Hurricane Andrew in 1992, insurers fled Florida, and the state ended up running its own insurer of last resort.",
                },
                {
                    "id": "premiums",
                    "title": "Let premiums rise",
                    "icon": "📈",
                    "summary": "Insurers will come back at a higher price. Businesses pay it.",
                    "today": {"approval": -1, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Another cost passed on to us.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You let insurance prices rise",
                        "Cover came back, but at a price",
                        "Higher shipping and insurance costs showed up in shop prices",
                    ],
                    "history": "After big attacks, terrorism cover usually returns within a year or two, at higher prices.",
                },
            ],
        },
        company_card(island, "18:00"),
        {
            "id": "budget",
            "time": "20:00",
            "speaker": "Defence Minister",
            "speaker_icon": "security",
            "title": "Paying for safety",
            "situation": (
                "The Defence Minister wants a much bigger security budget: more police, more coastguard, more "
                "intelligence officers. How do you pay for it?"
            ),
            "options": [
                {
                    "id": "borrow",
                    "title": "Borrow for a big security build-up",
                    "icon": "🏗️",
                    "summary": "More of everything, paid for with new debt.",
                    "today": {"approval": 5, "reserves": 0.0, "debt": 2.5, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Whatever it takes to feel safe again.\""},
                    "levers": {"fiscal": 0.4, "confidence": 0.15},
                    "chain": [
                        "You borrowed to pay for security",
                        "New hiring gave the economy a small lift",
                        "Visitors and investors felt safer",
                        "The debt rose, and will need paying back",
                    ],
                    "history": "Israel has long spent over 4% of its GDP on defence. Its security is credible, but it's a permanent weight on the budget.",
                },
                {
                    "id": "security_tax",
                    "title": "A new security tax",
                    "icon": "🧾",
                    "summary": "Pay for it now with a tax on incomes, so the debt doesn't grow.",
                    "today": {"approval": -4, "reserves": 0.0, "debt": -0.5, "currency": 0.5, "crowd": "boo",
                              "quote": "\"Another tax? We've just been bombed!\""},
                    "levers": {"austerity": 0.4, "confidence": 0.15, "credibility": 0.03},
                    "chain": [
                        "You raised a tax to pay for security",
                        "People had less to spend, so demand cooled",
                        "The debt stayed under control",
                    ],
                    "history": "Britain introduced income tax in 1799 to pay for the war against Napoleon.",
                },
                {
                    "id": "print_security",
                    "title": "Print the money",
                    "icon": "💵",
                    "summary": "The central bank pays. No new debt, no new tax.",
                    "today": {"approval": 4, "reserves": 0.0, "debt": 0.0, "currency": -2.5, "crowd": "cheer",
                              "quote": "\"Free security! What's the catch?\""},
                    "levers": {"print_pct": 2.0, "credibility": -0.08},
                    "chain": [
                        "You printed money to pay for security",
                        "No tax rose and no debt was added",
                        "More money chased the same goods, so prices climbed",
                        "The {currency} weakened as trust slipped",
                    ],
                    "history": "The Union printed 'greenbacks' to fund the American Civil War. Prices in the North nearly doubled.",
                },
                {
                    "id": "reprioritise",
                    "title": "Move money from other budgets",
                    "icon": "🔀",
                    "summary": "A modest increase, paid for by trimming other spending.",
                    "today": {"approval": -1, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Fewer potholes fixed, then.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You shifted money from other budgets",
                        "Security improved a little",
                        "Nothing else changed much",
                    ],
                    "history": "Most countries absorb attacks without huge new budgets. Intelligence work is cheap compared with armies.",
                },
            ],
        },
    ], island)
