import asyncio

from rctl_bot.commands import ACTION_COMMANDS, VOLUME_STATE_COMMAND, ActionText
from rctl_bot.handlers.controls import run_action
from rctl_bot.services.command_runner import CommandResult


class FakeMessage:
    def __init__(self) -> None:
        self.answers: list[str] = []

    async def answer(self, text: str) -> None:
        self.answers.append(text)


class FakeCommandRunner:
    def __init__(self, results: list[CommandResult]) -> None:
        self.results = results
        self.calls: list[tuple[str, ...]] = []

    async def run(self, argv: tuple[str, ...]) -> CommandResult:
        self.calls.append(argv)
        return self.results.pop(0)


def test_volume_up_replies_with_new_volume_level() -> None:
    message = FakeMessage()
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="", stderr=""),
            CommandResult(returncode=0, stdout="Volume: 0.55\n", stderr=""),
        ]
    )

    asyncio.run(run_action(message, ActionText.VOLUME_UP, runner))

    assert runner.calls == [ACTION_COMMANDS[ActionText.VOLUME_UP], VOLUME_STATE_COMMAND]
    assert message.answers == ["Volume: 55%"]


def test_volume_down_replies_with_new_volume_level() -> None:
    message = FakeMessage()
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="", stderr=""),
            CommandResult(returncode=0, stdout="Volume: 0.30\n", stderr=""),
        ]
    )

    asyncio.run(run_action(message, ActionText.VOLUME_DOWN, runner))

    assert runner.calls == [ACTION_COMMANDS[ActionText.VOLUME_DOWN], VOLUME_STATE_COMMAND]
    assert message.answers == ["Volume: 30%"]


def test_mute_replies_with_mute_on_when_sink_is_muted() -> None:
    message = FakeMessage()
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="", stderr=""),
            CommandResult(returncode=0, stdout="Volume: 0.55 [MUTED]\n", stderr=""),
        ]
    )

    asyncio.run(run_action(message, ActionText.MUTE, runner))

    assert runner.calls == [ACTION_COMMANDS[ActionText.MUTE], VOLUME_STATE_COMMAND]
    assert message.answers == ["Mute: on"]


def test_mute_replies_with_mute_off_when_sink_is_not_muted() -> None:
    message = FakeMessage()
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="", stderr=""),
            CommandResult(returncode=0, stdout="Volume: 0.55\n", stderr=""),
        ]
    )

    asyncio.run(run_action(message, ActionText.MUTE, runner))

    assert runner.calls == [ACTION_COMMANDS[ActionText.MUTE], VOLUME_STATE_COMMAND]
    assert message.answers == ["Mute: off"]
