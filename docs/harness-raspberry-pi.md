# Raspberry Pi Target Harness

This is a redacted deployment profile derived from the repository-local
`rinfo` snapshot. It intentionally excludes serial numbers, MAC addresses,
partition identifiers, IP addresses, and other unique network or device
identifiers.

## Hardware

- Board: Raspberry Pi 4 Model B Rev 1.4
- Architecture: AArch64
- CPU: four cores
- Memory: 4 GB
- Boot and root storage: microSD, with a roughly 16 GB root filesystem
- Swap: approximately 2 GB of compressed zram
- Reported throttling state: none (`throttled=0x0`)

## Operating Environment

- Distribution: Debian GNU/Linux 13 (trixie)
- Image: Raspberry Pi reference image dated 2026-04-21
- Kernel snapshot: Linux `6.18.34+rpt-rpi-v8`, built 2026-06-09
- Boot mode: 64-bit (`arm_64bit=1`)
- Configured ARM frequency: 1800 MHz
- Default system target is headless/multi-user; desktop packages are absent.

These values describe the captured snapshot and may drift after operating
system, firmware, or hardware changes.

## Audio and Display

- Primary analog playback device: `bcm2835 Headphones`
- Additional playback devices: two HDMI audio outputs
- Both HDMI connectors were disconnected in the snapshot.
- The bot controls the active PipeWire/WirePlumber default sink through
  `wpctl`; do not hard-code an ALSA card number.

## Networking

- Wireless LAN was active in the snapshot.
- Ethernet was enabled but had no detected link.
- Bluetooth and wireless LAN were not rfkill-blocked.

Do not copy raw networking output from `rinfo` into documentation, logs,
issues, or prompts. Summarize only the operational state needed for a task.

## Deployment Constraints

- Treat CPU, memory, and microSD write endurance as constrained resources.
- Avoid unnecessary background services, polling loops, and persistent writes.
- Keep subprocess calls explicit and bounded.
- Power commands require configured passwordless access only for the fixed
  `systemctl poweroff` and `systemctl reboot` commands.
