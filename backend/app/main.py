# from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import CORS_ORIGINS
from .routers import play

# Accounts and saved games are switched off for now: nobody logs in and nothing is stored.
# To bring them back, uncomment these lines (and the two routers below), and set DATABASE_URL and
# JWT_SECRET again.
# from .db import Base, engine
# from .routers import auth, game
#
#
# @asynccontextmanager
# async def lifespan(_: FastAPI):
#     Base.metadata.create_all(engine)
#     yield


app = FastAPI(title="Town Hall")  # add lifespan=lifespan with the database
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(play.router)
# app.include_router(auth.router)
# app.include_router(game.router)


@app.get("/api/health")
def health() -> dict:
    return {"ok": True}
