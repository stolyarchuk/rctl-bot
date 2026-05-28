from collections.abc import Mapping
from typing import TypeAlias


CommandArgv: TypeAlias = tuple[str, ...]


class ActionText:
    VOLUME_UP = "Volume up"
    VOLUME_DOWN = "Volume down"
    MUTE = "Mute"
    POWEROFF = "Poweroff"
    REBOOT = "Reboot"


ACTION_COMMANDS: Mapping[str, CommandArgv] = {
    ActionText.VOLUME_UP: ("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"),
    ActionText.VOLUME_DOWN: ("wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"),
    ActionText.MUTE: ("wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"),
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
