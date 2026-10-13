"""Financial crisis: a big bank collapses, savers panic, and lending freezes. The money supply shrinks."""

from .common import company_card, finalize, rates_card

SCENARIO = {
    "id": "bank_run",
    "category": "Financial crisis",
    "icon": "🏦",
    "title": "The Bank Run",
    "tagline": "A big bank's bad loans come to light. Savers queue to get their money out.",
    "intro": (
        "Overnight, the {island} Savings Bank admitted that a third of its property loans will never be "
        "repaid. By sunrise, the queues outside its branches stretch round the block, and savers at other "
        "banks are starting to join them. Every decision you make today will echo through the next two years."
    ),
    "briefing": [
        "🏧 Savers are emptying their accounts",
        "🔒 Banks have stopped lending to anyone",
        "🏠 House prices are falling",
        "📉 Less lending means less new money is being created",
    ],
    "teaches": "Money and banks: most money is created by lending, so when banks panic, money itself shrinks.",
    "map": None,
    "status": {"active": "🏦 Banks frozen", "over": "💳 Lending restarts"},
    "causes": {},
    "news": {
        # one story per quarter while the crisis lasts, then the recovery
        "during": [
            "Queues outside the {island} Savings Bank stretch round the block",
            "Savers stash cash under mattresses and buy gold",
            "\"Nobody can get a loan,\" say shopkeepers as credit dries up",
            "House prices slide for another quarter",
            "Withdrawals slow as the fear fades",
        ],
        "end": "Panic over: deposits flow back and banks start lending again",
        "after": [
            "First new mortgages in a year approved",
            "Bank shares recover half their losses",
            "Two years on: {island}'s banks are open for business",
        ],
    },
    "shock": {
        "risk": [3.0, 2.0, 1.2, 0.6, 0.2, 0.0, 0.0, 0.0],
        "demand": [-3.0, -4.0, -3.0, -1.8, -0.8, 0.0, 0.0, 0.0],
        "credit": [-12, -10, -7, -4, -1, 0, 0, 0],
        "layoffs": [1.2, 2.2, 2.2, 1.4, 0.6, 0.0, 0.0, 0.0],
        "exposure": None,
        "ends": 5,
        "start": {"approval": -2.0, "currency_index": -2.0},
    },
}


