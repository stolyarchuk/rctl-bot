import asyncio
from dataclasses import dataclass

from rctl_bot.commands import CommandArgv


@dataclass(frozen=True)
class CommandResult:
    returncode: int
    stdout: str
    stderr: str


class CommandRunner:
    async def run(self, argv: CommandArgv) -> CommandResult:
        process = await asyncio.create_subprocess_exec(
            *argv,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        return CommandResult(
            returncode=process.returncode,
            stdout=stdout.decode(),
            stderr=stderr.decode(),
        )
