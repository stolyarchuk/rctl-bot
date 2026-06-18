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


def test_set_initial_volume_logs_failure_and_returns(caplog) -> None:
    command_runner = FailingCommandRunner()

    with caplog.at_level(logging.ERROR):
        asyncio.run(bot.set_initial_volume(command_runner))

    assert command_runner.calls == [
        ("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "60%")
    ]
    assert "initial volume failed: no audio sink" in caplog.text
