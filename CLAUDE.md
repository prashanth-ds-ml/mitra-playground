# mitra-playground: rules for working in this repo

Practice ladder for Mitra (`../05-mitra`, decisions D-025..D-027 there). Each level = plan + tests + start files +
reference solution. Mitra builds levels with local models only; the hidden tests decide.

## Rules
- Discuss a level's plan with the user before writing its code.
- A level is ready only when `python scripts/check_level.py <level>` shows start fails and reference passes.
- `reference/` and `tests/hidden/` are never copied into a builder's workspace.
- Code written by Claude (reference solutions, scripts) is never training data for Mitra's fine-tune (D-022).
- API keys only in `.env` (never committed); only levels 05-06 use them, and Mitra never does (D-026).
- Python: shared root venv `../../.venv` (uv); install with `uv pip`, then `uv pip check`.
- GitHub: this repo pushes as `prashanth-ds-ml` (repo-local credential helper), whatever `gh` account is active.
- Scoreboard rows in README.md only from real runs, with the date.
