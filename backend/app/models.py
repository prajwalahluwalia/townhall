from datetime import datetime, timezone

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base

JsonType = JSON().with_variant(JSONB(), "postgresql")


def _now() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(40), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    games: Mapped[list["Game"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Game(Base):
    """One term in office: a player governing one island through one scenario."""

    __tablename__ = "games"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    island_id: Mapped[str] = mapped_column(String(40))
    scenario_id: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), default="in_office")  # in_office | completed
    current_step: Mapped[int] = mapped_column(Integer, default=0)
    live_stats: Mapped[dict] = mapped_column(JsonType)
    result: Mapped[dict | None] = mapped_column(JsonType, nullable=True)
    score: Mapped[int | None] = mapped_column(Integer, nullable=True)
    ending: Mapped[str | None] = mapped_column(String(80), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now, onupdate=_now)

    user: Mapped[User] = relationship(back_populates="games")
    decisions: Mapped[list["Decision"]] = relationship(
        back_populates="game", cascade="all, delete-orphan", order_by="Decision.step"
    )


class Decision(Base):
    """A single choice the player made. The simulation is replayed from these."""

    __tablename__ = "decisions"
    __table_args__ = (UniqueConstraint("game_id", "step"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id", ondelete="CASCADE"), index=True)
    step: Mapped[int] = mapped_column(Integer)
    card_id: Mapped[str] = mapped_column(String(40))
    option_id: Mapped[str] = mapped_column(String(40))
    reaction: Mapped[dict] = mapped_column(JsonType)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=_now)

    game: Mapped[Game] = relationship(back_populates="decisions")
