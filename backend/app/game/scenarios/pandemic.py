"""Pandemic: a new virus spreads. Demand collapses, supply chains snap and oil prices crash."""

from .common import company_card, finalize, finance_option, rates_card

SCENARIO = {
    "id": "grey_fever",
    "category": "Pandemic",
    "icon": "🦠",
    "title": "The Grey Fever",
    "tagline": "A new virus spreads across the islands faster than anyone can count.",
    "intro": (
        "Overnight, the first Grey Fever patients arrive at {island}'s main hospital. Forge has shut its "
        "factories, Aurum has closed its airports, and cruise ships are turning around mid-ocean. Every "
        "decision you make today will echo through the next two years."
    ),
    "briefing": [
        "🏥 Hospitals will fill within weeks",
        "✈️ Tourists cancel and shoppers stay home",
        "📦 Factory parts and medicine stop arriving",
        "🛢️ Oil prices crash as the world stops travelling",
    ],
    "teaches": "Demand shocks: when people stop spending, the danger flips from rising prices to lost jobs.",
    "map": None,
    "status": {"active": "🦠 Fever spreading", "over": "💉 Vaccines arrive"},
    "causes": {
        "fuel": ["Fuel prices", "Nobody was travelling, so oil got cheap. A negative number means fuel pulled inflation down."],
        "food": ["Food prices", "Harvests were fine, but getting food to shops cost more."],
        "supply": ["Broken supply chains", "Factories abroad shut, so parts and goods were scarce and pricier."],
    },
    "news": {
        # one story per quarter while the crisis lasts, then the recovery
        "during": [
            "Streets empty as the Grey Fever spreads",
            "Hospitals stretched as cases peak",
            "Second wave: hospitals stretched again",
            "Vaccine trials enter their final stage",
            "Cases fall, but the island stays cautious",
        ],
        "end": "VACCINES ARRIVE: queues at clinics, shops reopen",
        "after": [
            "Restaurants full again as {island} celebrates",
            "Tourists trickle back to {island}'s beaches",
            "Factories abroad restart, and parts start arriving again",
            "Schools report pupils catching up on lost months",
            "Two years on: {island} counts the cost of the fever",
        ],
    },
    "shock": {
        "oil": [-35, -25, -10, 0, 5, 5, 0, 0],
        "grain": [5, 8, 5, 2, 0, 0, 0, 0],
        "risk": [3.0, 1.5, 0.8, 0.3, 0.0, 0.0, 0.0, 0.0],
        "demand": [-7.0, -4.5, -2.5, -1.0, 0.0, 0.0, 0.0, 0.0],
        "supply": [0.8, 1.4, 1.2, 0.7, 0.3, 0.0, 0.0, 0.0],
        "fiscal": [0.8, 0.6, 0.4, 0.2, 0.0, 0.0, 0.0, 0.0],
        "layoffs": [4.0, 2.8, 1.4, 0.6, 0.0, 0.0, 0.0, 0.0],
        "exposure": "all",
        "ends": 4,
    },
}


