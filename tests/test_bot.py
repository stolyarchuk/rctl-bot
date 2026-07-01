import asyncio
import logging

from rctl_bot import bot
from rctl_bot.services.command_runner import CommandResult


class FailingCommandRunner:
    def __init__(self) -> None:
        self.calls = []

    async def run(self, argv):
        self.calls.append(argv)
        return CommandResult(returncode=1, stdout="", stderr="no audio sink")


class FakeBot:
    def __init__(self) -> None:
        self.messages: list[tuple[int, str]] = []

    async def send_message(self, chat_id: int, text: str) -> None:
        self.messages.append((chat_id, text))


class VolumeStateCommandRunner:
    def __init__(self) -> None:
        self.calls = []

    async def run(self, argv):
        self.calls.append(argv)
        return CommandResult(returncode=0, stdout="Volume: 0.60 [MUTED]\n", stderr="")


def test_set_initial_volume_logs_failure_and_returns(caplog) -> None:
    command_runner = FailingCommandRunner()

    with caplog.at_level(logging.ERROR):
        asyncio.run(bot.set_initial_volume(command_runner))

    assert command_runner.calls == [
        ("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "60%")
    ]
    assert "initial volume failed: no audio sink" in caplog.text


def test_notify_startup_admins_sends_greeting_with_volume_state() -> None:
    fake_bot = FakeBot()
    command_runner = VolumeStateCommandRunner()

    asyncio.run(
        bot.notify_startup_admins(fake_bot, frozenset({1002, 1001}), command_runner)
    )

    assert command_runner.calls == [("wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@")]
    assert fake_bot.messages == [
        (1001, "Raspberry Pi controls started.\nVolume: 60%\nMute: on"),
        (1002, "Raspberry Pi controls started.\nVolume: 60%\nMute: on"),
    ]
