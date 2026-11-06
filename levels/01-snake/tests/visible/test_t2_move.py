import pytest

from snake.game import Game


def new_game():
    g = Game(seed=1)
    g.food = (0, 0)  # out of the way
    return g


def test_step_moves_right_and_keeps_length():
    g = new_game()
    g.step()
    assert g.snake == [(11, 10), (10, 10), (9, 10)]


def test_turn_up_then_step():
    g = new_game()
    g.turn("up")
    g.step()
    assert g.snake[0] == (10, 9)
    assert g.direction == "up"


def test_turning_straight_back_is_ignored():
    g = new_game()
    g.turn("left")
    g.step()
    assert g.direction == "right"
    assert g.snake[0] == (11, 10)


def test_unknown_direction_raises():
    with pytest.raises(ValueError):
        new_game().turn("sideways")
