from rctl_bot.commands import ACTION_COMMANDS, VOLUME_STATE_COMMAND, ActionText, command_for_text


def test_action_commands_are_fixed_argv_lists() -> None:
    assert ACTION_COMMANDS[ActionText.VOLUME_UP] == (
        "wpctl",
        "set-volume",
        "@DEFAULT_AUDIO_SINK@",
        "5%+",
    )
    assert ACTION_COMMANDS[ActionText.VOLUME_DOWN] == (
        "wpctl",
        "set-volume",
        "@DEFAULT_AUDIO_SINK@",
        "5%-",
    )
    assert ACTION_COMMANDS[ActionText.MUTE] == (
        "wpctl",
        "set-mute",
        "@DEFAULT_AUDIO_SINK@",
        "toggle",
    )
    assert ACTION_COMMANDS[ActionText.UNMUTE] == ACTION_COMMANDS[ActionText.MUTE]
    assert ACTION_COMMANDS[ActionText.POWEROFF] == (
        "sudo",
        "-n",
        "/usr/bin/systemctl",
        "poweroff",
    )
    assert ACTION_COMMANDS[ActionText.REBOOT] == (
        "sudo",
        "-n",
        "/usr/bin/systemctl",
        "reboot",
    )


def test_command_for_text_returns_none_for_unknown_text() -> None:
    assert command_for_text(ActionText.MUTE) == ACTION_COMMANDS[ActionText.MUTE]
    assert command_for_text(ActionText.UNMUTE) == ACTION_COMMANDS[ActionText.MUTE]
    assert command_for_text("unknown") is None


def test_volume_state_command_is_fixed_argv_list() -> None:
    assert VOLUME_STATE_COMMAND == ("wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@")
