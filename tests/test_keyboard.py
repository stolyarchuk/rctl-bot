from rctl_bot.commands import ActionText
from rctl_bot.keyboards import build_controls_keyboard


def test_controls_keyboard_has_two_expected_rows() -> None:
    keyboard = build_controls_keyboard()

    rows = [[button.text for button in row] for row in keyboard.keyboard]

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
