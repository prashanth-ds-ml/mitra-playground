"""Hidden tests for the JSON API. Never shown to the builder."""
from snake import api


def test_reset_gives_a_fresh_game_after_play():
    api.handle("POST", "/api/reset", {})
    for _ in range(3):
        api.handle("POST", "/api/step", {})
    _, body = api.handle("POST", "/api/reset", {})
    assert body["snake"][0] == [10, 10] and body["score"] == 0 and body["over"] is False


def test_turn_without_body_is_400():
    api.handle("POST", "/api/reset", {})
    status, body = api.handle("POST", "/api/turn", None)
    assert status == 400 and "error" in body


def test_wrong_method_is_404():
    status, _ = api.handle("DELETE", "/api/state", None)
    assert status == 404


def test_state_has_every_field():
    api.handle("POST", "/api/reset", {})
    _, body = api.handle("GET", "/api/state", None)
    assert set(body) >= {"width", "height", "snake", "food", "score", "over", "direction"}


def test_turn_returns_the_new_direction():
    api.handle("POST", "/api/reset", {})
    status, body = api.handle("POST", "/api/turn", {"direction": "up"})
    assert status == 200 and body["direction"] == "up"
