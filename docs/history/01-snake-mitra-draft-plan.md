# Feature: Snake game level implementation

## Goal
Implement a playable Snake game level with snake movement, food collection, and collision detection for testing game mechanics.

## Design notes
- Game state stored in `game_state.json` with snake position (list of coordinates), food position, and score
- Snake moves one cell per tick; food spawns randomly on empty grid cells
- Collision detected when snake head touches food or self
- Grid size: 20x20 cells, each cell is 1 unit

## Tasks

### T1: Create game state structure
- Files: `game_state.json`, `snake.py`
- Do: Define Snake class with position tracking and movement logic; create initial game state file
- Done when: `python -c "from snake import Snake; s = Snake(); print(s.position)"` outputs coordinates
- Needs:

### T2: Implement food spawning
- Files: `snake.py`, `game_state.json`
- Do: Add random food placement that avoids snake body; update game state on spawn
- Done when: `python -c "from snake import Snake; s = Snake(); s.spawn_food(); print(s.food_position)"` shows valid position
- Needs: T1

### T3: Implement movement and collision detection
- Files: `snake.py`, `game_state.json`
- Do: Add move() method that updates snake position; detect collisions with food or self
- Done when: `python -c "from snake import Snake; s = Snake(); s.move(); print(s.position)"` shows updated position
- Needs: T1, T2

### T4: Create level configuration
- Files: `level_config.json`, `game_state.json`
- Do: Define level parameters (grid size, initial score); initialize game state from config
- Done when: `python -c "import json; c = json.load('level_config.json'); print(c['grid_size'])"` outputs 20
- Needs: T1

### T5: Write integration tests
- Files: `tests/test_snake.py`
- Do: Test snake movement, food collection, and collision detection scenarios
- Done when: `pytest tests/test_snake.py -v` passes all tests
- Needs: T1, T2, T3, T4
