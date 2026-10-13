import os
from pathlib import Path


def _load_dotenv() -> None:
    env_file = Path(__file__).resolve().parent.parent / ".env"
    if not env_file.exists():
        return
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_dotenv()

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+psycopg://localhost/townhall")
# Hosted Postgres (Neon, Render, Supabase) hands out postgres:// URLs; point them at psycopg 3.
for _prefix in ("postgres://", "postgresql://"):
    if DATABASE_URL.startswith(_prefix):
        DATABASE_URL = "postgresql+psycopg://" + DATABASE_URL[len(_prefix):]
SERVERLESS = bool(os.environ.get("VERCEL"))
JWT_SECRET = os.environ.get("JWT_SECRET", "dev-only-secret-change-me-in-production-please")
# Only needed while accounts are switched on (see app/main.py):
# if SERVERLESS and "JWT_SECRET" not in os.environ:
#     raise RuntimeError("Set JWT_SECRET in the Vercel project's environment variables")
JWT_ALGORITHM = "HS256"
JWT_TTL_HOURS = int(os.environ.get("JWT_TTL_HOURS", "72"))
CORS_ORIGINS = [o.strip() for o in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
