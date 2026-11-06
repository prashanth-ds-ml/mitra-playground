"""Run a builder on a level, then judge it with the hidden tests.

    python scripts/run_level.py levels/01-snake --builder mitra --model qwen3.5:4b

1. A fresh workspace gets start/, tests/visible/ (as tests/) and plan.md. Never reference/ or tests/hidden/.
2. The builder runs in that workspace (Mitra: `mitra solve --plan plan.md`, from ../05-mitra).
3. Only after the builder exits are the hidden tests copied in; the level's test command decides pass/fail.
4. A JSON result goes to results/<level>/<date>-<builder>-<model>.json; the workspace is kept for review.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MITRA = ROOT.parent / "05-mitra"


def build_workspace(level: Path, dest: Path) -> None:
    shutil.copytree(level / "start", dest, dirs_exist_ok=True)
    shutil.copytree(level / "tests" / "visible", dest / "tests", dirs_exist_ok=True)
    shutil.copy2(level / "plan.md", dest / "plan.md")


def run(cmd: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
                           encoding="utf-8", errors="replace")
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return -1, f"timed out after {timeout}s"


def test_counts(output: str) -> dict:
    import re
    last = output.strip().splitlines()[-1] if output.strip() else ""
    return {k: int(n) for n, k in re.findall(r"(\d+) (passed|failed|error)", last)} | {"line": last}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("level")
    ap.add_argument("--builder", default="mitra", choices=["mitra"])
    ap.add_argument("--model", default="qwen3.5:4b")
    ap.add_argument("--max-steps", type=int, default=30)
    ap.add_argument("--timeout", type=int, default=3600)
    args = ap.parse_args()

    level = (ROOT / args.level).resolve() if not Path(args.level).is_absolute() else Path(args.level)
    meta = tomllib.loads((level / "level.toml").read_text(encoding="utf-8"))
    ws = Path(tempfile.mkdtemp(prefix=f"run-{meta['id']}-"))
    build_workspace(level, ws)
    print(f"workspace: {ws}")

    t0 = time.monotonic()
    cmd = [sys.executable, "-m", "app.main", "solve", "--plan", str(ws / "plan.md"), "--test", meta["test_command"],
           "-w", str(ws), "--model", args.model, "--max-steps", str(args.max_steps)]
    code, out = run(cmd, MITRA, args.timeout)
    build_seconds = time.monotonic() - t0
    print(out[-6000:])

    _, visible_out = run([sys.executable, "-m", "pytest", "-q", "tests"], ws, 300)
    shutil.copytree(level / "tests" / "hidden", ws / "tests" / "hidden", dirs_exist_ok=True)
    _, full_out = run([sys.executable, "-m", "pytest", "-q", "tests"], ws, 300)
    visible, full = test_counts(visible_out), test_counts(full_out)
    passed = "failed" not in full and "error" not in full and full.get("passed", 0) > 0

    result = {"level": meta["id"], "builder": args.builder, "model": args.model,
              "date": time.strftime("%Y-%m-%d %H:%M"), "build_seconds": round(build_seconds),
              "builder_exit": code, "visible": visible, "visible_plus_hidden": full, "passed": passed,
              "workspace": str(ws)}
    out_dir = ROOT / "results" / meta["id"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{time.strftime('%Y%m%d-%H%M')}-{args.builder}-{args.model.replace(':', '-')}.json"
    runs = ws / ".mitra" / "runs"
    if runs.is_dir():  # keep the run records (scrubbed) for `mitra report` and the dashboard
        keep = ROOT / ".mitra" / "runs" / f"level-{meta['id']}-{out_file.stem}"
        shutil.copytree(runs, keep, dirs_exist_ok=True)
        result["records"] = str(keep.relative_to(ROOT))
    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"result: {out_file}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
