import re
from dataclasses import dataclass

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from rctl_bot.commands import (
    ACTION_COMMANDS,
    BOT_COMMANDS,
    VOLUME_STATE_COMMAND,
    ActionText,
    command_for_text,
)
from rctl_bot.config import Settings
from rctl_bot.filters import AdminFilter, PrivateChatFilter
from rctl_bot.keyboards import build_controls_keyboard
from rctl_bot.services.command_runner import CommandRunner

MUTE_KEYBOARD_REFRESH_TEXT = "\u2060"


@dataclass
class MuteState:
    muted: bool


def create_controls_router(
    settings: Settings,
    command_runner: CommandRunner,
    mute_state: MuteState,
) -> Router:
    router = Router(name="controls")
    router.message.filter(
        PrivateChatFilter(),
        AdminFilter(settings.admin_telegram_ids),
    )

    @router.message(Command("start"))
    async def start(message: Message) -> None:
        await message.answer(
            "Raspberry Pi controls are ready.",
            reply_markup=build_controls_keyboard(muted=mute_state.muted),
        )

    @router.message(Command(*BOT_COMMANDS.keys()))
    async def command_action(message: Message) -> None:
        command = message.text.removeprefix("/").split(maxsplit=1)[0].split("@", maxsplit=1)[0]
        action_text = BOT_COMMANDS[command]
        await run_action(message, action_text, command_runner, mute_state)

    @router.message(F.text.in_(set(ACTION_COMMANDS)))
    async def button_action(message: Message) -> None:
        await run_action(message, message.text, command_runner, mute_state)

    return router


async def read_mute_state(command_runner: CommandRunner) -> bool:
    result = await command_runner.run(VOLUME_STATE_COMMAND)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"mute state failed: {details}")
    return is_muted(result.stdout)


async def run_action(
    message: Message,
    action_text: str,
    command_runner: CommandRunner,
    mute_state: MuteState | None = None,
) -> None:
    argv = command_for_text(action_text)
    if argv is None:
        return

    report_volume_state = action_text in {
        ActionText.VOLUME_UP,
        ActionText.VOLUME_DOWN,
    }
    report_mute_state = action_text in {ActionText.MUTE, ActionText.UNMUTE}
    if not report_volume_state and not report_mute_state:
        await message.answer(f"Running {action_text}.")

    result = await command_runner.run(argv)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        await message.answer(f"{action_text} failed: {details}")
        return

    if report_volume_state or report_mute_state:
        state_result = await command_runner.run(VOLUME_STATE_COMMAND)
        if state_result.returncode != 0:
            details = (
                state_result.stderr.strip()
                or state_result.stdout.strip()
                or f"exit code {state_result.returncode}"
            )
            await message.answer(
                f"{action_text} state failed: {details}",
            )
            return

        if report_mute_state:
            muted = is_muted(state_result.stdout)
            if mute_state is not None:
                mute_state.muted = muted
            keyboard_message = await message.answer(
                MUTE_KEYBOARD_REFRESH_TEXT,
                reply_markup=build_controls_keyboard(muted=muted),
            )
            await keyboard_message.delete()
            return

        reply = format_audio_state_reply(action_text, state_result.stdout)
        await message.answer(reply)


def is_muted(stdout: str) -> bool:
    return "[MUTED]" in stdout


def format_audio_state_reply(action_text: str, stdout: str) -> str:
    match = re.search(r"Volume:\s+([0-9]+(?:\.[0-9]+)?)", stdout)
    if match is None:
        return "Volume: unknown"

    volume_percent = round(float(match.group(1)) * 100)
    return f"Volume: {volume_percent}%"
