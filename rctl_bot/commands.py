from collections.abc import Mapping
from typing import TypeAlias

CommandArgv: TypeAlias = tuple[str, ...]

INITIAL_VOLUME_COMMAND: CommandArgv = (
    "wpctl",
    "set-volume",
    "@DEFAULT_AUDIO_SINK@",
    "60%",
)

VOLUME_STATE_COMMAND: CommandArgv = ("wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@")


class ActionText:
    VOLUME_UP = "Volume up"
    VOLUME_DOWN = "Volume down"
    MUTE = "Mute"
    UNMUTE = "Unmute"
    POWEROFF = "Poweroff"
    REBOOT = "Reboot"


ACTION_COMMANDS: Mapping[str, CommandArgv] = {
    ActionText.VOLUME_UP: ("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"),
    ActionText.VOLUME_DOWN: ("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"),
    ActionText.MUTE: ("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"),
    ActionText.UNMUTE: ("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"),
    ActionText.POWEROFF: ("sudo", "-n", "/usr/bin/systemctl", "poweroff"),
    ActionText.REBOOT: ("sudo", "-n", "/usr/bin/systemctl", "reboot"),
}


BOT_COMMANDS: Mapping[str, str] = {
    "volume_up": ActionText.VOLUME_UP,
    "volume_down": ActionText.VOLUME_DOWN,
    "mute": ActionText.MUTE,
    "poweroff": ActionText.POWEROFF,
    "reboot": ActionText.REBOOT,
}


def command_for_text(text: str) -> CommandArgv | None:
    return ACTION_COMMANDS.get(text)
