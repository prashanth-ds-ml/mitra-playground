"""Tests for scripts/check_level.py, using a tiny throwaway level."""
import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("check_level", ROOT / "scripts" / "check_level.py")
check_level = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_level)

TEST = """
from calc import add

def test_add():
    assert add(2, 3) == 5
"""


def make_level(tmp_path: Path, start_code: str, reference_code: str) -> Path:
    level = tmp_path / "99-toy"
    (level / "start").mkdir(parents=True)
    (level / "reference").mkdir()
    (level / "tests" / "visible").mkdir(parents=True)
    (level / "tests" / "hidden").mkdir(parents=True)
    (level / "level.toml").write_text('id = "L99"\ntitle = "Toy"\ntest_command = "python -m pytest -q tests"\n')
    (level / "plan.md").write_text("# Feature: add\n")
    (level / "start" / "calc.py").write_text(start_code)
    (level / "reference" / "calc.py").write_text(reference_code)
    (level / "tests" / "visible" / "test_visible.py").write_text(TEST)
    (level / "tests" / "hidden" / "test_hidden.py").write_text(TEST.replace("test_add", "test_add_hidden"))
    return level


def test_valid_level_passes(tmp_path):
    level = make_level(tmp_path, "def add(a, b):\n    return 0\n", "def add(a, b):\n    return a + b\n")
    assert check_level.check_level(level) is True


def test_level_already_solved_at_start_is_rejected(tmp_path):
    good = "def add(a, b):\n    return a + b\n"
    level = make_level(tmp_path, good, good)
    assert check_level.check_level(level) is False


def test_broken_reference_is_rejected(tmp_path):
    bad = "def add(a, b):\n    return 0\n"
    level = make_level(tmp_path, bad, bad)
    assert check_level.check_level(level) is False


def test_missing_folder_is_reported(tmp_path):
    level = make_level(tmp_path, "", "")
    (level / "plan.md").unlink()
    try:
        check_level.load_level(level)
    except ValueError as exc:
        assert "plan.md" in str(exc)
    else:
        raise AssertionError("missing plan.md was not reported")


def test_find_levels_handles_missing_folder(tmp_path):
    assert check_level.find_levels(tmp_path / "no-such-folder") == []
    make_level(tmp_path, "", "")
    assert [p.name for p in check_level.find_levels(tmp_path)] == ["99-toy"]


def test_hidden_tests_reach_the_workspace_but_reference_does_not_by_default(tmp_path):
    level = make_level(tmp_path, "x = 1\n", "x = 2\n")
    ws = tmp_path / "ws"
    check_level.build_workspace(level, ws, with_reference=False, with_hidden=False)
    assert (ws / "tests" / "test_visible.py").exists()
    assert not (ws / "tests" / "test_hidden.py").exists()
    assert (ws / "calc.py").read_text() == "x = 1\n"
