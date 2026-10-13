"""Create the database tables once: `python -m app.init_db` (uses DATABASE_URL)."""
from .db import Base, engine
from . import models  # noqa: F401  (registers the tables on Base)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Tables ready:", ", ".join(sorted(Base.metadata.tables)))
