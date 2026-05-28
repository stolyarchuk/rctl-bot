# Repository Guidelines

## Coding Rules

Always read `CLAUDE.md` before making code changes. Treat it as the source of coding rules and constraints for this repository: clarify assumptions, keep changes simple, make surgical edits, and verify work with concrete commands.

## Project Structure

This is a Python aiogram 3 Raspberry Pi control bot.

- `main.py` is the executable entrypoint.
- `rctl_bot/bot.py` wires settings, aiogram `Bot`, `Dispatcher`, command registration, and polling.
- `rctl_bot/handlers/` contains aiogram routers and message handlers.
- `rctl_bot/config.py` owns pydantic settings and `.env` loading.
- `rctl_bot/commands.py` keeps the fixed `wpctl` and non-interactive `sudo -n /usr/bin/systemctl` argv mappings.
- `rctl_bot/keyboards.py` builds reply keyboards.
- `rctl_bot/filters.py` contains admin/private-chat filters.
- `rctl_bot/services/` contains side-effecting service wrappers.
- `tests/` covers behavior without running real Raspberry Pi commands.

## Development Commands

- Install/sync dependencies through `uv`.
- Run tests with `uv run pytest -q`.
- Check syntax/importability with `uv run python -m compileall rctl_bot main.py`.
- Run the bot with `uv run python main.py` after creating `.env` from `.env.example`.

## Implementation Notes

Do not construct shell command strings for Raspberry Pi actions. Keep command execution as explicit argv tuples and call subprocesses without a shell.

Handlers must remain private-chat and admin-only. Do not add group-chat behavior unless explicitly requested.

Tests must not call real `wpctl`, `systemctl poweroff`, or `systemctl reboot`; monkeypatch command execution instead.
