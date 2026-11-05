"""Check that each playground level is valid.

For every level: the start files must FAIL the full tests (visible + hidden), and the reference solution must PASS
them. Each check runs in a fresh temp folder, the same way a builder run would see the level.

Usage:
    python scripts/check_level.py --all
    python scripts/check_level.py levels/01-snake
"""
from __future__ import annotations

import argparse
import shlex
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEVELS = ROOT / "levels"
TIMEOUT_S = 300


def load_level(level_dir: Path) -> dict:
    meta = tomllib.loads((level_dir / "level.toml").read_text(encoding="utf-8"))
    for key in ("id", "title", "test_command"):
        if key not in meta:
            raise ValueError(f"{level_dir.name}: level.toml is missing '{key}'")
    for sub in ("start", "tests/visible", "tests/hidden", "reference"):
        if not (level_dir / sub).is_dir():
            raise ValueError(f"{level_dir.name}: missing folder '{sub}'")
    if not (level_dir / "plan.md").is_file():
        raise ValueError(f"{level_dir.name}: missing plan.md")
    return meta


def build_workspace(level_dir: Path, dest: Path, *, with_reference: bool, with_hidden: bool) -> None:
    """Lay out a workspace the way a run does: start/ files, then tests; optionally the reference on top."""
    shutil.copytree(level_dir / "start", dest, dirs_exist_ok=True)
    if with_reference:
        shutil.copytree(level_dir / "reference", dest, dirs_exist_ok=True)
    shutil.copytree(level_dir / "tests" / "visible", dest / "tests", dirs_exist_ok=True)
    if with_hidden:
        shutil.copytree(level_dir / "tests" / "hidden", dest / "tests", dirs_exist_ok=True)


def run_tests(command: str, cwd: Path) -> tuple[bool, str]:
    args = shlex.split(command)
    if args and args[0] == "python":
        args[0] = sys.executable  # same interpreter as this script (the shared venv locally, CI's Python in CI)
    try:
        proc = subprocess.run(args, cwd=cwd, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return False, f"timed out after {TIMEOUT_S}s"
    out = (proc.stdout + proc.stderr).strip().splitlines()
    return proc.returncode == 0, out[-1] if out else ""


def check_level(level_dir: Path) -> bool:
    meta = load_level(level_dir)
    ok = True
    for label, with_reference, should_pass in (("start", False, False), ("reference", True, True)):
        with tempfile.TemporaryDirectory(prefix=f"mp-{meta['id']}-") as tmp:
            ws = Path(tmp)
            build_workspace(level_dir, ws, with_reference=with_reference, with_hidden=True)
            passed, last = run_tests(meta["test_command"], ws)
        good = passed == should_pass
        ok &= good
        want = "pass" if should_pass else "fail"
        print(f"  {'ok ' if good else 'BAD'} {label:<9} should {want}, did {'pass' if passed else 'fail'}  ({last})")
    return ok


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("levels", nargs="*", type=Path, help="level folders to check")
    parser.add_argument("--all", action="store_true", help="check every folder in levels/")
    args = parser.parse_args(argv)

    dirs = sorted(p for p in LEVELS.iterdir() if (p / "level.toml").exists()) if args.all else args.levels
    if not dirs:
        print("no levels to check")
        return 0 if args.all else 2

    all_ok = True
    for level_dir in dirs:
        print(f"{level_dir.name}")
        try:
            all_ok &= check_level(level_dir)
        except ValueError as exc:
            print(f"  BAD {exc}")
            all_ok = False
    print("all levels ok" if all_ok else "some levels are broken")
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
