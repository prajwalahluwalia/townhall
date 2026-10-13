from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from ..auth import create_token, current_user, hash_password, verify_password
from ..db import get_db
from ..models import User
from ..schemas import AuthOut, LoginIn, RegisterIn, UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


def _out(user: User) -> UserOut:
    return UserOut(id=user.id, username=user.username, email=user.email)


@router.post("/register", response_model=AuthOut, status_code=status.HTTP_201_CREATED)
def register(body: RegisterIn, db: Session = Depends(get_db)) -> AuthOut:
    clash = db.scalar(select(User).where(or_(User.username == body.username, User.email == body.email)))
    if clash:
        field = "username" if clash.username == body.username else "email"
        raise HTTPException(status.HTTP_409_CONFLICT, f"That {field} is already taken")
    user = User(username=body.username, email=body.email, password_hash=hash_password(body.password))
    db.add(user)
    db.commit()
    return AuthOut(token=create_token(user.id), user=_out(user))


@router.post("/login", response_model=AuthOut)
def login(body: LoginIn, db: Session = Depends(get_db)) -> AuthOut:
    ident = body.username.strip()
    user = db.scalar(select(User).where(or_(User.username == ident, User.email == ident.lower())))
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong username or password")
    return AuthOut(token=create_token(user.id), user=_out(user))


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)) -> UserOut:
    return _out(user)
