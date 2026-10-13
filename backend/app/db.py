from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy.pool import NullPool

from .config import DATABASE_URL, SERVERLESS

if SERVERLESS:
    # Each function instance is short-lived, so let Supabase's pooler hold the connections.
    # Its transaction mode (port 6543) can't keep prepared statements, so psycopg must not make them.
    engine = create_engine(DATABASE_URL, poolclass=NullPool, connect_args={"prepare_threshold": None})
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Iterator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
