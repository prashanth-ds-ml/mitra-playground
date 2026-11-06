"""Hidden tests: edge cases of the rules in plan.md. Never shown to the builder."""
import pytest

from snake.game import Game


@pytest.mark.parametrize("seed", range(40))
def test_food_never_lands_on_the_snake(seed):
    g = Game(width=6, height=6, seed=seed)
    g.food = (4, 3)  # eat once, so new food is placed next to a longer snake
    g.step()
    assert g.food not in g.snake
    assert 0 <= g.food[0] < 6 and 0 <= g.food[1] < 6


def test_custom_size_start_position():
    g = Game(width=9, height=7, seed=1)
    assert g.snake == [(4, 3), (3, 3), (2, 3)]


@pytest.mark.parametrize("direction,turn_to,head", [
    ("up", "down", (10, 9)),
    ("down", "up", (10, 11)),
])
def test_reverse_is_ignored_in_every_direction(direction, turn_to, head):
    g = Game(seed=1)
    g.food = (0, 0)
    g.turn(direction)
    g.turn(turn_to)
    g.step()
    assert g.snake[0] == head


@pytest.mark.parametrize("turn", ["up", "down", "right"])
def test_every_wall_ends_the_game(turn):
    g = Game(seed=1)
    g.food = (0, 0)
    g.turn(turn)
    steps = 0
    while not g.over and steps < 30:
        g.step()
        steps += 1
    assert g.over is True
    head = g.snake[0]
    assert 0 <= head[0] < 20 and 0 <= head[1] < 20


def test_left_wall():
    g = Game(seed=1)
    g.food = (19, 19)
    g.turn("up")
    g.step()
    g.turn("left")
    for _ in range(30):
        g.step()
    assert g.over is True and g.snake[0] == (0, 9)


def test_running_into_own_body_ends_the_game():
    g = Game(seed=1)
    # grow to length 5 by feeding straight ahead
    for x in (11, 12):
        g.food = (x, 10)
        g.step()
    g.food = (0, 0)
    assert len(g.snake) == 5
    for d in ("up", "left", "down"):
        g.turn(d)
        g.step()
    assert g.over is True
    assert g.score == 2


def test_score_and_length_after_three_apples():
    g = Game(seed=5)
    for x in (11, 12, 13):
        g.food = (x, 10)
        g.step()
    assert g.score == 3 and len(g.snake) == 6
    assert g.state()["score"] == 3
    assert g.state()["snake"][0] == [13, 10]


def test_state_after_game_over_reports_over():
    g = Game(width=4, height=4, seed=1)
    g.food = (0, 0)
    for _ in range(6):
        g.step()
    assert g.state()["over"] is True
