# Feature: Snake game (Python game logic + browser canvas front end)

## Goal
A classic Snake game. All rules live in a small Python module that is fully tested; a tiny HTTP API exposes the game
as JSON; a single HTML page draws it on a canvas and sends arrow-key turns. Standard library only.

## Design notes
- Grid: `width` x `height` cells, default 20 x 20. A cell is a tuple `(x, y)`; `(0, 0)` is the top-left corner,
  x grows to the right, y grows downwards.
- Directions are the strings `"up"`, `"down"`, `"left"`, `"right"`. Moves: up = (0, -1), down = (0, 1),
  left = (-1, 0), right = (1, 0).
- `snake/game.py` has `class Game(width=20, height=20, seed=None)` with attributes:
  `snake` (list of cells, head first), `direction` (str), `food` (cell), `score` (int), `over` (bool).
- A new game: snake of length 3 in the middle row, head at `(width // 2, height // 2)`, body to its left,
  direction `"right"`, score 0, not over, food on a random free cell.
- Food uses `random.Random(seed)` stored as `self.rng`, so a seed gives the same food every time.
  Tests may also set `game.food` directly.
- `snake/api.py` has `handle(method, path, body)` returning `(status_code, dict)`; it keeps one module-level `Game`.
- `serve.py` serves `web/` and forwards `/api/...` to `handle`. `web/index.html` draws the game on a `<canvas>`.

## Tasks

### T1: New game state
- Files: `snake/__init__.py`, `snake/game.py`
- Do: create the `Game` class with the start state from the design notes, a `place_food()` method that puts food
  on a random free cell (using `self.rng`), and `state()` returning
  `{"width", "height", "snake": [[x, y], ...], "food": [x, y], "score", "over", "direction"}`.
- Done when: `python -m pytest -q tests/test_t1_state.py` passes
- Needs: -

### T2: Moving and turning
- Files: `snake/game.py`
- Do: `turn(direction)` changes the direction, except that turning straight back (e.g. "left" while moving "right")
  is ignored; unknown directions raise `ValueError`. `step()` moves the head one cell in the direction and drops the
  tail, so the length stays the same.
- Done when: `python -m pytest -q tests/test_t2_move.py` passes
- Needs: T1

### T3: Eating and growing
- Files: `snake/game.py`
- Do: when the new head lands on the food, the snake keeps its tail (grows by 1), `score` goes up by 1 and new food
  is placed on a free cell.
- Done when: `python -m pytest -q tests/test_t3_food.py` passes
- Needs: T2

### T4: Game over
- Files: `snake/game.py`
- Do: moving into a wall or into the snake's own body sets `over = True` and leaves the snake where it was.
  `step()` does nothing once the game is over.
- Done when: `python -m pytest -q tests/test_t4_over.py` passes
- Needs: T3

### T5: JSON API
- Files: `snake/api.py`
- Do: `handle(method, path, body)`: `GET /api/state` returns the state; `POST /api/turn` with `{"direction": ...}`
  turns (400 with `{"error": ...}` for a bad or missing direction, `body` may be `None`); `POST /api/step` steps;
  `POST /api/reset` starts a new default game. Every successful call returns `(200, game.state())`.
  Any other method or path returns 404 with `{"error": ...}`.
- Done when: `python -m pytest -q tests/test_t5_api.py` passes
- Needs: T4

### T6: Browser front end
- Files: `web/index.html`, `serve.py`
- Do: `web/index.html` has a `<canvas id="board">`, polls `/api/state`, sends `POST /api/step` on a timer and
  `POST /api/turn` on arrow keys, and draws the snake, the food and the score. `serve.py` runs a `http.server` on
  port 8000 that serves `web/` and passes `/api/...` requests to `snake.api.handle`.
- Done when: `python -m pytest -q tests/test_t6_web.py` passes
- Needs: T5
