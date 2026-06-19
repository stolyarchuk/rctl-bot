# Coding and Safety Harness

## Command Execution

- Represent Raspberry Pi actions as explicit argument tuples.
- Run subprocesses without a shell. Do not construct shell command strings.
- Keep audio control based on `wpctl`.
- Keep power actions non-interactive:
  `sudo -n /usr/bin/systemctl poweroff` and
  `sudo -n /usr/bin/systemctl reboot`.
- Do not add arbitrary command execution or user-controlled command arguments.

## Telegram Access

- Handlers must remain private-chat and admin-only.
- Do not add group-chat behavior or broaden authorization unless explicitly
  requested.
- Preserve the persistent controls keyboard unless the requested behavior
  requires changing it.

## Tests

- Tests must never execute real `wpctl`, poweroff, or reboot commands.
- Monkeypatch command execution and assert the expected argument tuples.
- Add or update focused tests when behavior changes.

## Change Boundaries

- Match the existing project style.
- Touch only files and lines required by the task.
- Remove only imports, variables, or functions made obsolete by the current
  change.
- Mention unrelated problems instead of fixing them without authorization.
