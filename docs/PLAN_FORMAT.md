# Plan format (v0)

One Markdown file per feature. Mitra writes it with `/plan` (local model) or a person writes it by hand; `mitra run`
works through the tasks in order. The same format is used in every level's `plan.md`. Kept small on purpose: a 4-9B
model has to read it and write it.

```markdown
# Feature: <one line>

## Goal
<2-5 lines: what the finished feature does, for whom>

## Design notes
- <decisions the tasks rely on: file layout, data shapes, names>

## Tasks

### T1: <short title>
- Files: <paths the task creates or changes>
- Do: <what to build, 1-4 lines>
- Done when: `<test command>` passes
- Needs: -            (or the task ids this one depends on, e.g. T1, T2)

### T2: ...
```

## Rules
- Every task has a **Done when** line with a command that runs on its own. No command, no task.
- One task = one small change a small model can finish: ideally 1-2 files and under ~100 lines.
- **Needs** lists only earlier tasks. If a task fails, the tasks that need it are skipped.
- Design notes hold the facts every task shares (names, data shapes), so a task never has to guess them.

Version history: v0 2026-11-05 (first draft; Mitra M3 may refine it).
