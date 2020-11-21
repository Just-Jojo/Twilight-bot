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
from .utils.basic_utils import (
    moderator, administrator, Moderation,
    guild_owner, Getters, humanize_timedelta
)
from .utils.converter import RawUserIds

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


class Core(Cog):
    def __init__(self, bot: Twilight):
        self.bot = bot

    @command()
    async def ping(self, ctx):
        """Pong."""
        await ctx.send("Pong.")

    # @command()
    # @is_owner()
    # async def sudo(self, ctx: Context, user: discord.Member, *, command):
    #     pass

    @group(name="set")
    @guild_owner()
    @guild_only()
    async def _set(self, ctx: Context):
        """Set up Twilight"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

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
        result = Moderation.add_role(self, ctx.guild, role_type, role)
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
        result = Moderation.remove_role(self, ctx.guild, role_type)
        await ctx.send(content=result)

    @command(name="reload", aliases=["cu", "update"])
    @is_owner()
    async def _reload(self, ctx: Context, cog: str):
        """Reload a cog"""
        result = self.bot.reload_extension(cog)
        await ctx.send(result)

    @command()
    @is_owner()
    async def shutdown(self, ctx: Context):
        """Shuts Twilight down"""
        await ctx.send("Shutting down Twilight")
        await asyncio.sleep(2)
        await self.bot.shutdown(restart=False)

    @command()
    @is_owner()
    async def restart(self, ctx: Context):
        """Attempts to restart the bot"""
        await ctx.send("Restarting...")
        await asyncio.sleep(2)
        await self.bot.shutdown(restart=True)

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
        if len(self.bot.last_exception) > 1990:
            return await ctx.send("I can't send the traceback as it's over 2000 characters long")
        await ctx.send(self.bot.last_exception)

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
        embed = Embed.create(self, ctx, title="Uptime!",
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
        result = Moderation.announcement_set(self, False, ctx.guild, channel)
        await ctx.send(content=result)

    @announceset.command()
    async def _remove(self, ctx: Context):
        """Remove the announcement channel"""
        result = Moderation.announcement_set(self, True, ctx.guild)
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
        await self.announce_to_guilds(embed)

    async def announce_to_guilds(self, message: discord.Embed):
        channels = Getters.get_all_announce()
        for channel in channels:
            if channel is not None:
                chan = self.bot.get_channel(channel)
                await chan.send(embed=message)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        Moderation.setup(self, guild)
        embed_basic = {
            "title": "Twilight has joined {}!".format(guild.name),
            "color": 0x11C5E5
        }
        embed = discord.Embed(**embed_basic)
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)
        channel: discord.TextChannel = self.bot.get_channel(707431591051264121)
        await channel.send(embed=embed)

    @Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        Moderation.teardown(self, guild)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("core")


def setup(bot: Twilight):
    bot.add_cog(Core(bot))
