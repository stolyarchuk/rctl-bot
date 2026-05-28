from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import Message

from rctl_bot.commands import ACTION_COMMANDS, BOT_COMMANDS, command_for_text
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

    await message.answer(f"Running {action_text}.")
    result = await command_runner.run(argv)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        await message.answer(f"{action_text} failed: {details}")
