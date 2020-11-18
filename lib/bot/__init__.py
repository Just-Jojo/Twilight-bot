import discord
from discord.ext.commands import Bot as BotBase
from discord import Forbidden
from discord.ext.commands import (
    Context, CommandNotFound, BadArgument, MissingRequiredArgument,
)
from asyncio import sleep
import traceback
from enum import IntEnum  # For the restart command :D
import sys


cogs = [
    "general",
    "core",
    "mylittlepony",
    "mod"
]

OWNERS = [544974305445019651, ]
IGNORE_EXECEPTIONS = (CommandNotFound, BadArgument)
LICENSE = """MIT License

Copyright (c) 2020 Jojo#7711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE."""


class Ready(object):
    def __init__(self):
        for cog in cogs:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print("{} is ready\n".format(cog))

    def all_ready(self):
        return all([getattr(self, cog) for cog in cogs])


class Twilight(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        self.last_exception = None
        self.license = LICENSE
        self._shutdown_level = ShutdownLevels.CRITICAL
        super().__init__(command_prefix=">", owner_ids=OWNERS)

    def setup(self):
        for cog in cogs:
            self.load_extension("lib.cogs.{}".format(cog))
            print("{} loaded".format(cog))
        print("Cogs loaded")

    async def logout(self):
        await super().logout()

    async def shutdown(self, *, restart: bool = False):
        if restart is True:
            self._shutdown_level = ShutdownLevels.RESTART
        elif restart is False:
            self._shutdown_level = ShutdownLevels.SHUTDOWN
        sys.exit(self._shutdown_level)

    def run(self, version):
        self.version = version

        print("Waking up Twilight")
        self.setup()

        with open("./lib/bot/token.txt", "r") as token:
            self.TOKEN = token.read()

        print("Giving Twilight coffee")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_command_error(self, ctx, exc: Exception):
        if any([isinstance(exc, error) for error in IGNORE_EXECEPTIONS]):
            return
        elif isinstance(exc, MissingRequiredArgument):
            return await ctx.send_help(ctx.command)
        await ctx.send("`Error in command '{}'. Check your console for details`".format(ctx.command))
        self.last_exception = "```py\n{}```".format(
            traceback.format_exception(
                type(exc), exc, exc.__traceback__
            )
        )
        if hasattr(exc, "original"):
            if isinstance(exc, Forbidden):
                await ctx.send("Discord has forbidden me to do that")
            else:
                raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            while not self.cogs_ready.all_ready():
                await sleep(1.5)

            self.ready = True
        else:
            print("Bot reconnected")

    async def on_message(self, message):
        if message.author.bot:
            return  # Pesky bots
        await self.process_commands(message)

    def reload_extension(self, extension: str):
        extension = extension.lower()
        if extension not in cogs:
            return "I don't have a cog named `{}`".format(extension)
        if extension == "core":
            return "I can't reload/unload `core` as it would break Twilight"
        else:
            super().reload_extension("lib.cogs.{}".format(extension))
            return "Reloaded `{}`".format(extension)


class ShutdownLevels(IntEnum):
    SHUTDOWN = 0
    CRITICAL = 1
    RESTART = 26


twilight = Twilight()
