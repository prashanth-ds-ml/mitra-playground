from snake.game import Game


def test_hitting_the_right_wall_ends_the_game():
    g = Game(width=5, height=5, seed=1)
    g.food = (0, 0)
    for _ in range(5):
        g.step()
    assert g.over is True
    assert g.snake[0] == (4, 2)  # stayed on the last cell


def test_no_moves_after_game_over():
    g = Game(width=5, height=5, seed=1)
    g.food = (0, 0)
    for _ in range(10):
        g.step()
    snake = list(g.snake)
    g.step()
    assert g.snake == snake
