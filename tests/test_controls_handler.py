import asyncio

from rctl_bot.commands import ACTION_COMMANDS, VOLUME_STATE_COMMAND, ActionText
from rctl_bot.handlers.controls import MuteState, read_mute_state, run_action
from rctl_bot.services.command_runner import CommandResult


class FakeMessage:
    def __init__(self) -> None:
        self.answers: list[tuple[str, object | None]] = []
        self.deleted_answers: list[tuple[str, object | None]] = []

    async def answer(self, text: str, reply_markup: object | None = None) -> None:
        answer = FakeAnswer(self, text, reply_markup)
        self.answers.append((text, reply_markup))
        return answer


class FakeAnswer:
    def __init__(self, message: FakeMessage, text: str, reply_markup: object | None) -> None:
        self.message = message
        self.text = text
        self.reply_markup = reply_markup

    async def delete(self) -> None:
        answer = (self.text, self.reply_markup)
        self.message.answers.remove(answer)
        self.message.deleted_answers.append(answer)


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
    assert message.answers == [("Volume: 55%", None)]


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
    assert message.answers == [("Volume: 30%", None)]


def test_read_mute_state_returns_true_when_sink_is_muted() -> None:
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="Volume: 0.55 [MUTED]\n", stderr=""),
        ]
    )

    muted = asyncio.run(read_mute_state(runner))

    assert runner.calls == [VOLUME_STATE_COMMAND]
    assert muted is True


def test_read_mute_state_returns_false_when_sink_is_not_muted() -> None:
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="Volume: 0.55\n", stderr=""),
        ]
    )

    muted = asyncio.run(read_mute_state(runner))

    assert runner.calls == [VOLUME_STATE_COMMAND]
    assert muted is False


def test_mute_updates_button_to_unmute_without_mute_status_reply() -> None:
    message = FakeMessage()
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="", stderr=""),
            CommandResult(returncode=0, stdout="Volume: 0.55 [MUTED]\n", stderr=""),
        ]
    )
    mute_state = MuteState(muted=False)

    asyncio.run(run_action(message, ActionText.MUTE, runner, mute_state))

    assert runner.calls == [ACTION_COMMANDS[ActionText.MUTE], VOLUME_STATE_COMMAND]
    assert mute_state.muted is True
    assert message.answers == []
    keyboard = message.deleted_answers[0][1]
    assert keyboard.keyboard[0][2].text == ActionText.UNMUTE


def test_unmute_updates_button_to_mute_without_mute_status_reply() -> None:
    message = FakeMessage()
    runner = FakeCommandRunner(
        [
            CommandResult(returncode=0, stdout="", stderr=""),
            CommandResult(returncode=0, stdout="Volume: 0.55\n", stderr=""),
        ]
    )
    mute_state = MuteState(muted=True)

    asyncio.run(run_action(message, ActionText.UNMUTE, runner, mute_state))

    assert runner.calls == [ACTION_COMMANDS[ActionText.MUTE], VOLUME_STATE_COMMAND]
    assert mute_state.muted is False
    assert message.answers == []
    keyboard = message.deleted_answers[0][1]
    assert keyboard.keyboard[0][2].text == ActionText.MUTE
