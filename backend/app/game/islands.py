"""Island archetypes the player can govern.

Each island starts from a different place on the development ladder. The same
decision plays out differently depending on how much trust, savings (reserves)
and dependence on imported fuel/food an island has. That contrast is a big
part of what the game teaches.
"""

ISLANDS: dict[str, dict] = {
    "aurelia": {
        "id": "aurelia",
        "name": "Aurelia",
        "tier": "rich",
        "tier_label": "Rich",
        "tagline": "Glass towers, private banks, and the world's savings.",
        "description": (
            "A wealthy financial hub. People trust its currency and it has deep savings, "
            "but it imports most of its fuel and food and its banks lent heavily abroad."
        ),
        "currency": "Aurelian Crown",
        "currency_code": "AUC",
        "population": "2.1 million",
        "gdp_per_capita": 68000,
        "start": {
            "inflation": 2.2, "unemployment": 4.0, "interest_rate": 3.0, "debt_to_gdp": 88.0,
            "reserves_months": 14.0, "currency_index": 100.0, "approval": 58.0, "environment": 68.0,
        },
        "credibility": 0.9,
        "neutral_rate": 1.5,
        "fuel_dependence": 0.55,
        "food_dependence": 0.6,
        "export_sensitivity": 0.4,
        "tourism_share": 0.15,
        "foreign_debt_share": 0.1,
        "company": {
            "name": "Aurelia Bank Group",
            "sector": "finance",
            "workers": "48,000",
            "health": 70,
            "crises": {
                "strait_crisis": "lent 30 billion crowns to Petra's oil companies, and those loans are now going bad",
                "grey_fever": "is sitting on billions in loans to hotels, airlines and shops that can no longer pay",
                "harbour_attack": "is facing withdrawals after rumours that the attackers moved money through its private bank",
                "hidden_debt": "holds billions in government bonds that lost a fifth of their value this morning",
                "tariff_wall": "has been warned by Aurum that it will lose access to ducats if it keeps serving Forge's companies",
                "bank_run": "is the bank everyone fears is next, and savers are queueing at its branches too",
            },
        },
        "un_eligible": False,
        "art": {"buildings": "towers", "palette": ["#e9c46a", "#2a9d8f", "#264653"], "size": 1.0},
    },
    "nordhaven": {
        "id": "nordhaven",
        "name": "Nordhaven",
        "tier": "developed",
        "tier_label": "Developed",
        "tagline": "Factories, engineers, and a strong welfare state.",
        "description": (
            "An industrial, developed island that exports machines and electric cars. "
            "It has solid institutions, but its factories run on imported energy."
        ),
        "currency": "Nordic Mark",
        "currency_code": "NDM",
        "population": "6.4 million",
        "gdp_per_capita": 47000,
        "start": {
            "inflation": 2.6, "unemployment": 5.0, "interest_rate": 3.5, "debt_to_gdp": 62.0,
            "reserves_months": 10.0, "currency_index": 100.0, "approval": 55.0, "environment": 62.0,
        },
        "credibility": 0.82,
        "neutral_rate": 1.75,
        "fuel_dependence": 0.6,
        "food_dependence": 0.35,
        "export_sensitivity": 0.7,
        "tourism_share": 0.1,
        "foreign_debt_share": 0.15,
        "company": {
            "name": "Nordhaven Motors",
            "sector": "manufacturing",
            "workers": "120,000",
            "health": 64,
            "crises": {
                "strait_crisis": "can't get parts and pay for energy at the same time, and is threatening to move its factories to Forge",
                "grey_fever": "has shut two assembly lines because parts from Forge stopped arriving and nobody is buying cars",
                "harbour_attack": "can't ship its cars because the bombed harbour handled most of its exports",
                "hidden_debt": "was promised big state contracts by the disgraced ministers, and those contracts are now frozen",
                "tariff_wall": "now faces a 35% tariff on every car it sells to Aurum, its biggest market",
                "bank_run": "can't renew its credit line now that banks have stopped lending",
            },
        },
        "un_eligible": False,
        "art": {"buildings": "factories", "palette": ["#8ecae6", "#219ebc", "#023047"], "size": 0.95},
    },
    "coralia": {
        "id": "coralia",
        "name": "Coralia",
        "tier": "developing",
        "tier_label": "Developing",
        "tagline": "Booming beaches, busy sewing floors, rising ambitions.",
        "description": (
            "A fast-growing developing island that earns money from tourism and clothing exports. "
            "Its middle class is growing quickly, but trust in its currency is still young."
        ),
        "currency": "Coral Peso",
        "currency_code": "CRP",
        "population": "14 million",
        "gdp_per_capita": 9800,
        "start": {
            "inflation": 5.0, "unemployment": 7.0, "interest_rate": 6.0, "debt_to_gdp": 52.0,
            "reserves_months": 6.0, "currency_index": 100.0, "approval": 52.0, "environment": 46.0,
        },
        "credibility": 0.58,
        "neutral_rate": 2.5,
        "fuel_dependence": 0.75,
        "food_dependence": 0.35,
        "export_sensitivity": 0.8,
        "tourism_share": 0.45,
        "foreign_debt_share": 0.35,
        "company": {
            "name": "Coralia Textiles",
            "sector": "manufacturing",
            "workers": "310,000",
            "health": 58,
            "crises": {
                "strait_crisis": "has lost a big order from Aurum buyers and can't pay its loans in Aurum ducats",
                "grey_fever": "has had every Aurum clothing order cancelled, and its crowded sewing floors are a health risk",
                "harbour_attack": "has lost its insurance at the port, so foreign buyers are cancelling clothing orders",
                "hidden_debt": "turns out to have been secretly backed by the hidden loans, and its lenders want their money back",
                "tariff_wall": "now faces a 35% tariff on its clothes in Aurum, and buyers are moving to cheaper islands",
                "bank_run": "kept its wage money at the failing bank and can't pay this month's salaries",
            },
        },
        "un_eligible": False,
        "art": {"buildings": "town", "palette": ["#ffb4a2", "#e5989b", "#6d6875"], "size": 0.85},
    },
    "terrava": {
        "id": "terrava",
        "name": "Terrava",
        "tier": "poor",
        "tier_label": "Poor",
        "tagline": "Green fields, dusty roads, and very little in the bank.",
        "description": (
            "A poor farming island. It grows much of its own food, but it imports nearly all "
            "its fuel and fertiliser, and people remember the last time prices ran wild."
        ),
        "currency": "Terran Shilling",
        "currency_code": "TRS",
        "population": "22 million",
        "gdp_per_capita": 2100,
        "start": {
            "inflation": 8.0, "unemployment": 11.0, "interest_rate": 9.0, "debt_to_gdp": 71.0,
            "reserves_months": 3.0, "currency_index": 100.0, "approval": 48.0, "environment": 40.0,
        },
        "credibility": 0.38,
        "neutral_rate": 3.0,
        "fuel_dependence": 0.88,
        "food_dependence": 0.2,
        "export_sensitivity": 0.6,
        "tourism_share": 0.15,
        "foreign_debt_share": 0.55,
        "company": {
            "name": "Terrava Farmers' Cooperative",
            "sector": "agriculture",
            "workers": "1.4 million",
            "health": 50,
            "crises": {
                "strait_crisis": "can't afford fertiliser now that fuel costs have doubled, so the next harvest is at risk",
                "grey_fever": "can't get its harvest to market because lockdowns closed the roads and the city markets",
                "harbour_attack": "has crops rotting in warehouses because the harbour, its only export route, is closed",
                "hidden_debt": "was counting on a government fertiliser credit that was paid for with the hidden debt",
                "tariff_wall": "has seen Aurum put tariffs on its coffee and cocoa, its main cash crops",
                "bank_run": "can't get its usual seasonal loans for seed and fertiliser because the banks have stopped lending",
            },
        },
        "un_eligible": True,
        "art": {"buildings": "village", "palette": ["#a3b18a", "#588157", "#3a5a40"], "size": 0.9},
    },
    "kalani": {
        "id": "kalani",
        "name": "Kalani",
        "tier": "very_poor",
        "tier_label": "Very poor · seeking UN help",
        "tagline": "Fishing boats, storm scars, and an open request to the UN.",
        "description": (
            "A very poor island that is still recovering from last year's hurricane. It depends on "
            "imports for almost everything and is already asking the United Nations for help."
        ),
        "currency": "Kalani Shell",
        "currency_code": "KLS",
        "population": "900,000",
        "gdp_per_capita": 850,
        "start": {
            "inflation": 12.0, "unemployment": 18.0, "interest_rate": 12.0, "debt_to_gdp": 108.0,
            "reserves_months": 1.5, "currency_index": 100.0, "approval": 44.0, "environment": 33.0,
        },
        "credibility": 0.22,
        "neutral_rate": 3.5,
        "fuel_dependence": 0.95,
        "food_dependence": 0.65,
        "export_sensitivity": 0.5,
        "tourism_share": 0.35,
        "foreign_debt_share": 0.75,
        "company": {
            "name": "Kalani Fisheries",
            "sector": "fishing",
            "workers": "60,000",
            "health": 42,
            "crises": {
                "strait_crisis": "has a fleet that can't afford diesel, so its boats are sitting in harbour",
                "grey_fever": "lost its export buyers overnight as foreign fish markets shut",
                "harbour_attack": "has its fleet stuck behind a security cordon in the harbour, unable to sail",
                "hidden_debt": "owes money to state banks that just lost access to foreign credit",
                "tariff_wall": "has been shut out of Aurum's market for tuna",
                "bank_run": "lost its working cash when its bank froze withdrawals",
            },
        },
        "un_eligible": True,
        "art": {"buildings": "huts", "palette": ["#90e0ef", "#00b4d8", "#03045e"], "size": 0.7},
    },
}

# The other islands in the world. They are not playable; they are trading partners and the
# source of shocks.
WORLD = [
    {"id": "petra", "name": "Petra", "role": "Oil & gas exporter", "exports": "Fuel"},
    {"id": "granara", "name": "Granara", "role": "Breadbasket", "exports": "Grain"},
    {"id": "forge", "name": "Forge", "role": "Factory of the world", "exports": "Electronics"},
    {"id": "aurum", "name": "Aurum", "role": "Reserve-currency banker", "exports": "Ducats & credit"},
]


def get_island(island_id: str) -> dict | None:
    return ISLANDS.get(island_id)


def public_islands() -> list[dict]:
    return list(ISLANDS.values())
