from snake.game import Game


def test_new_game_start_state():
    g = Game()
    assert (g.width, g.height) == (20, 20)
    assert g.snake == [(10, 10), (9, 10), (8, 10)]
    assert g.direction == "right"
    assert g.score == 0
    assert g.over is False


def test_food_is_on_the_board_and_not_on_the_snake():
    g = Game(seed=1)
    x, y = g.food
    assert 0 <= x < 20 and 0 <= y < 20
    assert g.food not in g.snake


def test_same_seed_same_food():
    assert Game(seed=7).food == Game(seed=7).food


def test_state_is_plain_json_data():
    g = Game(width=10, height=8, seed=3)
    s = g.state()
    assert s["width"] == 10 and s["height"] == 8
    assert s["snake"] == [[5, 4], [4, 4], [3, 4]]
    assert s["food"] == list(g.food)
    assert s["score"] == 0 and s["over"] is False and s["direction"] == "right"
