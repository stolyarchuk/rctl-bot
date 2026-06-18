# Startup Volume Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Set the default audio sink volume to 60% at bot startup without changing mute state or blocking startup on failure.

**Architecture:** Reuse the existing fixed argv command mapping and `CommandRunner`. A small startup helper runs the volume command, logs failures, and returns so normal mute-state initialization and polling continue.

**Tech Stack:** Python 3.13, aiogram 3, pytest, `wpctl`

---

### Task 1: Initialize startup volume

**Files:**
- Modify: `rctl_bot/commands.py`
- Modify: `rctl_bot/bot.py`
- Create: `tests/test_bot.py`

- [x] **Step 1: Write the failing test**

Add a fake command runner and assert that a failed startup command uses:

```python
("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "60%")
```

The helper must return normally and log the command failure.

- [x] **Step 2: Run the focused test**

Run: `uv run pytest -q tests/test_bot.py`

Expected: FAIL because the startup volume command/helper does not exist.

- [x] **Step 3: Write the minimal implementation**

Add the fixed argv tuple, then call it through `CommandRunner` before the existing
mute-state read. Log a nonzero result without raising.

- [x] **Step 4: Verify**

Run:

```text
uv run pytest -q
uv run python -m compileall rctl_bot main.py
```

Expected: all tests pass and compileall exits successfully.
