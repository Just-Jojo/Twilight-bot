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
SOFTWARE."""

### ~~~ Basic Discord and other utilities imports ~~~ ###
import discord
from discord import __version__ as dpyversion
from discord.ext import commands
from discord.ext.commands import (
    command, Cog, is_owner, Context, check, group
)
import asyncio
import json

### ~~~ Local imports ~~~ ###
from .utils.embed import Embed
from .utils.basic_utils import (
    moderator, administrator, Moderation
)


class Core(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ping(self, ctx):
        await ctx.send("Pong.")

    @group(name="set")
    @is_owner()
    async def _set(self, ctx: Context):
        """Set up Twilight"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @_set.command(aliases=('admin', ))
    async def administrator(self, ctx: Context, role: discord.Role):
        """Set the adminstrator role"""
        Moderation.add_role(ctx.gulid, "administrator", role)
        await ctx.send(
            content="Set up {} as the administrator role".format(role.mention),
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=False
            )
        )

    @command(name="reload", aliases=["cu", "update"])
    @is_owner()
    async def _reload(self, ctx: Context, cog: str):
        result = self.bot.reload_extension(cog)
        await ctx.send(result)

    @command()
    @is_owner()
    async def shutdown(self, ctx: Context):
        await ctx.send("Logging out")
        await self.bot.close()

    @command()
    async def invite(self, ctx):
        """Invite the bot to your server"""
        description = (
            "Invite for Twilight! [Here]"
            "(https://discord.com/api/oauth2/authorize?client_id=734159757488685126&permissions=470117622&scope=bot)"
            " is the link to add her to your server (Note,"
            " in order to add a bot to a server you must have the `adminstrator` permission)"
            "\nTo receive support, join the [Vanguard](https://discord.gg/JmCFyq7) support server"
            "\nThank you for checking out Twilight! <3"
        )
        embed = Embed.create(
            self, ctx, title="Invite Twilight to your server!", description=description
        )
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        Moderation.setup(self, guild)

    @Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        Moderation.teardown(self, guild)

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
        embed = Embed.create(
            self, ctx, title="Twilight bot Info", description="Version informations"
        )
        embed.add_field(
            name="discord.py version", value=dpyversion, inline=False
        )
        embed.add_field(
            name="Twilight bot version", value=self.bot.version, inline=False
        )
        await ctx.send(embed=embed)

    @command(name="license")
    async def _license(self, ctx):
        embed = Embed.create(
            self, ctx, title="Twilight bot License",
            description=self.bot.license, footer="Twilight bot License :D"
        )
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("core")


def setup(bot):
    bot.add_cog(Core(bot))
