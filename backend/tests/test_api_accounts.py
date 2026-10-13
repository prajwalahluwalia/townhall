"""Accounts and saved games. Switched off for now (see app/main.py), so these tests are skipped."""

import os

import pytest

pytest.skip("accounts and saved games are switched off", allow_module_level=True)

os.environ["DATABASE_URL"] = os.environ.get("TEST_DATABASE_URL", "postgresql+psycopg://localhost/townhall_test")

from fastapi.testclient import TestClient  # noqa: E402

from app.db import Base, engine  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture()
def client():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    with TestClient(app) as c:
        yield c


def _register(client, name="governor"):
    r = client.post("/api/auth/register", json={"username": name, "email": f"{name}@example.com", "password": "secret123"})
    assert r.status_code == 201, r.text
    return {"Authorization": f"Bearer {r.json()['token']}"}


def test_register_login_and_me(client):
    _register(client)
    assert client.post("/api/auth/register", json={"username": "governor", "email": "x@example.com",
                                                   "password": "secret123"}).status_code == 409
    assert client.post("/api/auth/login", json={"username": "governor", "password": "nope-nope"}).status_code == 401
    r = client.post("/api/auth/login", json={"username": "governor@example.com", "password": "secret123"})
    assert r.status_code == 200
    me = client.get("/api/auth/me", headers={"Authorization": f"Bearer {r.json()['token']}"})
    assert me.json()["username"] == "governor"
    assert client.get("/api/auth/me").status_code == 401


def test_full_term_saves_decisions_and_report(client):
    h = _register(client)
    listing = client.get("/api/islands").json()
    assert len(listing["islands"]) == 5 and len(listing["scenarios"]) == 6
    game = client.post("/api/games", json={"island_id": "kalani", "scenario_id": "grey_fever"}, headers=h).json()
    assert game["scenario"]["id"] == "grey_fever" and "Kalani" in game["scenario"]["intro"]
    gid = game["id"]
    assert client.post(f"/api/games/{gid}/fast-forward", headers=h).status_code == 409
    while game["card"]:
        card = game["card"]
        r = client.post(f"/api/games/{gid}/decisions",
                        json={"card_id": card["id"], "option_id": card["options"][0]["id"]}, headers=h)
        assert r.status_code == 200, r.text
        game = r.json()["game"]
    assert len(game["decisions"]) == 7
    report = client.post(f"/api/games/{gid}/fast-forward", headers=h).json()
    assert report["ending"]["title"]
    assert client.get(f"/api/games/{gid}/report", headers=h).json()["score"] == report["score"]
    assert report["scenario"]["id"] == "grey_fever"
    games = client.get("/api/games", headers=h).json()
    assert games[0]["status"] == "completed" and games[0]["scenario_title"] == "The Grey Fever"


def test_cannot_touch_other_players_games(client):
    h1 = _register(client, "alice")
    h2 = _register(client, "bob")
    gid = client.post("/api/games", json={"island_id": "aurelia"}, headers=h1).json()["id"]
    assert client.get(f"/api/games/{gid}", headers=h2).status_code == 404


def test_rejects_out_of_order_decision(client):
    h = _register(client)
    gid = client.post("/api/games", json={"island_id": "aurelia"}, headers=h).json()["id"]
    r = client.post(f"/api/games/{gid}/decisions", json={"card_id": "rates", "option_id": "hold"}, headers=h)
    assert r.status_code == 409


def test_new_game_defaults_to_war_and_rejects_unknown_scenario(client):
    h = _register(client)
    game = client.post("/api/games", json={"island_id": "aurelia"}, headers=h).json()
    assert game["scenario"]["id"] == "strait_crisis" and game["card"]["id"] == "war"
    r = client.post("/api/games", json={"island_id": "aurelia", "scenario_id": "zombies"}, headers=h)
    assert r.status_code == 400
