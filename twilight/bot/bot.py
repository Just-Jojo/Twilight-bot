"""
MIT License

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
SOFTWARE.
"""

import asyncio
import json
import logging
import sys
import typing
from enum import IntEnum
from os import path

import discord
from discord.ext import commands
from discord.ext.commands import Bot

from twilight.cogs import Core, Dev, cogs
from twilight.cogs.abc import Cog

log = logging.getLogger("twilight.bot")

_guild_config = {
    "prefixes": [],
    "member_welcome": ["Welcome {0.mention} to {1.name}"],
    "member_leave": ["Goodbye {0.name}! We'll miss you!"],
    "welcome_channel": None,
    "admins": [],
    "mods": [],  # admins and mods are role ids
}


def setup_paths() -> typing.Tuple[str, str, str]:
    """Returns the paths for the bot to use"""
    if path.exists("./data/config.json"):
        config_path = "./data/config.json"
    else:
        from twi_secrets import DATAPATH as config_path
    if path.exists("./data/guild_data.json"):
        guild_path = "./data/guild_data.json"
    else:
        from twi_secrets import GUILD_DATAPATH as guild_path
    if path.exists("./data/member_data.json"):
        member_path = "./data/member_data.json"
    else:
        from twi_secrets import MEMBER_DATAPATH as member_path
    return config_path, guild_path, member_path


def setup_config(conf_path: str, guild_path: str, member_path: str) -> dict:
    with open(conf_path) as fp:
        ret = json.load(fp)
    with open(guild_path) as fp:
        guild = json.load(fp)
    with open(member_path) as fp:
        member = json.load(fp)
    return ret, guild, member


async def dev_mode(ctx: commands.Context):
    return await ctx.bot.is_owner(ctx.author)