def cards(island: dict) -> list[dict]:
    return finalize([
        {
            "id": "health",
            "time": "08:00",
            "speaker": "Health Minister",
            "speaker_icon": "health",
            "title": "The wards are filling up",
            "situation": (
                "Cases are doubling every four days. Doctors say that without action, {island}'s hospitals will "
                "run out of beds within a month. Business owners are begging you not to shut the economy."
            ),
            "options": [
                {
                    "id": "lockdown",
                    "title": "Full lockdown",
                    "icon": "🔒",
                    "summary": "Everyone stays home except essential workers. The virus slows sharply, and so does the economy.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 0.5, "currency": -0.5, "crowd": "mixed",
                              "quote": "\"Safe, yes. But how do I pay rent with the shop shut?\""},
                    "levers": {"contain": 0.8, "drag_now": 2.0},
                    "chain": [
                        "You shut everything except essentials",
                        "Spending and jobs dropped hard for a few months",
                        "The virus slowed, so the outbreak was smaller and shorter",
                        "When the island reopened, it bounced back faster",
                    ],
                    "history": "New Zealand locked down hard and early in 2020. It had one of the lowest death rates in the world, and its economy rebounded quickly.",
                    "news": [[1, "bad", "Lockdown: {island}'s streets fall silent"]],
                },
                {
                    "id": "targeted",
                    "title": "Test, trace, and protect the elderly",
                    "icon": "🧪",
                    "summary": "Masks, mass testing and limits on crowds. Most businesses stay open with rules.",
                    "today": {"approval": 2, "reserves": -0.1, "debt": 0.6, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Masks on, shop open. I can live with that.\""},
                    "levers": {"contain": 0.4, "drag_now": 0.6},
                    "baseline": True,
                    "chain": [
                        "You fought the virus with testing and rules, not a shutdown",
                        "Some spending fell, but most businesses stayed open",
                        "The outbreak was slowed, but not stopped",
                    ],
                    "history": "South Korea relied on mass testing and contact tracing in 2020 and avoided a full national lockdown.",
                },
                {
                    "id": "stay_open",
                    "title": "Keep everything open",
                    "icon": "🚪",
                    "summary": "Let people decide for themselves. The economy keeps running and the virus spreads freely.",
                    "today": {"approval": -2, "reserves": 0.0, "debt": 0.0, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Business as usual. My grandmother is terrified.\""},
                    "levers": {"contain": -0.5},
                    "chain": [
                        "You kept the island open",
                        "At first, spending held up",
                        "The virus spread widely, so people stayed home out of fear anyway",
                        "The outbreak was bigger, and so was the damage to spending later",
                    ],
                    "history": "Sweden kept most of its economy open in 2020. Its economy shrank less than many, but its early death rate was far higher than Norway's or Finland's.",
                },
                {
                    "id": "borders",
                    "title": "Close the borders only",
                    "icon": "🛂",
                    "summary": "Nobody comes in or leaves. Life inside the island carries on.",
                    "today": {"approval": 5, "reserves": -0.3, "debt": 0.0, "currency": -1.0, "crowd": "cheer",
                              "quote": "\"Keep it out! We'll manage on our own.\""},
                    "levers": {"contain": 0.5, "trade": -0.4},
                    "chain": [
                        "You closed {island}'s borders",
                        "The virus arrived more slowly",
                        "Tourism and trade dried up completely",
                        "Hotels and ports lost a year of business",
                    ],
                    "history": "Australia shut its borders in March 2020 for almost two years. Cases stayed low, but tourism and universities lost billions.",
                },
            ],
        },
        {
            "id": "jobs",
            "time": "10:00",
            "speaker": "Labour Minister",
            "speaker_icon": "union",
            "title": "Nobody is going to work",
            "situation": (
                "Restaurants, hotels and shops are empty. Owners say they will have to fire staff by Friday "
                "unless someone helps pay the wages. The Labour Minister wants a decision now."
            ),
            "options": [
                {
                    "id": "furlough",
                    "title": "Pay 80% of wages for idle workers",
                    "icon": "🧾",
                    "summary": "The government pays most of the wage while workers stay home. Jobs are kept, debt rises.",
                    "today": {"approval": 8, "reserves": 0.0, "debt": 3.0, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"I still have a job to go back to. That's everything.\""},
                    "levers": {"job_protect": 0.8, "fiscal": 0.6},
                    "chain": [
                        "You paid most of the wages of idle workers",
                        "Firms kept their staff instead of firing them",
                        "Unemployment rose far less than it would have",
                        "The bill went onto the government's debt",
                    ],
                    "history": "Germany's Kurzarbeit and Britain's furlough scheme paid most workers' wages in 2020, so unemployment rose far less than in the US.",
                },
                {
                    "id": "cheques",
                    "title": "Send every adult a cheque",
                    "icon": "✉️",
                    "summary": "Cash for everyone, now. People decide what they need.",
                    "today": {"approval": 10, "reserves": -0.2, "debt": 2.5, "currency": -0.8, "crowd": "cheer",
                              "quote": "\"Money in my account! I'm ordering a new TV.\""},
                    "levers": {"fiscal": 1.0},
                    "chain": [
                        "You sent cash to every adult",
                        "Spending held up, even on things nobody urgently needed",
                        "Some firms still fired workers, because cheques don't keep a job open",
                        "When the island reopened, lots of spending met too few goods, and prices rose",
                    ],
                    "history": "The US sent stimulus cheques to most adults in 2020–21. Spending recovered fast, and so did inflation in 2021–22.",
                },
                {
                    "id": "print_fund",
                    "title": "Print money to pay for it all",
                    "icon": "💵",
                    "summary": "The central bank creates new {currency}s to fund wages and handouts. No new debt.",
                    "today": {"approval": 9, "reserves": 0.0, "debt": 0.0, "currency": -3.0, "crowd": "cheer",
                              "quote": "\"No debt, no taxes? Sounds too good to be true.\""},
                    "levers": {"print_pct": 3.0, "job_protect": 0.4, "credibility": -0.1},
                    "chain": [
                        "You printed new money to pay wages",
                        "Jobs were protected without adding to the debt",
                        "While the island was locked down, the new money mostly sat in bank accounts",
                        "When spending came back, the extra money pushed prices up and weakened the {currency}",
                    ],
                    "history": "Argentina's central bank printed money to fund its 2020 pandemic spending. Inflation passed 50% the next year.",
                    "news": [[3, "bad", "Shoppers return, and find prices much higher"]],
                },
                {
                    "id": "loans",
                    "title": "Cheap loans for businesses",
                    "icon": "🏦",
                    "summary": "State-backed loans that firms must repay. Some will use them to keep staff.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 1.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Another loan? I can barely pay the last one.\""},
                    "levers": {"job_protect": 0.3, "fiscal": 0.2},
                    "baseline": True,
                    "chain": [
                        "You offered state-backed loans to businesses",
                        "Some firms used them to keep staff",
                        "Others fired workers anyway and saved the cash",
                        "Unemployment still rose, though less than with no help",
                    ],
                    "history": "Many governments offered state-guaranteed business loans in 2020. Some firms survived on them; others borrowed and failed later.",
                },
            ],
        },
        rates_card("12:00", (
            "Spending has collapsed and oil is cheap, so prices are falling in some shops. Banks are nervous "
            "about lending to anyone."
        ), {
            "hold": {"summary": "Wait and see how deep the slump goes before moving."},
            "cut": {
                "levers": {"rate_change": -1.0, "job_protect": 0.4},
                "today": {"approval": 5, "reserves": -0.2, "debt": 0.0, "currency": -1.0, "crowd": "cheer",
                          "quote": "\"Cheaper loans! Maybe the shop can hang on.\""},
                "summary": "Make loans cheaper so businesses survive the slump. With people staying home, the extra money won't spill into prices yet.",
                "history": "In March 2020, central banks cut rates to near zero within weeks to keep businesses alive.",
            },
            "hike_small": {"levers": {"rate_change": 1.0}},
            "hike_big": {
                "levers": {"rate_change": 3.0, "credibility": 0.03},
                "history": "Raising rates in a slump is rare. When the US Fed tightened too soon in 1937, the economy fell back into depression.",
            },
        }),
        {
            "id": "supplies",
            "time": "14:00",
            "speaker": "Trade Minister",
            "speaker_icon": "trade",
            "title": "Empty shelves at the pharmacy",
            "situation": (
                "Masks, painkillers and soap have sold out. Every island is scrambling for the same supplies, "
                "and some sellers have tripled their prices. People are panic-buying rice too."
            ),
            "options": [
                {
                    "id": "export_ban",
                    "title": "Ban exports of masks, medicine and rice",
                    "icon": "🚫",
                    "summary": "Keep everything made on {island} at home. Trading partners will be furious.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 0.0, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Our masks, for our people!\""},
                    "levers": {"trade": -0.3, "supply_push": 0.3},
                    "chain": [
                        "You banned exports of medicine and food",
                        "Local shelves filled up a little",
                        "Other islands banned exports to {island} in return",
                        "Supplies you couldn't make yourself got even scarcer",
                    ],
                    "history": "In 2020, dozens of countries banned exports of masks and medicine, and Vietnam briefly restricted rice exports. Others hit back.",
                },
                {
                    "id": "price_cap",
                    "title": "Cap prices on essentials",
                    "icon": "🔒",
                    "summary": "Anyone charging more than last month's price for masks, soap or staples is fined.",
                    "today": {"approval": 8, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"No more profiteers! Fair prices for everyone!\""},
                    "levers": {"price_cap": True},
                    "chain": [
                        "You capped prices on essentials",
                        "Prices on the shelf stayed low",
                        "Sellers had no reason to bring in more stock, so shelves emptied",
                        "Goods moved to a black market at even higher prices",
                    ],
                    "history": "Price-gouging laws in 2020 kept masks cheap on paper, but shelves stayed empty for weeks in many places.",
                    "news": [[2, "bad", "Price-capped soap vanishes from shelves, appears on black market"]],
                },
                {
                    "id": "joint_buy",
                    "title": "Keep trade open and buy jointly",
                    "icon": "🤝",
                    "summary": "Team up with Aurum and Forge to buy in bulk. No bans, no caps.",
                    "today": {"approval": 1, "reserves": -0.3, "debt": 0.3, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Sharing with other islands? While we're short?\""},
                    "levers": {"supply_push": -0.6, "credibility": 0.03},
                    "chain": [
                        "You kept trade open and bought supplies jointly",
                        "Buying in bulk got better prices and faster deliveries",
                        "Supply chains healed sooner, so prices settled faster",
                    ],
                    "history": "The EU bought vaccines and equipment jointly in 2020 so its smaller members weren't outbid.",
                },
                {
                    "id": "market",
                    "title": "Let the market sort it out",
                    "icon": "🤷",
                    "summary": "High prices will draw in new supply. You do nothing.",
                    "today": {"approval": -5, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"Ten times the price for a mask? Shameful.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You left prices to the market",
                        "Prices spiked and the poorest went without",
                        "High prices drew in new supply within a few months",
                    ],
                    "history": "Mask and hand-gel prices tripled in early 2020, then fell back as factories ramped up.",
                },
            ],
        },
        {
            "id": "vaccine",
            "time": "16:00",
            "speaker": "Chief Scientist",
            "speaker_icon": "scientist",
            "title": "The vaccine race",
            "situation": (
                "Two labs in Aurum and Forge say a vaccine will be ready within a year. Rich islands are already "
                "paying for their place in the queue. Where does {island} stand?"
            ),
            "options": [
                {
                    "id": "preorder",
                    "title": "Pay top price to jump the queue",
                    "icon": "💉",
                    "summary": "Pre-order millions of doses at a premium. Expensive, but {island} gets them first.",
                    "today": {"approval": 6, "reserves": -0.8, "debt": 1.5, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"We'll be first in line? Thank goodness.\""},
                    "levers": {"shorten": 1},
                    "chain": [
                        "You paid a premium to get vaccines early",
                        "{island} was vaccinated a season before most islands",
                        "Shops, hotels and offices reopened sooner",
                        "The bill came out of reserves and added to the debt",
                    ],
                    "history": "Israel paid well above the going price for early doses in late 2020 and vaccinated faster than any other country.",
                    "news": [[2, "good", "{island} among first islands to vaccinate"]],
                },
                {
                    "id": "sharing",
                    "title": "Join the global sharing scheme",
                    "icon": "🌍",
                    "summary": "Pay a fair share into a pool that splits doses between all islands.",
                    "today": {"approval": 0, "reserves": -0.2, "debt": 0.3, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Fair is fair. But when do *we* get ours?\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You joined the sharing scheme",
                        "It was cheap, but doses arrived after the rich islands had theirs",
                        "The outbreak ran its normal course",
                    ],
                    "history": "COVAX aimed to share vaccines fairly in 2021, but rich countries' pre-orders meant poorer countries waited much longer.",
                },
                {
                    "id": "skip",
                    "title": "Skip vaccines and let immunity build",
                    "icon": "🎲",
                    "summary": "Save the money. Most people will catch it and recover.",
                    "today": {"approval": -6, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"So we just... wait to get sick?\""},
                    "levers": {"contain": -0.3, "shorten": -1},
                    "chain": [
                        "You decided not to buy vaccines",
                        "The virus kept circulating long after other islands reopened",
                        "Fear kept tourists and shoppers away for months longer",
                    ],
                    "history": "Countries that vaccinated slowly in 2021 faced extra waves and stayed closed to tourists for longer.",
                },
            ],
        },
        company_card(island, "18:00"),
        {
            "id": "bill",
            "time": "20:00",
            "speaker": "Finance Minister",
            "speaker_icon": "finance",
            "title": "Who pays for all this?",
            "situation": (
                "The fever has cost {island} a fortune: hospitals, wages, loans and lost taxes. The Finance "
                "Minister wants a plan for the bill before the markets start asking."
            ),
            "options": [
                {
                    "id": "wealth_tax",
                    "title": "A one-off tax on the richest",
                    "icon": "💎",
                    "summary": "Those with the biggest fortunes pay a one-time levy to cover the crisis.",
                    "today": {"approval": 4, "reserves": 0.0, "debt": -1.5, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"About time the yacht owners chipped in.\""},
                    "levers": {"austerity": 0.4, "credibility": 0.03},
                    "chain": [
                        "You taxed the largest fortunes once",
                        "The debt grew more slowly",
                        "Some wealthy people moved money abroad, which weighed on the {currency}",
                        "Spending by the rich cooled a little",
                    ],
                    "history": "Argentina passed a one-off tax on large fortunes in December 2020 to pay for its pandemic response.",
                },
                finance_option(island),
                {
                    "id": "inflate",
                    "title": "Let inflation shrink the debt",
                    "icon": "🫠",
                    "summary": "Keep rates low and let rising prices make the old debt smaller in real terms.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 0.0, "currency": -2.0, "crowd": "mixed",
                              "quote": "\"So my savings pay for it. Clever.\""},
                    "levers": {"print_pct": 1.5, "credibility": -0.08},
                    "chain": [
                        "You let inflation do the work",
                        "Prices rose faster than interest rates",
                        "The debt shrank compared to the size of the economy",
                        "Savers quietly paid the bill as their money lost value",
                    ],
                    "history": "After World War II, Britain and the US let low rates and inflation shrink their war debts over decades.",
                },
                {
                    "id": "later",
                    "title": "Worry about it later",
                    "icon": "⏳",
                    "summary": "The crisis isn't over. Pay the bill when times are better.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Fine by me. Someone else's problem.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You put off paying for the crisis",
                        "The debt stayed high",
                        "{island} faces the next crisis with less room to spend",
                    ],
                    "history": "Most countries left their pandemic debts in place after 2021. Higher interest rates later made them costlier.",
                },
            ],
        },
    ], island)
