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
    assert len(client.get("/api/islands").json()["islands"]) == 5
    game = client.post("/api/games", json={"island_id": "kalani"}, headers=h).json()
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
    games = client.get("/api/games", headers=h).json()
    assert games[0]["status"] == "completed"


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
