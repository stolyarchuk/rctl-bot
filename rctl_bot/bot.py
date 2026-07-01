import asyncio
import logging

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from rctl_bot.commands import (
    BOT_COMMANDS,
    INITIAL_VOLUME_COMMAND,
    VOLUME_STATE_COMMAND,
    ActionText,
)
from rctl_bot.config import Settings
from rctl_bot.handlers.controls import (
    MuteState,
    create_controls_router,
    format_audio_state_reply,
    is_muted,
    read_mute_state,
)
from rctl_bot.services.command_runner import CommandRunner


async def register_private_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in BOT_COMMANDS.items()
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


async def set_initial_volume(command_runner: CommandRunner) -> None:
    result = await command_runner.run(INITIAL_VOLUME_COMMAND)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        logging.error("initial volume failed: %s", details)


async def notify_startup_admins(
    bot: Bot,
    admin_telegram_ids: frozenset[int],
    command_runner: CommandRunner,
) -> None:
    result = await command_runner.run(VOLUME_STATE_COMMAND)
    if result.returncode != 0:
        details = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        logging.error("startup notification volume state failed: %s", details)
        return

    text = "\n".join(
        [
            "Raspberry Pi controls started.",
            format_audio_state_reply(ActionText.VOLUME_UP, result.stdout),
            f"Mute: {'on' if is_muted(result.stdout) else 'off'}",
        ]
    )
    for admin_id in sorted(admin_telegram_ids):
        try:
            await bot.send_message(chat_id=admin_id, text=text)
        except Exception as exc:
            logging.error("startup notification to %s failed: %s", admin_id, exc)


async def run_bot() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    bot = Bot(token=settings.bot_token)
    command_runner = CommandRunner()
    await set_initial_volume(command_runner)
    mute_state = MuteState(muted=await read_mute_state(command_runner))
    dispatcher = Dispatcher()
    dispatcher.include_router(create_controls_router(settings, command_runner, mute_state))

    await register_private_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await notify_startup_admins(bot, settings.admin_telegram_ids, command_runner)
    await dispatcher.start_polling(bot)


def main() -> None:
    uvloop.install()
    asyncio.run(run_bot())
