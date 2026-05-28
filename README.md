Raspberry Pi control bot
========================

Telegram bot for controlling a Raspberry Pi from a private admin chat.

## Configuration

Create `.env` from `.env.example`:

```env
BOT_TOKEN=123456:replace-me
ADMIN_TELEGRAM_IDS=100000001,100000002
```

Only users listed in `ADMIN_TELEGRAM_IDS` can use the bot. Handlers also require a private chat.

## Actions

- `Volume up` -> `wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%+`
- `Volume down` -> `wpctl set-volume @DEFAULT_AUDIO_SINK@ 5%-`
- `Mute` -> `wpctl set-mute @DEFAULT_AUDIO_SINK@ toggle`
- `Poweroff` -> `systemctl poweroff`
- `Reboot` -> `systemctl reboot`

The bot registers slash commands for private chats and shows a two-row reply keyboard:

- `Volume up`, `Volume down`, `Mute`
- `Poweroff`, `Reboot`

## Run

```bash
uv run python main.py
```
