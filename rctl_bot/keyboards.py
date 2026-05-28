from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from rctl_bot.commands import ActionText


def build_controls_keyboard(muted: bool = False) -> ReplyKeyboardMarkup:
    mute_text = ActionText.UNMUTE if muted else ActionText.MUTE
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=ActionText.VOLUME_UP),
                KeyboardButton(text=ActionText.VOLUME_DOWN),
                KeyboardButton(text=mute_text),
            ],
            [
                KeyboardButton(text=ActionText.POWEROFF),
                KeyboardButton(text=ActionText.REBOOT),
            ],
        ],
        is_persistent=True,
        resize_keyboard=True,
    )
