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
### ~~~ Basic Discord and other utilities imports ~~~ ###
import discord
from discord import __version__ as dpyversion
from discord.ext import commands
from discord.ext.commands import (
    command, Cog, is_owner, Context, check, group, guild_only
)
import asyncio
import json
from platform import python_version as pver
from datetime import datetime
### ~~~ Local imports ~~~ ###
from ..bot import Twilight  # Type hinting
from .utils.embed import Embed
from .utils.basic_utils import *
from .utils.converter import RawUserIds
from typing import *
from . import mixin
from tabulate import tabulate

types = {
    "administrator": ["admin", "administrator", "adm"],
    "moderator": ["mod", "moderator", "moder"]
}
information = r"""
    Twilight is a Discord bot written in Python by Jojo#7791.
    Twilight is designed mostly for MLP features but also has moderation tools.
    
    \~\~\~\~\~\~
    
    To invite Twilight to your server, use `>invite` and click on the link.
    You can find the [support](https://discord.gg/JmCFyq7) server
"""


class Core(mixin.BaseCog):
    """
    Core commands Cog. This include `ping` and moderation settings.
    """

    def __init__(self, bot: Twilight):
        self.bot = bot
        self.mod = Moderation()
        self.embed = Embed()

    @command()
    async def ping(self, ctx):
        """Pong."""
        await ctx.send("Pong.")

    @group(name="set")
    @guild_owner()
    @guild_only()
    async def _set(self, ctx: Context):
        """Set up Twilight"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_set.command()
    async def modlog(self, ctx: Context, channel: discord.TextChannel = None):
        """Set a modlog channel"""
        if not channel:
            if Getters.get_modlog(ctx.guild) is None:
                msg = await ctx.send("Would you like to remove the Modlog channel")
                response = await ctx.bot.wait_for('message', check=lambda m: m.id == ctx.author.id)
                if response.content.lower() in ("yes", "y"):
                    message = self.mod.modlog_remove(ctx.guild)
                else:
                    message = "Canceled"
                await msg.edit(content=message)
        else:
            message = self.mod.modlog_set(channel, ctx.guild)
            await ctx.send(content=message)

    @_set.command(name="add")
    async def _add(self, ctx: Context, role_type: str, role: discord.Role):
        """Add a role

        `role_type` means the role type you want to add (eg. moderator or admin)"""
        role_type = role_type.lower()
        if (
            role_type not in types["administrator"] and role_type not in types["moderator"]
        ):
            return await ctx.send(content=(
                "I could not understand what type of role you wanted to set"
                ", you can add one using `admin` or `mod`"
            )
            )
        role_type = "administrator" if role_type in types["administrator"]\
            else "moderator"
        result = self.mod.add_role(ctx.guild, role_type, role)
        await ctx.send(content=result)

    @_set.command()
    async def remove(self, ctx: Context, role_type: str):
        """Remove a role

        `role_type` means the role type you want to remove (eg. moderator or admin)"""
        role_type = role_type.lower()
        if (
            role_type not in types["administrator"] and role_type not in types["moderator"]
        ):
            return await ctx.send(
                content=(
                    "I could not understand the type of role you wanted to remove"
                    ", you can remove one using `admin` or `mod`"
                )
            )
        role_type = "administrator" if role_type in types["administrator"]\
            else "moderator"
        result = self.mod.remove_role(ctx.guild, role_type)
        await ctx.send(content=result)

    @command(name="reload", aliases=["cu", "update"])
    @is_owner()
    async def _reload(self, ctx: Context, cog: str):
        """Reload a cog"""
        result = self.bot.reload_extension(cog)
        await ctx.send(result)

    @command()
    @is_owner()
    async def shutdown(self, ctx: Context, commit: bool = True):
        """Shuts Twilight down"""
        await ctx.send("Shutting down Twilight")
        await self.bot.shutdown(commit=commit)

    @command()
    @is_owner()
    async def restart(self, ctx: Context, commit: bool = True):
        """Attempts to restart the bot"""
        await ctx.send("Restarting...")
        await asyncio.sleep(2)
        await self.bot.restart(commit=commit)

    @command()
    async def invite(self, ctx):
        """Invite the bot to your server"""
        description = (
            "Invite for Twilight! [Here]"
            "(https://discord.com/api/oauth2/authorize?client_id=734159757488685126&permissions=470117622&scope=bot)"
            " is the link to add her to your server (Note,"
            " in order to add a bot to a server you must have the `adminstrator` permission)"
            "\n\nTo receive support, join the [Vanguard](https://discord.gg/JmCFyq7) support server"
            "\nThank you for checking out Twilight! <3"
        )
        embed = Embed.create(
            self, ctx, title="Invite Twilight to your server!", description=description
        )
        await ctx.send(embed=embed)

    @command()
    @is_owner()
    async def trace(self, ctx):
        """Sends the latest traceback error"""
        if self.bot.last_exception == None:
            return await ctx.send("No exceptions have occured yet!")
        if len(self.bot.last_exception) > 2000:
            await ctx.send("Check your console for the logs!")
        embed = self.embed.create(
            ctx, title="Traceback Error", description=self.bot.last_exception)
        await ctx.send(embed=embed)

    @command()
    async def info(self, ctx: Context):
        """Twilight's info"""
        embed = Embed.create(
            self, ctx, title="Twilight bot Info", footer="Twilight bot Info"
        )
        embed.add_field(
            name="<:dpy:779489296389767208>", value="Version: `{}`".format(dpyversion)
        )
        embed.add_field(
            name="<:twilight:734586922910875750>", value="Version: `{}`".format(self.bot.version)
        )
        embed.add_field(
            name="<:python:760888220228780063>", value="Version: `{}`".format(pver())
        )
        embed.add_field(name="Info", value=information, inline=False)
        await ctx.send(embed=embed)

    @command()
    async def uptime(self, ctx: Context):
        """Get Twilight's uptime"""
        since = self.bot._uptime.strftime("%Y-%m-%D %H:%M:%S")
        uptime = datetime.utcnow() - self.bot._uptime
        uptime_str = humanize_timedelta(
            timedelta=uptime) or "Less than one second"
        # await ctx.send("Been up for: **{}** (since {} UTC)".format(uptime_str, since))
        embed = self.embed.create(ctx, title="Uptime!",
                                  footer="Twilight uptime")
        embed.add_field(name="Total time", value="**{}**".format(uptime_str))
        embed.add_field(name="Up since", value="**{}**".format(since))
        await ctx.send(embed=embed)

    @command(name="license")
    async def _license(self, ctx):
        """Twilight's license"""
        embed = Embed.create(
            self, ctx, title="Twilight bot License",
            description=self.bot.license, footer="Twilight bot License :D"
        )
        await ctx.send(embed=embed)

    @group()
    @administrator()
    @guild_only()
    async def announceset(self, ctx: Context):
        """Base announcement channel command"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @announceset.command()
    async def add(self, ctx: Context, channel: discord.TextChannel):
        """Add a channel as the announcement channel"""
        result = self.mod.announcement_set(False, ctx.guild, channel)
        await ctx.send(content=result)

    @announceset.command()
    async def _remove(self, ctx: Context):
        """Remove the announcement channel"""
        result = self.mod.announcement_set(True, ctx.guild)
        await ctx.send(content=result)

    @command()
    @is_owner()
    async def announce(self, ctx: Context, *, announcement: str):
        """Announce a message to Twilight's guilds"""
        embed = Embed.create(
            self, ctx, title="Twilight bot Announcement",
            description=announcement, thumbnail=ctx.bot.avatar_url,
            color=discord.Color.purple(), footer="Twilight bot updates by Jojo#7791"
        )
        async with ctx.typing():
            await self.announce_to_guilds(embed)

    @group()
    @is_owner()
    async def blocklist(self, ctx: Context):
        """Base command for the blocklist settings"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @blocklist.group()
    async def guild(self, ctx: Context):
        """Base guild related blocklist"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @guild.command(name="list")
    async def __list(self, ctx: Context):
        """List the blocklisted guilds"""
        await ctx.author.send(self.bot.guild_blocklist)

    @guild.command(name="add")
    async def _add(self, ctx: Context, guild_id: int):
        """Add a guild to the blocklist via id"""
        guild = self.bot.fetch_guild(guild_id)
        await guild.leave()
        self.bot.guild_blocklist.append(guild_id)
        self.bot.save_blocklist()
        await ctx.send("Added that guild to the blocklist")

    @guild.command(name="remove", aliases=["del", ])
    async def _remove(self, ctx: Context, guild_id: int):
        """Remove a guild from the blocklist via id"""
        self.bot.guild_blocklist.pop(guild_id)
        self.bot.save_blocklist()
        await ctx.send("Removed that guild from the blocklist")

    @blocklist.command(name="list")
    async def _list(self, ctx: Context):
        """List the members in the blocklist"""
        await ctx.author.send(self.bot.blocklist)  # Don't want it to be public
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    @blocklist.command()
    async def add(self, ctx: Context, member: Union[discord.Member, int]):
        """Add a user to the blocklist"""
        if isinstance(member, int):  # If it's an int we just want to append it
            self.bot.blocklist.append(member)
        else:
            self.bot.blocklist.append(member.id)
        self.bot.save_blocklist()  # save it from the command incase it doesn't work
        await ctx.send(f"Added that user to the blocklist")

    @blocklist.command()
    async def remove(self, ctx: Context, member: Union[discord.Member, int]):
        """Remove a user from the blocklist"""
        if isinstance(member, int):  # Same thing
            self.bot.blocklist.pop(member)
        else:
            self.bot.blocklist.pop(member.id)
        self.bot.save_blocklist()  # save it from the command incase it doesn't work
        await ctx.send("Removed that user from the blocklist")

    async def announce_to_guilds(self, message: discord.Embed) -> None:
        """Send a message out to every guild that Twilight is in"""
        channels = Getters.get_all_announce()
        for channel in channels:
            if channel is not None:
                chan = self.bot.get_channel(channel)
                await chan.send(embed=message)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if guild.id in self.bot.guild_blocklist:
            await guild.leave()
        self.mod.setup(guild)
        embed_basic = {
            "title": "Twilight has joined {}!".format(guild.name),
            "color": 0x11C5E5
        }
        embed = discord.Embed(**embed_basic)
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)
        channel: discord.TextChannel = self.bot.get_channel(707431591051264121)
        await channel.send(embed=embed)

    @command()
    @is_owner()
    async def load(self, ctx: Context, cog: str):
        self.bot.load_extension(cog)
        await ctx.send(content=f"Loaded `{cog}`")

    @command()
    @is_owner()
    async def unload(self, ctx: Context, cog: str):
        if cog.lower() == "core":
            await ctx.send(content="Mate... what are you doing?")
            return
        self.bot.unload_extension(cog)
        await ctx.send(content=f"Unloaded `{cog}`")

    @command()
    @is_owner()
    async def cogs(self, ctx: Context):
        cogs = self.bot.grab_cogs()
        embed = self.embed.create(ctx, title="Cogs")
        cogs_list = []
        for key, value in cogs.items():
            _list = []
            _list.append(key)
            _list.append(value)
            # Not the prettiest thing ever but it'll work...
            cogs_list.append(_list)
        embed.description = box(
            tabulate(cogs_list, ("Cog Name", "Loaded")), "md")
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        self.mod.teardown(guild)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("core")


def setup(bot: Twilight):
    bot.add_cog(Core(bot))
