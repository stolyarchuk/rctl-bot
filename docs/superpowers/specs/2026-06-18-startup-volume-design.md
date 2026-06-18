# Startup Volume Design

## Behavior

On startup, run:

```text
wpctl set-volume @DEFAULT_AUDIO_SINK@ 60%
```

This changes only the volume level. The existing mute state remains unchanged.

If the command fails, log the error and continue starting the bot. Then read the
current mute state as before, register handlers, and begin polling.

## Implementation

Add one fixed argv tuple to `rctl_bot/commands.py` and execute it from
`rctl_bot/bot.py` through the existing `CommandRunner`. Do not add configuration,
shell command strings, or mute commands.

## Verification

Add one startup-focused test proving the 60% command runs and a failure returns
normally after logging the error.
Run:

```text
uv run pytest -q
uv run python -m compileall rctl_bot main.py
```
