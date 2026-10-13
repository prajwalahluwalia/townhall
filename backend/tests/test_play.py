def _start(client, island="kalani", scenario="grey_fever"):
    return {"island_id": island, "scenario_id": scenario, "decisions": []}


def test_full_game_without_an_account(client):
    listing = client.get("/api/islands").json()
    assert len(listing["islands"]) == 5 and len(listing["scenarios"]) == 6
    body = _start(client)
    game = client.post("/api/play", json=body).json()
    assert game["scenario"]["id"] == "grey_fever" and "Kalani" in game["scenario"]["intro"]
    assert client.post("/api/play/report", json=body).status_code == 409
    while game["card"]:
        card = game["card"]
        r = client.post("/api/play/decide", json={**body, "card_id": card["id"], "option_id": card["options"][0]["id"]})
        assert r.status_code == 200, r.text
        body["decisions"].append([card["id"], card["options"][0]["id"]])
        game = r.json()["game"]
        assert r.json()["reaction"] == game["decisions"][-1]["reaction"]
    assert game["status"] == "day_over" and len(game["decisions"]) == 7
    report = client.post("/api/play/report", json=body).json()
    assert report["ending"]["title"] and report["scenario"]["id"] == "grey_fever"
    # Nothing is stored: the same choices always give the same report.
    assert client.post("/api/play/report", json=body).json()["score"] == report["score"]


def test_rejects_unknown_island_scenario_and_out_of_order_choices(client):
    assert client.post("/api/play", json={**_start(client), "island_id": "atlantis"}).status_code == 400
    assert client.post("/api/play", json={**_start(client), "scenario_id": "zombies"}).status_code == 400
    body = _start(client, "aurelia", "strait_crisis")
    assert client.post("/api/play/decide", json={**body, "card_id": "rates", "option_id": "hold"}).status_code == 409
    assert client.post("/api/play", json={**body, "decisions": [["rates", "hold"]]}).status_code == 400
    assert client.post("/api/play", json={**body, "decisions": [["war", "nonsense"]]}).status_code == 400
