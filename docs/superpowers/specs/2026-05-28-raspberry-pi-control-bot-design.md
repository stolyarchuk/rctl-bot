# Raspberry Pi Control Bot Design

## Goal

Build an aiogram 3 Telegram bot that lets configured admins control Raspberry Pi volume, mute, poweroff, and reboot actions from a private chat keyboard.

## Requirements

- Load settings from environment variables and `.env`.
- Require `BOT_TOKEN`.
- Require one or more admin Telegram IDs in `ADMIN_TELEGRAM_IDS`.
- Ignore all non-admin users.
- Ignore group and supergroup chats.
- Register bot commands for private chats.
- Provide a reply keyboard with two rows:
  - `Volume up`, `Volume down`, `Mute`
  - `Poweroff`, `Reboot`
- Map actions to fixed system commands:
  - `wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+`
  - `wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-`
  - `wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle`
  - `systemctl poweroff`
  - `systemctl reboot`

## Architecture

The project follows the aiogram guide style with small modules for settings, filters, keyboards, handlers, services, and application startup. Handlers do not construct shell strings; they resolve button text to a predefined action and delegate execution to a service that calls `asyncio.create_subprocess_exec`.

The bot uses aiogram routers and filters. Admin-only and private-chat restrictions are enforced by filters on the controls router, so individual handlers stay small.

## Testing

Tests cover settings parsing, keyboard layout, admin/private filter behavior, command mapping, and command execution argument passing. Tests do not invoke real Raspberry Pi commands.
