# Raspberry Pi Control Bot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an aiogram 3 bot that lets configured Telegram admins control Raspberry Pi volume, mute, poweroff, and reboot from private chat.

**Architecture:** Create a small package split into settings, filters, keyboards, handlers, services, commands, and app startup. Handlers use fixed command mappings and delegate subprocess execution to a service, keeping shell access auditable and testable.

**Tech Stack:** Python 3.13, aiogram 3, pydantic-settings, python-dotenv, pytest.

---

### Task 1: Tests For Bot Contract

**Files:**
- Create: `tests/test_settings.py`
- Create: `tests/test_keyboard.py`
- Create: `tests/test_filters.py`
- Create: `tests/test_commands.py`
- Create: `tests/test_command_runner.py`

- [ ] **Step 1: Write failing tests**

Add tests for comma-separated admin ID parsing, the two-row keyboard layout, admin/private filters, action command mappings, and subprocess argument passing.

- [ ] **Step 2: Run tests to verify they fail**

Run: `uv run python -m pytest -q`

Expected: FAIL because the `rctl_bot` package does not exist yet.

### Task 2: Core Package

**Files:**
- Create: `rctl_bot/config.py`
- Create: `rctl_bot/commands.py`
- Create: `rctl_bot/keyboards.py`
- Create: `rctl_bot/filters.py`
- Create: `rctl_bot/services/command_runner.py`
- Create: `rctl_bot/services/__init__.py`
- Create: `rctl_bot/__init__.py`

- [ ] **Step 1: Implement minimal code**

Create the settings model, fixed action mappings, keyboard factory, filters, and command runner needed by the tests.

- [ ] **Step 2: Run tests to verify they pass**

Run: `uv run python -m pytest -q`

Expected: PASS.

### Task 3: Aiogram Startup And Handlers

**Files:**
- Create: `rctl_bot/handlers/__init__.py`
- Create: `rctl_bot/handlers/controls.py`
- Create: `rctl_bot/bot.py`
- Modify: `main.py`
- Modify: `pyproject.toml`
- Modify: `README.md`
- Create: `.env.example`

- [ ] **Step 1: Add bot entrypoint**

Wire `Bot`, `Dispatcher`, router registration, private command registration, `/start`, and control-button handlers.

- [ ] **Step 2: Add dependencies and docs**

Add aiogram, pydantic-settings, python-dotenv, and pytest to `pyproject.toml`. Document the `.env` variables and Raspberry Pi command prerequisites.

- [ ] **Step 3: Verify**

Run: `uv run python -m pytest -q`

Run: `uv run python -m compileall rctl_bot main.py`

Expected: both commands exit 0.
