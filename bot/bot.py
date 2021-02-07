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
import os
import random
import sys
import traceback
import typing
from tabulate import tabulate
from datetime import datetime
import logging

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Bot as BotBase
from twi_secrets import TOKEN, TWI_SETTINGS_PATH, LICENSE_PATH
from utils import get_settings, Embed, box

from bot.help import send_help_for, twilight_help

log = logging.getLogger("twilight.bot")
if os.path.exists("./bot/cogs.json"):
    cogs_path = "./bot/cogs.json"
else:
    from twi_secrets import COGS_PATH as cogs_path

if os.path.exists("./bot/blocklist.json"):
    blocklist_path = "./bot/blocklist.json"
else:
    from twi_secrets import BLOCKLIST_PATH as blocklist_path


@commands.command()
async def ping(ctx):
    """Pong."""
    await ctx.message.reply("Pong.", mention_author=False)


@commands.command()
@commands.is_owner()
async def load(ctx, cog: str):
    """Load a cog"""
    bot = ctx.bot
    bot.load_extension(cog)
    await ctx.send(content=f"Loaded `{cog}`")


@commands.command()
@commands.is_owner()
async def unload(ctx, cog: str):
    """Unload a cog"""
    bot = ctx.bot
    bot.unload_extension(cog)
    await ctx.send(content=f"Unloaded `{cog}`")


@commands.command()
@commands.is_owner()
async def cogs(ctx):
    """List the cogs and their loaded state"""
    cogs = ctx.bot.grab_cogs()
    embed = Embed.create(ctx, title="Cogs")
    cogs_list = []
    for key, value in cogs.items():
        _list = []
        _list.append(key)
        _list.append(value)
        # Not the prettiest thing ever but it'll work...
        cogs_list.append(_list)
    embed.description = box(tabulate(cogs_list, ("Cog Name", "Loaded")), "md")
    await ctx.send(embed=embed)


to_add = [ping, load, unload, cogs, twilight_help]
TWILIGHT_WAVE_PNG = "https://cdn.discordapp.com/attachments/779822877460660274/779866702971666442/twilight_wave.png"
TWILIGHT_PFP = "https://cdn.discordapp.com/avatars/734159757488685126/9acbfbc1be79bd3b73b763dba39e647d.webp?size=1024"
OWNERS = [
    544974305445019651,
]
IGNORE_EXECEPTIONS = (commands.CommandNotFound, commands.BadArgument)
with open(LICENSE_PATH) as fp:
    LICENSE = fp.read()  # Open the license file


async def dev_check(ctx: commands.Context):
    """Lock commands to the dev only"""
    bot = ctx.bot
    return await bot.is_owner(ctx.author)


def grab_cogs() -> dict:
    """Open the cogs JSON file and return the cogs

    Returns
    -------
    dict
        The cogs dictionary containing the loaded state of cogs
    """
    with open(cogs_path) as f:
        return json.load(f)


def write_cogs(cogs: dict) -> None:
    """Write a dictionary containing the states of cogs to the JSON file

    Parameters
    ----------
    cogs: :class:`dict`
        The cogs dictionary
    """
    with open(cogs_path, "w") as f:
        json.dump(cogs, f, indent=4)


def grab_prefix(bot: "Twilight", msg: discord.Message):
    """Custom prefixes for Twilight"""
    base = [f"<@{bot.user.id}> ", f"<@!{bot.user.id}> ", ">"]
    if msg.guild:
        with open(TWI_SETTINGS_PATH) as fp:
            settings = json.load(fp)
        if str(msg.guild.id) not in settings.keys():
            pass  # TODO: Change this to be setup
        else:
            base.extend(settings[str(msg.guild.id)]["prefixes"])
    return base


