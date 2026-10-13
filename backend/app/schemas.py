import re

from pydantic import BaseModel, Field, field_validator

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=40)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)

    @field_validator("username")
    @classmethod
    def _username(cls, v: str) -> str:
        v = v.strip()
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", v):
            raise ValueError("Use letters, numbers, dots, dashes or underscores")
        return v

    @field_validator("email")
    @classmethod
    def _email(cls, v: str) -> str:
        v = v.strip().lower()
        if not _EMAIL_RE.match(v):
            raise ValueError("Enter a valid email address")
        return v


class LoginIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: int
    username: str
    email: str


class AuthOut(BaseModel):
    token: str
    user: UserOut


class NewGameIn(BaseModel):
    island_id: str
    scenario_id: str = "strait_crisis"


class DecisionIn(BaseModel):
    card_id: str
    option_id: str
