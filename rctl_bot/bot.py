import asyncio
import logging

import uvloop
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

from rctl_bot.commands import BOT_COMMANDS
from rctl_bot.config import Settings
from rctl_bot.handlers.controls import create_controls_router
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
    dispatcher = Dispatcher()
    dispatcher.include_router(create_controls_router(settings, CommandRunner()))

    await register_private_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


def main() -> None:
    uvloop.install()
    asyncio.run(run_bot())
