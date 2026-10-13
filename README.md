# Town Hall

An educational simulation game about inflation, money and trade. You govern an island for one
day while a war closes the world's main shipping strait. You make seven decisions, then the game
fast-forwards two years and shows what each decision actually caused.

- **Frontend:** React + Vite (`frontend/`): SVG island art, animations (framer-motion)
- **Backend:** Python FastAPI (`backend/`): auth, saved games, and the economic simulation
- **Database:** PostgreSQL: `users`, `games`, `decisions`

## Run it

Prerequisites: Python 3.11+, Node 20+, PostgreSQL running locally.

```bash
# one-time
createdb townhall
cd backend
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
cp .env.example .env            # then set a long random JWT_SECRET

# backend (tables are created on startup)
.venv/bin/uvicorn app.main:app --port 8000 --reload

# frontend, in another terminal
cd frontend && npm install && npm run dev
```

Open http://localhost:5173. Vite proxies `/api` to the backend on port 8000.

Tests (they use a separate `townhall_test` database: `createdb townhall_test`):

```bash
cd backend && .venv/bin/python -m pytest -q
```

## How the game works

| Piece | File |
|---|---|
| Five islands (rich → very poor/UN-assisted) | `backend/app/game/islands.py` |
| The seven decision cards for the "Strait Crisis" day | `backend/app/game/cards.py` |
| Economic model, consequence map, headlines, ending | `backend/app/game/engine.py` |

Each decision has an **instant reaction** (crowd, markets, treasury), shown right away, and
**levers** that drive the two-year simulation. Inflation is broken into its causes (expectations,
demand, fuel, food, a weaker currency, printed money, wages). This makes the report able to
show where the inflation came from.

The **consequence map** replays the simulation with each decision swapped for the
middle-of-the-road option. That measures what the single choice caused on its own, and the
same replay powers the "what if you'd chosen…" comparisons.

Every decision is saved to the `decisions` table as it is made, so a term can be resumed and
the report can always be rebuilt from the saved choices.
