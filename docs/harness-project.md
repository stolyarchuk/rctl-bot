# Project Harness

## Purpose

This repository contains a Python aiogram 3 bot that controls audio and power
functions on a Raspberry Pi 4.

## Structure

- `main.py` is the executable entrypoint.
- `rctl_bot/bot.py` creates the aiogram `Bot` and `Dispatcher`, registers bot
  commands and routers, and starts polling.
- `rctl_bot/config.py` loads pydantic settings and `.env`.
- `rctl_bot/commands.py` defines the fixed command argument mappings.
- `rctl_bot/filters.py` contains admin and private-chat filters.
- `rctl_bot/keyboards.py` builds Telegram reply keyboards.
- `rctl_bot/handlers/` contains routers and message handlers.
- `rctl_bot/services/` contains wrappers for side effects such as subprocesses.
- `tests/` verifies behavior without executing real Raspberry Pi controls.

## Development Commands

- Install or synchronize dependencies with `uv sync`.
- Run tests with `uv run pytest -q`.
- Check syntax and importability with
  `uv run python -m compileall rctl_bot main.py`.
- Copy `.env.example` to `.env`, configure it, and run the bot with
  `uv run python main.py`.

Keep these instructions synchronized with the live package layout and commands.
