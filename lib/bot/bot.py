import discord
from discord import Intents
from discord.ext.commands import Bot as BotBase
from discord import Forbidden
from discord.ext.commands import (
    Context, CommandNotFound, BadArgument, MissingRequiredArgument, CheckFailure, NotOwner,
    Command, errors, ExtensionNotLoaded
)
from typing import *
from asyncio import sleep
import traceback
from enum import IntEnum  # For the restart command :D
import sys
from datetime import datetime
from ..db import db
from ..cogs.utils.embed import Embed
from ..secrets import TOKEN, COGS_PATH
import json

TWILIGHT_WAVE_PNG = "https://cdn.discordapp.com/attachments/779822877460660274/779866702971666442/twilight_wave.png"
TWILIGHT_PFP = "https://cdn.discordapp.com/avatars/734159757488685126/9acbfbc1be79bd3b73b763dba39e647d.webp?size=1024"
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


def grab_cogs():
    with open(COGS_PATH) as f:
        return json.load(f)


def write_cogs(cogs: dict):
    with open(COGS_PATH, "w") as f:
        return json.dump(cogs, f, indent=4)


class Ready(object):
    def __init__(self):
        self.cogs = grab_cogs()
        for cog in self.cogs:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print("{} is ready\n".format(cog))

    def all_ready(self):
        return all([getattr(self, cog) for cog in self.cogs])


class Twilight(BotBase):
    """
        The Twilight bot core.
        This core allows me to have a customized Discord bot that still has all of the functions of a normal bot
        Mostly, this allows me to have more control over different events and such
    """

    def __init__(self, version: str):
        self.ready = False
        self.cogs_ready = Ready()
        self.last_exception = None
        self.grab_cogs = grab_cogs
        self.license = LICENSE
        self._shutdown_level = ShutdownLevels.CRITICAL
        self._uptime = None
        self.version = version
        super().__init__(
            command_prefix=">", owner_ids=OWNERS,
            intents=Intents.all()
        )

    def setup(self):
        cogs = grab_cogs()
        loaded = [x for x in cogs.keys() if cogs[x] == True]
        for cog in loaded:
            try:
                self.load_extension(cog)
            except errors.ExtensionFailed as e:
                print(f"Failed to load {cog}")
                print(e)
            except errors.ExtensionNotFound as e:
                print(f"Could not find {cog}")
            else:
                print("{} loaded".format(cog))
        print("Cogs loaded")

    async def logout(self):
        await super().logout()

    async def shutdown(self, commit: bool = True):
        if commit:
            db.commit()
        sys.exit(0)

    async def restart(self, commit: bool = True):
        if commit:
            db.commit()
        sys.exit(4)

    def run(self):
        print("Waking up Twilight")
        self.setup()

        self.TOKEN = TOKEN

        print(f"Giving Twilight coffee. Running version {self.version}")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        if not self.is_ready:
            return await ctx.send("I am not ready for commands yet!")
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_command_error(self, ctx, exc: Exception):
        if any([isinstance(exc, error) for error in IGNORE_EXECEPTIONS]):
            return
        elif isinstance(exc, MissingRequiredArgument):
            return await ctx.send_help(ctx.command)
        elif isinstance(exc, NotOwner):
            return  # Don't need to do anything for owner only
        elif isinstance(exc, CheckFailure):  # Check failures are the worstest
            return await ctx.send("You did not pass the required check for command `{}`".format(ctx.command))
        await ctx.send("`Error in command '{}'. Check your console for details`".format(ctx.command))
        self.last_exception = "```py\n{}```".format(
            "".join(traceback.format_exception(
                type(exc), exc, exc.__traceback__
            ))
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
            self._uptime = datetime.utcnow()
        else:
            print("Bot reconnected")
        channel = self.get_channel(779822877460660274)
        embed = discord.Embed(
            title="Twilight Online again", description="Twilight is back online.",
            color=discord.Color.blue()
        )
        embed.set_thumbnail(url=TWILIGHT_WAVE_PNG)
        embed.timestamp = datetime.utcnow()
        await channel.send(embed=embed)

    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return  # Pesky bots
        await self.process_commands(message)

    def reload_extension(self, extension: str, bypass_core: bool = None):
        if bypass_core:
            return super().reload_extension("lib.cogs.core")
        extension = extension.lower()
        cogs = self.grab_cogs()
        if extension not in cogs.keys():
            return "I don't have a cog named `{}`".format(extension)
        if extension == "core":
            return "I can't reload/unload `core` as it would break Twilight"
        else:
            super().reload_extension(f"lib.cogs.{extension}")
            return "Reloaded `{}`".format(extension)

    def load_extension(self, cog: str):
        if cog.startswith("lib."):
            return super().load_extension(cog)
        cogs = grab_cogs()
        if cog in cogs.keys():
            cogs[cog] = True
            write_cogs(cogs)
        else:
            pass
        return super().load_extension(f"lib.cogs.{cog}")

    def unload_extension(self, cog: str):
        if cog.startswith("lib."):  # This is for `reload_extension`
            return super().unload_extension(cog)
        cogs = grab_cogs()
        if cog in cogs.keys():
            cogs[cog] = False
            write_cogs(cogs)
        return super().unload_extension(f"lib.cogs.{cog}")


class ShutdownLevels(IntEnum):
    SHUTDOWN = 0
    CRITICAL = 1
    RESTART = 26  # IDK why I made this 26... looking at Red too much LOL