def cards(island: dict) -> list[dict]:
    return finalize([
        {
            "id": "deposits",
            "time": "08:00",
            "speaker": "Deputy Governor",
            "speaker_icon": "banker",
            "title": "Queues at the cash machines",
            "situation": (
                "Savers have pulled a tenth of all deposits out of {island}'s banks since dawn. Even healthy "
                "banks could fall if this goes on, because no bank keeps all its deposits as cash. "
                "The Deputy Governor wants a statement before the branches open at nine."
            ),
            "options": [
                {
                    "id": "guarantee_all",
                    "title": "Guarantee every deposit, in full",
                    "icon": "🛡️",
                    "summary": "The government promises that nobody will lose a single {currency}, at any bank.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 3.0, "currency": 1.0, "crowd": "cheer",
                              "quote": "\"My savings are safe? Then I'll leave them where they are.\""},
                    "levers": {"contain": 1.0, "confidence": 0.3},
                    "chain": [
                        "You guaranteed every deposit in full",
                        "The queues vanished, because nobody needed to rush",
                        "Banks stopped bleeding cash and slowly started lending again",
                        "Taxpayers took on the risk of every bank's mistakes",
                    ],
                    "history": "Ireland guaranteed all its banks' debts in 2008. The panic stopped, but the bill later forced it into an EU–IMF bailout.",
                },
                {
                    "id": "guarantee_limit",
                    "title": "Guarantee savings up to a limit",
                    "icon": "🧮",
                    "summary": "Every saver is safe up to 100,000. Anything above that is at risk.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 1.0, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Under the limit? Fine. My boss is still queueing.\""},
                    "levers": {"contain": 0.4},
                    "baseline": True,
                    "chain": [
                        "You guaranteed ordinary savers up to a limit",
                        "Most people stopped panicking",
                        "Big depositors still pulled money out, so lending stayed tight",
                    ],
                    "history": "Most countries insure deposits up to a limit, like the US FDIC's $250,000, so ordinary savers never need to panic.",
                },
                {
                    "id": "bank_holiday",
                    "title": "Close the banks for a week",
                    "icon": "🚫",
                    "summary": "A bank holiday. Nobody can withdraw anything until things calm down.",
                    "today": {"approval": -8, "reserves": 0.0, "debt": 0.0, "currency": -1.5, "crowd": "boo",
                              "quote": "\"I can't buy groceries! My money is locked in there!\""},
                    "levers": {"contain": 0.5, "drag_now": 1.5, "credibility": -0.05},
                    "chain": [
                        "You shut the banks",
                        "The run stopped, but nobody could pay for anything",
                        "Shops and businesses lost a week of sales",
                        "People learned the banks could lock up their money",
                    ],
                    "history": "Cyprus shut its banks for two weeks in 2013 and limited withdrawals for two years.",
                    "news": [[1, "bad", "Banks shut: cash-only economy as savers locked out"]],
                },
                {
                    "id": "nothing",
                    "title": "Let the run play out",
                    "icon": "🤷",
                    "summary": "Weak banks should fail. Strong ones will survive.",
                    "today": {"approval": -5, "reserves": 0.0, "debt": 0.0, "currency": -1.5, "crowd": "boo",
                              "quote": "\"So it's every saver for themselves?\""},
                    "levers": {"contain": -0.5},
                    "chain": [
                        "You let the bank run continue",
                        "Healthy banks were dragged down along with weak ones",
                        "Lending froze almost completely, so the money supply shrank",
                        "Spending and jobs fell much further",
                    ],
                    "history": "From 1930 to 1933, the US let thousands of banks fail. The money supply shrank by a third and the Depression deepened.",
                    "news": [[2, "bad", "Two more banks fail as panic spreads"]],
                },
            ],
        },
        {
            "id": "rescue",
            "time": "10:00",
            "speaker": "Finance Minister",
            "speaker_icon": "finance",
            "title": "What to do with the {island} Savings Bank?",
            "situation": (
                "The {island} Savings Bank will run out of cash by Friday. Its shareholders want a rescue. "
                "Taxpayers are furious at the idea. The Finance Minister has four plans."
            ),
            "options": [
                {
                    "id": "nationalise",
                    "title": "Nationalise it",
                    "icon": "🏛️",
                    "summary": "The government takes over the bank. Shareholders lose everything; savers are safe.",
                    "today": {"approval": 4, "reserves": 0.0, "debt": 4.0, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"Good. The bankers get nothing.\""},
                    "levers": {"contain": 0.3},
                    "chain": [
                        "You took the bank into public ownership",
                        "Shareholders were wiped out, but savers were protected",
                        "The bank's bad loans landed on the government's books",
                    ],
                    "history": "Britain nationalised Northern Rock in 2008, after the first UK bank run in over 140 years.",
                },
                {
                    "id": "bail_in",
                    "title": "Make big depositors share the loss",
                    "icon": "✂️",
                    "summary": "Shareholders and anyone with more than 100,000 in the bank take a cut.",
                    "today": {"approval": 3, "reserves": 0.0, "debt": 0.0, "currency": -1.0, "crowd": "mixed",
                              "quote": "\"Ordinary people protected, rich savers pay. Fair, I suppose.\""},
                    "levers": {"contain": 0.2, "confidence": -0.1, "credibility": 0.04},
                    "chain": [
                        "You made big depositors take a loss",
                        "Taxpayers paid nothing",
                        "Businesses that kept wages in the bank were hurt",
                        "Big savers elsewhere moved money abroad, just in case",
                    ],
                    "history": "In 2013, Cyprus made large depositors at its biggest bank take losses of nearly half.",
                },
                {
                    "id": "bailout",
                    "title": "Bail it out, owners and all",
                    "icon": "🖨️",
                    "summary": "The central bank creates money to buy the bad loans. The bank carries on as before.",
                    "today": {"approval": -4, "reserves": 0.0, "debt": 0.0, "currency": -2.0, "crowd": "boo",
                              "quote": "\"Heads they win, tails we lose.\""},
                    "levers": {"print_pct": 2.0, "contain": 0.4, "credibility": -0.08},
                    "chain": [
                        "You printed money to rescue the bank and its owners",
                        "The bank survived and kept lending",
                        "Other banks learned they'd be rescued too, so they'd take more risks",
                        "The new money weakened the {currency}",
                    ],
                    "history": "Bank rescues in 2008 that protected owners and bonuses fuelled years of public anger.",
                },
                {
                    "id": "merge",
                    "title": "Sell it to a healthy rival",
                    "icon": "🔗",
                    "summary": "A stronger bank takes it over this weekend, with a government guarantee on the worst loans.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 1.0, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Same branch, new name. Whatever works.\""},
                    "levers": {"contain": 0.2},
                    "baseline": True,
                    "chain": [
                        "You arranged a rescue merger",
                        "The bank's customers moved to a stronger bank",
                        "Taxpayers took on some of the risk through the guarantee",
                    ],
                    "history": "In 2023, Credit Suisse was folded into UBS over a single weekend, backed by Swiss government guarantees.",
                },
            ],
        },
        rates_card("12:00", (
            "Banks have stopped lending, so far less new money is being created. Prices could start falling, "
            "which makes debts harder to repay."
        ), {
            "hold": {"summary": "Rates aren't the problem; trust is. You wait."},
            "cut": {
                "levers": {"rate_change": -1.0, "job_protect": 0.4},
                "today": {"approval": 5, "reserves": -0.2, "debt": 0.0, "currency": -1.0, "crowd": "cheer",
                          "quote": "\"Cheaper loans! Maybe the shop can hang on.\""},
                "summary": "Make borrowing cheaper so banks and businesses can breathe while lending is frozen.",
                "chain": [
                    "You cut interest rates",
                    "Cheaper loans eased the pressure on borrowers",
                    "Banks slowly found it worth lending again",
                    "The {currency} weakened a little",
                ],
                "history": "In 2008, central banks cut rates to near zero to fight the credit freeze.",
            },
            "hike_small": {"levers": {"rate_change": 1.0}},
            "hike_big": {
                "levers": {"rate_change": 3.0, "credibility": 0.03},
                "history": "In 1931, the US Fed raised rates during a banking panic to defend gold. Thousands more banks failed.",
            },
        }),
        {
            "id": "homes",
            "time": "14:00",
            "speaker": "Housing Minister",
            "speaker_icon": "planner",
            "title": "Homeowners can't pay",
            "situation": (
                "House prices have fallen 15% and people are losing jobs. Thousands of families are behind on "
                "their mortgages, and banks want to repossess homes to get some money back."
            ),
            "options": [
                {
                    "id": "holiday",
                    "title": "A mortgage payment holiday",
                    "icon": "🏠",
                    "summary": "Families can pause payments for six months without losing their home.",
                    "today": {"approval": 7, "reserves": 0.0, "debt": 0.5, "currency": 0.0, "crowd": "cheer",
                              "quote": "\"We get to keep the house. Thank you.\""},
                    "levers": {"job_protect": 0.2, "contain": 0.15, "fiscal": 0.15},
                    "chain": [
                        "You let families pause their mortgages",
                        "Fewer homes were repossessed",
                        "Families kept spending on other things",
                        "Banks waited longer for their money",
                    ],
                    "history": "Many countries let borrowers pause mortgage payments in 2020. It prevented a wave of repossessions.",
                },
                {
                    "id": "bad_bank",
                    "title": "A 'bad bank' buys the worst loans",
                    "icon": "🗑️",
                    "summary": "A state company takes the bad loans off banks' hands, so they can lend again.",
                    "today": {"approval": 1, "reserves": 0.0, "debt": 2.5, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"So the bad debt becomes our debt.\""},
                    "levers": {"contain": 0.4},
                    "chain": [
                        "You set up a 'bad bank' for the worst loans",
                        "Banks' books were cleaned up, so they could lend again",
                        "The state took on the losses, and slowly sold the houses later",
                    ],
                    "history": "Sweden's 'bad bank' cleaned up its banking crisis in 1992–93, and the state eventually got most of its money back.",
                },
                {
                    "id": "repossess",
                    "title": "Let banks repossess",
                    "icon": "🔑",
                    "summary": "Contracts are contracts. Banks can take the homes.",
                    "today": {"approval": -5, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "boo",
                              "quote": "\"Twenty years in that house.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You let repossessions go ahead",
                        "Families lost homes, and house prices fell further",
                        "Neighbourhoods and local spending took years to recover",
                    ],
                    "history": "In the US after 2008, millions of homes were repossessed. Neighbourhoods and spending took years to recover.",
                },
            ],
        },
        {
            "id": "qe",
            "time": "16:00",
            "speaker": "Chief Economist",
            "speaker_icon": "scientist",
            "title": "Should the central bank print?",
            "situation": (
                "With banks not lending, the money in the economy is shrinking. The Chief Economist proposes "
                "that the central bank creates new money to buy government bonds and pump cash into the system."
            ),
            "options": [
                {
                    "id": "big_qe",
                    "title": "Create money on a huge scale",
                    "icon": "🖨️",
                    "summary": "Buy bonds worth 3% of the economy. Fill the hole that frozen lending left.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.0, "currency": -0.8, "crowd": "mixed",
                              "quote": "\"Printing money? Isn't that how Zimbabwe happened?\""},
                    "levers": {"print_pct": 3.0, "contain": 0.2},
                    "chain": [
                        "The central bank created money to buy bonds",
                        "It replaced some of the money the banks had stopped creating",
                        "With lending frozen, prices barely rose",
                        "Borrowing got cheaper across the economy",
                    ],
                    "history": "The US, UK and euro area created trillions after 2008. With banks barely lending, inflation stayed low for a decade.",
                },
                {
                    "id": "small_qe",
                    "title": "A small dose",
                    "icon": "💊",
                    "summary": "Buy bonds worth 1% of the economy and see what happens.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": -0.5, "crowd": "mixed",
                              "quote": "\"A little bit of printing. OK.\""},
                    "levers": {"print_pct": 1.0},
                    "chain": [
                        "The central bank created a little money",
                        "It helped at the edges",
                    ],
                    "history": "Japan tried small rounds of money creation in the early 2000s, with modest effect.",
                },
                {
                    "id": "no_qe",
                    "title": "No printing",
                    "icon": "✋",
                    "summary": "Creating money is dangerous. Let the system heal by itself.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Sound money. Good.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "The central bank created no new money",
                        "The money supply kept shrinking while banks weren't lending",
                    ],
                    "history": "In the early 1930s, central banks refused to create money while banks failed. The money supply collapsed.",
                },
            ],
        },
        company_card(island, "18:00"),
        {
            "id": "rules",
            "time": "20:00",
            "speaker": "Planning Minister" if not island["un_eligible"] else "UN Envoy",
            "speaker_icon": "planner" if not island["un_eligible"] else "envoy",
            "title": "Never again",
            "situation": (
                "The panic will pass, but it can happen again. You can sign one new rule for {island}'s banks "
                "tonight."
            ),
            "options": [
                {
                    "id": "capital",
                    "title": "Banks must hold far more of their own money",
                    "icon": "🧱",
                    "summary": "Banks have to fund more of their loans with shareholders' money, not just deposits.",
                    "today": {"approval": 2, "reserves": 0.0, "debt": 0.0, "currency": 0.5, "crowd": "mixed",
                              "quote": "\"Sounds technical. Does it stop this happening?\""},
                    "levers": {"credibility": 0.06, "credit": -0.8},
                    "chain": [
                        "You made banks hold more capital",
                        "Each bank could take bigger losses without failing",
                        "Lending grew a little more slowly",
                    ],
                    "history": "After 2008, the Basel III rules made banks hold much more capital. Most banks got through 2020 without bailouts.",
                },
                {
                    "id": "insurance_fund",
                    "title": "A deposit insurance fund, paid by banks",
                    "icon": "🏦",
                    "summary": "Banks pay into a fund that protects savers next time.",
                    "today": {"approval": 3, "reserves": 0.0, "debt": -0.5, "currency": 0.5, "crowd": "cheer",
                              "quote": "\"Let the banks pay for their own safety net.\""},
                    "levers": {"credibility": 0.04, "credit": -0.3},
                    "chain": [
                        "You made banks fund deposit insurance",
                        "Savers trusted the system again",
                        "Banks passed a small cost on to borrowers",
                    ],
                    "history": "The US FDIC, set up in 1933, is funded by banks. After it began, bank runs almost vanished for 75 years.",
                },
                {
                    "id": "break_up",
                    "title": "Break up the biggest banks",
                    "icon": "🔨",
                    "summary": "Split everyday banking from risky investing so no bank is too big to fail.",
                    "today": {"approval": 6, "reserves": 0.0, "debt": 0.0, "currency": -0.5, "crowd": "cheer",
                              "quote": "\"Cut them down to size!\""},
                    "levers": {"credibility": 0.02, "credit": -0.5},
                    "chain": [
                        "You split up the biggest banks",
                        "Savers' money was walled off from risky bets",
                        "Lending was a bit more expensive while banks reorganised",
                    ],
                    "history": "The US Glass–Steagall Act (1933) separated everyday banking from investment banking for 66 years.",
                },
                {
                    "id": "postpone",
                    "title": "Postpone it",
                    "icon": "⏳",
                    "summary": "Fix the crisis first. New rules can wait.",
                    "today": {"approval": 0, "reserves": 0.0, "debt": 0.0, "currency": 0.0, "crowd": "mixed",
                              "quote": "\"Until the next time, then.\""},
                    "levers": {},
                    "baseline": True,
                    "chain": [
                        "You put off new rules",
                        "Banks went back to business as usual",
                    ],
                    "history": "Banking rules are often loosened again once memories of a crisis fade.",
                },
            ],
        },
    ], island)