class Twilight(BotBase):
    """
    The Twilight bot core.

    This core allows me to have a customized Discord bot that still has all of the functions of a normal bot

    Mostly, this allows me to have more control over different events and such

    Attributes
    ----------
    __version__: :class:`str`
        Twilight's version
    __author__: :class:`str`
        String containing the author of the code
    last_exception: :class:`str`
        The last exception raised by a command
        Useful for the traceback command
    uptime: :class:`DateTime`
        The time the bot has been up
    exit_code: :class:`int`
        The code the bot should exit with when turning off
        This is for the autorestart file
    blocklist: :class:`dict`
        A dictionary containing two lists of blocklisted ids
        key `users` contains the blocklisted user ids
        key `guilds` contains the blocklisted guild ids
    """

    __version__ = "0.1.10"
    __author__ = "Jojo#7791"

    def __init__(self):
        self.TOKEN = TOKEN
        self.last_exception = None
        self.grab_cogs = grab_cogs
        self.license = LICENSE
        self.uptime = None
        self.exit_code = 1
        with open(blocklist_path) as fp:
            self.blocklist: Dict[str, list] = json.load(fp)
        intents = discord.Intents.default()
        intents.members = True
        super().__init__(
            command_prefix=grab_prefix,
            help_command=None,
            owner_ids=OWNERS,
            intents=intents,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=False, replied_user=True
            ),
        )
        for com in to_add:
            self.add_command(com)
            log.info(f"Loaded {com.name}")

    def setup(self):
        """Setup Twilight's cogs

        This will grab cogs from a json file and load them one by one

        If a cog fails to load, it's state will be toggled to False

        After loading the cogs it will write them again.
        """
        cogs = grab_cogs()
        loaded = [x for x in cogs.keys() if cogs[x] == True]
        for cog in loaded:
            try:
                self.load_extension(cog)
            except commands.ExtensionFailed as e:
                print(f"Failed to load {cog}")
                print(e)
                cogs[cog] = False
            except commands.ExtensionNotFound as e:
                print(f"Could not find {cog}")
            else:
                log.info("{} loaded".format(cog))
        write_cogs(cogs)
        log.info("Cogs loaded")

    def save_blocklist(self):
        """Saves the blocklist to a JSON file"""
        with open(blocklist_path) as fp:
            blocklist = json.load(fp)
        blocklist["users"] = self.blocklist
        blocklist["guilds"] = self.guild_blocklist
        with open(blocklist, "w") as fp:
            json.dump(blocklist, fp, indent=4)
        log.info("Saved the blocklist")

    async def async_stop(self, exit_code: int = 0):
        """|coro|

        Close the bot's connections and logs out

        Parameters
        ----------
        exit_code: Optional[:class:`int`]
            The code the bot should exit with
            Defaults to `0` (shutdown)

            Codes:
                0: Shutdown
                1: Warning
                4: Restart
        """
        await self.logout()
        log.info("Logging out of Twilight")
        self.exit_code = exit_code

    def stop(self, exit_code: int = 0):
        """A non-async way to close the bot

        Parameters
        ----------
        exit_code: Optional[:class:`int`]
            The code the bot should exit with
            Defaults to `0` (shutdown)

            Codes:
                0: Shutdown
                1: Warning
                4: Restart
        """
        asyncio.create_task(self.stop(exit_code=exit_code))

    def run(self, no_cogs: bool = False, dev: bool = False):
        """Run Twilight

        Parameters
        ----------
        no_cogs: :type:`bool`
            Whether or not Twilight should load up cogs
        dev: :type:`bool`
            Locks commands to dev only.
        """
        log.info("Waking up Twilight")
        if no_cogs is False:
            self.setup()
        if dev is True:
            self.add_check(dev_check)

        log.info(f"Giving Twilight coffee. Running version {self.__version__}")
        super().run(self.TOKEN, reconnect=True)

    async def on_command_error(self, ctx, exc: Exception):
        if any([isinstance(exc, error) for error in IGNORE_EXECEPTIONS]):
            return
        elif isinstance(exc, commands.MissingRequiredArgument):
            return await send_help_for(ctx=ctx, thing=ctx.command.qualified_name)
        elif isinstance(exc, commands.NotOwner):
            return  # Don't need to do anything for owner only
        elif isinstance(exc, commands.ConversionError):
            if exc.args:
                return await ctx.send(exc.args[0])
            else:
                return await send_help_for(ctx, ctx.command)
        elif isinstance(exc, commands.CheckFailure):  # Check failures are the worstest
            return await ctx.send(
                "You did not pass the required check for command `{}`".format(
                    ctx.command
                )
            )
        await ctx.send(
            "`Error in command '{}'. Check your console for details`".format(
                ctx.command
            )
        )
        self.last_exception = "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        )
        if hasattr(exc, "original"):
            if isinstance(exc, discord.Forbidden):
                await ctx.send("Discord has forbidden me to do that")
            else:
                raise exc.original
        else:
            raise exc

    async def on_ready(self):
        log.info("Twilight online.")

    async def on_message(self, message: discord.Message):
        if message.content in (f"<@!{self.user.id}>", f"<@{self.user.id}>"):
            return await message.reply(
                f"My prefixes are {', '.join(grab_prefix(self, message))}"
            )
        if message.author.bot:
            return  # Pesky bots
        if message.author.id in self.blocklist:
            return  # Blocked people shouldn't be able to use commands
        await self.process_commands(message)

    def reload_extension(self, extension: str):
        """A modified version of :func:`Bot.reload_extension`

        Parameters
        ----------
        extension: :class:`str`
            The extension to reload
            If the extension is loaded it will reload that cog
            If it is unloaded, however, it will load and then reload the cog
        """
        # Checking of the cog should be in the actual command
        try:
            return super().reload_extension(f"cogs.{extension}")
        except commands.ExtensionNotLoaded:
            # If it's not loaded we just want to load it
            self.load_extension(extension)
            return super().reload_extension(f"cogs.{extension}")

    def load_extension(self, cog: str) -> typing.Optional[str]:
        """A modified version of :func:`Bot.load_extension`

        Parameters
        ----------
        cog: :class:`str`
            The cog to load
            If the cog is already loaded it will return a message

        Returns
        -------
        Optional[str]
            If the cog is already loaded it will return so

        Raises
        ------
        commands.ExtensionNotFound
            If the cog isn't in the cogs JSON this will be raised
        """
        # `super().reload_extension()` gives this a cogs.:extension:
        if cog.startswith("cogs."):
            return super().load_extension(cog)  # So load it here
        cogs = grab_cogs()
        if cog in cogs.keys():
            cogs[cog] = True
            write_cogs(cogs)
            return super().load_extension(f"cogs.{cog}")
        else:
            raise commands.ExtensionNotFound(f"No cog named {cog}")

    def unload_extension(self, cog: str):
        """A modified version of :func:`discord.unload_extension`

        Parameters
        ----------
        cog: :class:`str`
            The cog to unload
            If the cog is already unloaded it will return so

        Returns
        -------
        Optional[str]
            If the cog is unloaded it will return a statement saying so

        Raises
        ------
        commands.ExtensionNotFound
            If the cog isn't in the JSON file it will raise this
        """
        if cog.startswith("cogs."):  # This is for `reload_extension`
            # TODO Find if reload extension actually calls this
            return super().unload_extension(cog)
        cogs = grab_cogs()
        if cog in cogs.keys():
            cogs[cog] = False
            write_cogs(cogs)
            return super().unload_extension(f"cogs.{cog}")
        else:
            raise commands.ExtensionNotFound(f"No cog named  {cog}")
