from aiogram.enums import ButtonStyle

from rctl_bot.commands import ActionText
from rctl_bot.keyboards import build_controls_keyboard


def test_controls_keyboard_has_two_expected_rows() -> None:
    keyboard = build_controls_keyboard()

    rows = [[button.text for button in row] for row in keyboard.keyboard]
    styles = [[button.style for button in row] for row in keyboard.keyboard]

    assert rows == [
        [
            ActionText.VOLUME_UP,
            ActionText.VOLUME_DOWN,
            ActionText.MUTE,
        ],
        [
            ActionText.POWEROFF,
            ActionText.REBOOT,
        ],
    ]
    assert keyboard.resize_keyboard is True
    assert keyboard.is_persistent is True
    assert styles == [
        [ButtonStyle.SUCCESS, ButtonStyle.SUCCESS, ButtonStyle.PRIMARY],
        [ButtonStyle.DANGER, ButtonStyle.DANGER],
    ]


def test_controls_keyboard_uses_unmute_when_sink_is_muted() -> None:
    keyboard = build_controls_keyboard(muted=True)

    rows = [[button.text for button in row] for row in keyboard.keyboard]

    assert rows[0][2] == ActionText.UNMUTE
    assert keyboard.keyboard[0][2].style == ButtonStyle.PRIMARY
