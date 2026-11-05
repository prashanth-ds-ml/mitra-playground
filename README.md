# mitra-playground

Practice projects for [Mitra](https://github.com/prashanth-ds-ml/mitra), a local coding assistant built for small
models. Each level is a small project with a plan and tests. Mitra (on local models only) tries to build it; the tests
decide. The levels get harder, so the scoreboard shows how far up the ladder a local model can climb.

> **Building in public.** Levels are added one at a time.

## The ladder
| Level | Project | Stack | Status |
|---|---|---|---|
| 01 | Snake game | Python game logic + browser (HTML canvas) front end | planned |
| 02 | Second arcade-style game (more state, collisions) | tbd | planned |
| 03 | Portfolio site | tbd | planned |
| 04 | API + database | FastAPI + SQLite, then Postgres | planned |
| 05 | AI app (chatbot / RAG) | uses OpenRouter or NVIDIA APIs at runtime | planned |
| 06 | Small full system (front end + API + DB + AI) | tbd | planned |

## Scoreboard
Filled in as runs happen. A level counts as passed only when the hidden tests pass.

| Level | Builder | Model | Visible tests | Hidden tests | Date |
|---|---|---|---|---|---|
| - | - | - | - | - | - |

## How a level is laid out
```
levels/01-snake/
  level.toml        id, title, test command
  plan.md           the feature, in the plan format (docs/PLAN_FORMAT.md)
  start/            files the builder starts from (may be nearly empty)
  tests/visible/    tests the builder can see and run
  tests/hidden/     tests that decide pass/fail; never given to the builder
  reference/        a known-good solution, used only to check the level itself
```
A run copies `start/` and `tests/visible/` into a fresh folder; the builder never sees `tests/hidden/` or `reference/`.

`reference/` code is written to prove each level is solvable. It is not used as training data for any model.

## Check the levels
```
python scripts/check_level.py --all
```
For every level: the start files must **fail** the tests and the reference solution must **pass** them. CI runs this on
every push.

## API keys (levels 05-06 only)
The apps in levels 05-06 call OpenRouter or NVIDIA models for their own AI features. Copy `.env.example` to `.env` and
fill in your keys. `.env` is never committed. Mitra itself only uses local models.

## Licence
MIT
