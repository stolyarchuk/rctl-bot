import re

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


def create_controls_router(settings: Settings, command_runner: CommandRunner) -> Router:
    router = Router(name="controls")
    router.message.filter(
        PrivateChatFilter(),
        AdminFilter(settings.admin_telegram_ids),
    )

    @router.message(Command("start"))
    async def start(message: Message) -> None:
        await message.answer(
            "Raspberry Pi controls are ready.",
            reply_markup=build_controls_keyboard(),
        )

    @router.message(Command(*BOT_COMMANDS.keys()))
    async def command_action(message: Message) -> None:
        command = message.text.removeprefix("/").split(maxsplit=1)[0].split("@", maxsplit=1)[0]
        action_text = BOT_COMMANDS[command]
        await run_action(message, action_text, command_runner)

    @router.message(F.text.in_(set(ACTION_COMMANDS)))
    async def button_action(message: Message) -> None:
        await run_action(message, message.text, command_runner)

    return router


async def run_action(message: Message, action_text: str, command_runner: CommandRunner) -> None:
    argv = command_for_text(action_text)
    if argv is None:
        return

    report_audio_state = action_text in {
        ActionText.VOLUME_UP,
        ActionText.VOLUME_DOWN,
        ActionText.MUTE,
    }
    if not report_audio_state:
        await message.answer(f"Running {action_text}.")

    result = await command_runner.run(argv)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        await message.answer(f"{action_text} failed: {details}")
        return

    if report_audio_state:
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

        reply = format_audio_state_reply(action_text, state_result.stdout)
        await message.answer(reply)


def format_audio_state_reply(action_text: str, stdout: str) -> str:
    if action_text == ActionText.MUTE:
        return "Mute: on" if "[MUTED]" in stdout else "Mute: off"

    match = re.search(r"Volume:\s+([0-9]+(?:\.[0-9]+)?)", stdout)
    if match is None:
        return "Volume: unknown"

    volume_percent = round(float(match.group(1)) * 100)
    return f"Volume: {volume_percent}%"