class Twilight(Bot):
    """Twilight bot class"""

    __version__ = "2.0.1"  # \o/

    def __init__(self, cli_flags):
        self.config_path, self.guild_path, self.member_path = setup_paths()
        self.config, self.guild_config, self.member_config = setup_config(
            self.config_path, self.guild_path, self.member_path
        )

        async def get_prefix(bot: self, m: discord.Message):
            base = [self.config["base_prefix"]]
            if m.guild:
                thing = self.config.get(str(m.guild.id), [])
                if thing:
                    thing = thing["prefixes"]
                base.extend(thing)
            return base

        allowed_mentions = discord.AllowedMentions(
            everyone=False, users=True, roles=False, replied_user=False
        )
        intents = discord.Intents.default()

        self._disable_com = []
        super().__init__(
            command_prefix=get_prefix,
            allowed_mentions=allowed_mentions,
            owner_ids=self.config["owners"],
            intents=intents,
        )
        if cli_flags.dev:
            self.add_check(dev_mode)
        if cli_flags.lock:
            self._disable_com.append("invite")
        self._exit_code = ShutdownCodes.CRITICAL
        self.blacklist = []
        self._changed_status = False

    async def on_command_error(self, ctx: commands.Context, exc: Exception):
        if isinstance(exc, commands.NotOwner) or isinstance(exc, commands.CheckFailure):
            pass
        elif isinstance(exc, commands.CommandNotFound):
            pass
        elif isinstance(exc, commands.MissingRequiredArgument):
            await ctx.send_help(ctx.command)
        elif isinstance(exc, commands.BadArgument):
            if exc.args:
                await ctx.send(exc.args[0])
            else:
                await ctx.send_help(ctx.command)
        else:
            await ctx.send(
                f"`Error in command '{ctx.command}'. Check your console for details`"
            )
            raise exc

    async def on_message(self, msg: discord.Message):
        if msg.author.id in self.blacklist or msg.author.bot:
            return
        await self.process_commands(msg)

    async def pre_launch(self):
        """Load cogs and disable commands"""
        self.add_cog(Core(self))
        self.add_cog(Dev(self))
        to_load = cogs
        to_del = []
        for cog in to_load:
            try:
                self.load_extension(name=f"twilight.cogs.{cog}")
            except Exception as exc:
                log.exception(f"Failed to load cog {cog}", exc_info=exc)
                to_del.append(cog)
        for cog in to_del:
            to_load.remove(cog)
        for com in self._disable_com:
            self.disable_command(com)
        self._disable_com = []
        if to_load:
            log.info(f"Loaded these cogs: {', '.join(to_load)}")

    async def start(self, *args, **kwargs):
        """This allows Twilight to load extensions before running"""
        await self.pre_launch()
        return await super().start(self.config["token"], *args, **kwargs)

    def disable_command(self, command: typing.Union[str, commands.Command]):
        """Disable a command.
        This will replace it with a command that says its disabled
        """
        if isinstance(command, commands.Command):
            command = command.name
        com = self.remove_command(command)
        if com is not None:

            @commands.command(name=command)
            async def _replaced(ctx):
                await ctx.send("This command is disabled")

            self.add_command(_replaced)

    def add_cog(self, cog: Cog):
        """Add a cog to Twilight"""
        if not isinstance(cog, Cog):
            raise RuntimeError(
                (
                    f"The {cog.__class__.__name__} cog does not inherit from the base cog"
                    f" class."
                )
            )
        if cog.__cog_name__ in self.cogs:
            raise RuntimeError(f"There is already a cog named {cog.__cog_name__}")
        Cog.__init__(cog)
        try:
            super().add_cog(cog)
        except Exception:
            del cog
            raise

    async def shutdown(self, restart: bool = False):
        """Have the bot shutdown"""
        if restart:
            self._exit_code = ShutdownCodes.RESTART
        else:
            self._exit_code = ShutdownCodes.SHUTDOWN
        await self.logout()
        sys.exit(self._exit_code)

    async def on_connect(self):
        log.info("Twilight is now connected.")
        if not self._changed_status:
            await self.change_presence(activity=discord.Game(name="V2 is out! | >help"))
            self._changed_status = True

    async def on_ready(self):
        log.info("Twilight is now online.")

    async def on_guild_join(self, guild: discord.Guild):
        # Convert the id to a string as that's what I use
        # for keys in the data file
        gid = str(guild.id)
        if gid not in self.guild_config.keys():
            self.guild_config[gid] = _guild_config
            await self._save_config()
        log.info(f"Joined {guild.name}")

    async def on_guild_leave(self, guild: discord.Guild):
        # For guild leaves I might leave the data there
        # I will have to call my guild update method (coming soon™)
        log.info(f"Left {guild.name}")

    async def on_member_join(self, member: discord.Member):
        guild = member.guild
        await self._check_guild(guild)
        if not (channel := self.guild_config[str(guild.id)]["welcome_channel"]):
            return
        welcome = self.guild_config[str(guild.id)].get(
            "member_welcome", "Welcome {0.mention} to {1.name}"
        )
        await channel.send(welcome.format(member, guild))

    async def _check_guild(self, guild: discord.Guild):
        """|coro|

        Check a guild to see if it is in the config
        """
        found = self.guild_config.get(str(guild.id), None)
        if found is None:
            self.guild_config[str(guild.id)] = _guild_config
            self._save_config()

    async def _save_config(self):
        """|coro|

        Save and update the config
        """
        with open(self.guild_path, "w") as fp:
            json.dump(self.guild_config, fp, indent=4)
        with open(self.member_path, "w") as fp:
            json.dump(self.member_config, fp, indent=4)
        _, self.guild_config, self.member_config = setup_config(
            self.config_path, self.guild_path, self.member_path
        )


class ShutdownCodes(IntEnum):
    """An Int Enum containing the various shutdown codes

    This makes keeping track of the shutdown codes easier lol
    """

    SHUTDOWN = 0
    CRITICAL = 1
    RESTART = 2
