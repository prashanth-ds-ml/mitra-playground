from snake.game import Game


def test_eating_grows_the_snake_and_scores():
    g = Game(seed=1)
    g.food = (11, 10)  # right in front of the head
    g.step()
    assert g.snake == [(11, 10), (10, 10), (9, 10), (8, 10)]
    assert g.score == 1


def test_new_food_after_eating_is_free():
    g = Game(seed=2)
    g.food = (11, 10)
    g.step()
    assert g.food != (11, 10)
    assert g.food not in g.snake
