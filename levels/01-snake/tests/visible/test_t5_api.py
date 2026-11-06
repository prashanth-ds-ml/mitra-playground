from snake import api


def test_state_reset_turn_step():
    status, body = api.handle("POST", "/api/reset", {})
    assert status == 200 and body["score"] == 0
    status, body = api.handle("GET", "/api/state", None)
    assert status == 200 and body["snake"][0] == [10, 10]
    status, _ = api.handle("POST", "/api/turn", {"direction": "down"})
    assert status == 200
    status, body = api.handle("POST", "/api/step", {})
    assert status == 200 and body["snake"][0] == [10, 11]


def test_bad_direction_is_400():
    api.handle("POST", "/api/reset", {})
    status, body = api.handle("POST", "/api/turn", {"direction": "nowhere"})
    assert status == 400 and "error" in body


def test_unknown_path_is_404():
    status, body = api.handle("GET", "/api/nope", None)
    assert status == 404 and "error" in body
