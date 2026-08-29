from aiogram.enums import ButtonStyle
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from rctl_bot.commands import ActionText


def build_controls_keyboard(muted: bool = False) -> ReplyKeyboardMarkup:
    mute_text = ActionText.UNMUTE if muted else ActionText.MUTE
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionText.VOLUME_UP, style=ButtonStyle.SUCCESS),
                KeyboardButton(text=ActionText.VOLUME_DOWN, style=ButtonStyle.SUCCESS),
                KeyboardButton(text=mute_text, style=ButtonStyle.PRIMARY),
            ],
            [
                KeyboardButton(text=ActionText.POWEROFF, style=ButtonStyle.DANGER),
                KeyboardButton(text=ActionText.REBOOT, style=ButtonStyle.DANGER),
            ],
        ],
        is_persistent=True,
        resize_keyboard=True,
    )
