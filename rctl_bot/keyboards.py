from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from rctl_bot.commands import ActionText


def build_controls_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionText.VOLUME_UP),
                KeyboardButton(text=ActionText.VOLUME_DOWN),
                KeyboardButton(text=ActionText.MUTE),
            ],
            [
                KeyboardButton(text=ActionText.POWEROFF),
                KeyboardButton(text=ActionText.REBOOT),
            ],
        ],
        resize_keyboard=True,
    )
