import asyncio
import logging

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from rctl_bot.commands import BOT_COMMANDS
from rctl_bot.config import Settings
from rctl_bot.handlers.controls import MuteState, create_controls_router, read_mute_state
from rctl_bot.services.command_runner import CommandRunner


async def register_private_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(command=command, description=description)
            for command, description in BOT_COMMANDS.items()
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )


async def run_bot() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = Settings()
    bot = Bot(token=settings.bot_token)
    command_runner = CommandRunner()
    mute_state = MuteState(muted=await read_mute_state(command_runner))
    dispatcher = Dispatcher()
    dispatcher.include_router(create_controls_router(settings, command_runner, mute_state))

    await register_private_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


def main() -> None:
    uvloop.install()
    asyncio.run(run_bot())
