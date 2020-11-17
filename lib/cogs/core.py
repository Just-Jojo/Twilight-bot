### ~~~ Basic Discord and other utilities imports ~~~ ###
import discord
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
        Moderation.setup(guild)

    @Cog.listener()
    async def on_guild_leave(self, guild: discord.Guild):
        Moderation.teardown(guild)

    @command()
    @is_owner()
    async def trace(self, ctx):
        """Sends the latest traceback error"""
        if self.bot.last_exception == None:
            return await ctx.send("No exceptions have occured yet!")
        if len(self.bot.last_exception) > 1990:
            return await ctx.send("I can't send the traceback as it's over 2000 characters long")
        await ctx.send(self.bot.last_exception)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("core")


def setup(bot):
    bot.add_cog(Core(bot))
