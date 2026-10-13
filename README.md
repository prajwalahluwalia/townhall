# Town Hall

An educational simulation game about inflation, money and trade. You pick an island and a crisis,
then govern it for one day. You make seven decisions, then the game fast-forwards two years and
shows what each decision actually caused.

- **Frontend:** React + Vite (`frontend/`): SVG island art, animations (framer-motion)
- **Backend:** Python FastAPI (`backend/`): auth, saved games, and the economic simulation
- **No accounts, no database:** the browser keeps the current game and the server rebuilds everything from
  the choices sent with each request. Login and saved games (PostgreSQL) are switched off; see
  `backend/app/main.py` to turn them back on.

## Run it

Prerequisites: Python 3.11+, Node 20+.

```bash
# backend
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --port 8000 --reload

# frontend, in another terminal
cd frontend && npm install && npm run dev
```

Open http://localhost:5173. Vite proxies `/api` to the backend on port 8000.

Tests: `cd backend && .venv/bin/python -m pytest -q` (the account tests are skipped while accounts are off).

## Deploy (Vercel)

One Vercel project serves both halves: the Vite build as static files, and FastAPI as a Python
function (`api/index.py`) behind `/api`. Config lives in `vercel.json` and the root `requirements.txt`.
Import the repo in Vercel with the Root Directory set to the repo root and deploy. No environment
variables or database are needed.

## How the game works

| Piece | File |
|---|---|
| Five islands (rich → very poor/UN-assisted) | `backend/app/game/islands.py` |
| Six crises, each with its own shock and seven decision cards | `backend/app/game/scenarios/` |
| Economic model, consequence map, headlines, ending | `backend/app/game/engine.py` |

Every island can face every crisis:

| Category | Scenario | How it hits the economy |
|---|---|---|
| War | The Strait Crisis (`war.py`) | Oil and grain prices jump |
| Pandemic | The Grey Fever (`pandemic.py`) | Spending collapses, supply chains break, oil gets cheap |
| Terrorism | Attack on the Harbour (`terror.py`) | Tourists and investors flee, insurance costs rise |
| Internal affairs | The Hidden Debt (`scandal.py`) | Hidden debt exposed, borrowing costs and protests surge |
| External affairs | The Tariff Wall (`trade_war.py`) | A trade war hits exports and makes imports dearer |
| Financial crisis | The Bank Run (`bank_run.py`) | Savers panic, lending freezes, money supply shrinks |

A scenario describes its crisis as a quarter-by-quarter `shock` (see `engine.simulate`), and can
change the island's starting point. Shared desks (the rate meeting, the island's biggest company,
the long-term plan) live in `scenarios/common.py`; the company's trouble is written per island and
per crisis in `islands.py`.

Each decision has an **instant reaction** (crowd, markets, treasury), shown right away, and
**levers** that drive the two-year simulation. Inflation is broken into its causes (expectations,
demand, fuel, food, a weaker currency, printed money, wages). This makes the report able to
show where the inflation came from.

The **consequence map** replays the simulation with each decision swapped for the
middle-of-the-road option. That measures what the single choice caused on its own, and the
same replay powers the "what if you'd chosen…" comparisons.

The report is rebuilt from the list of choices whenever it's asked for, so the server never needs
to store a game.
