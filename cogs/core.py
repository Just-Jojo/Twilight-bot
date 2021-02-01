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
from datetime import datetime
from platform import python_version as pver
from typing import *


import discord
from bot import Twilight  # Type hinting
from discord import __version__ as dpyversion
from discord.ext import commands
from utils import (Embed, TwilightEmbedMenu, admin, box, guild_setup,
                   humanize_timedelta, teardown)

from cogs.mixin import BaseCog

information = r"""
    Twilight is a Discord bot written in Python by Jojo#7791.
    Twilight is designed mostly for MLP features but also has moderation tools.

    \~\~\~\~\~\~

    To invite Twilight to your server, use `>invite` and click on the link.
    You can find the [support](https://discord.gg/JmCFyq7) server
"""


class Core(BaseCog):
    """Core commands
    """

    def __init__(self, bot: Twilight):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong."""
        await ctx.message.reply("Pong.", mention_author=False)

    @commands.command()
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
            ctx, title="Invite Twilight to your server!", description=description
        )
        await ctx.send(embed=embed)

    @commands.command()
    async def info(self, ctx):
        """Twilight's info"""
        embed = Embed.create(
            ctx, title="Twilight bot Info", footer="Twilight bot Info"
        )
        embed.add_field(
            name="<:dpy:779489296389767208>", value="Version: `{}`".format(dpyversion)
        )
        embed.add_field(
            name="<:twilight:734586922910875750>", value="Version: `{}`".format(self.bot.__version__)
        )
        embed.add_field(
            name="<:python:760888220228780063>", value="Version: `{}`".format(pver())
        )
        embed.add_field(name="Info", value=information, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx):
        """Get Twilight's uptime"""
        since = self.bot.uptime.strftime("%Y-%m-%D %H:%M:%S")
        uptime = datetime.utcnow() - self.bot.uptime
        uptime_str = humanize_timedelta(
            timedelta=uptime) or "Less than one second"
        # await ctx.send("Been up for: **{}** (since {} UTC)".format(uptime_str, since))
        embed = Embed.create(ctx, title="Uptime!",
                             footer="Twilight uptime")
        embed.add_field(name="Total time", value="**{}**".format(uptime_str))
        embed.add_field(name="Up since", value="**{}**".format(since))
        await ctx.send(embed=embed)

    @commands.command(name="license")
    async def twilight_license(self, ctx):
        """Twilight's license"""
        embed = Embed.create(
            self, ctx, title="Twilight bot License",
            description=self.bot.license, footer="Twilight bot License :D"
        )
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        if guild.id in self.bot.guild_blocklist:
            await guild.leave()
        guild_setup(guild)
        embed_basic = {
            "title": "Twilight has joined {}!".format(guild.name),
            "color": 0x11C5E5
        }
        embed = discord.Embed(**embed_basic)
        embed.set_author(name=guild.name, icon_url=guild.icon_url)
        embed.set_thumbnail(url=guild.icon_url)
        channel: discord.TextChannel = self.bot.get_channel(707431591051264121)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        teardown(guild)


def setup(bot: Twilight):
    bot.add_cog(Core(bot))
