import asyncio
from types import SimpleNamespace

import pytest

from rctl_bot.services.command_runner import CommandResult, CommandRunner


class FakeProcess:
    returncode = 0

    async def communicate(self) -> tuple[bytes, bytes]:
        return b"ok\n", b""


def test_command_runner_executes_argv_without_shell(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = []

    async def fake_create_subprocess_exec(*argv, stdout, stderr):
        calls.append((argv, stdout, stderr))
        return FakeProcess()

    monkeypatch.setattr(asyncio, "create_subprocess_exec", fake_create_subprocess_exec)

    result = asyncio.run(CommandRunner().run(("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle")))

    assert calls == [
        (
            ("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"),
            asyncio.subprocess.PIPE,
            asyncio.subprocess.PIPE,
        )
    ]
    assert result == CommandResult(returncode=0, stdout="ok\n", stderr="")
