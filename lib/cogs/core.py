import discord
from discord.ext.commands import (
    command, Cog, is_owner, Context
)
import asyncio
from .utils.embed import Embed


class Core(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def ping(self, ctx):
        await ctx.send("Pong.")

    @command(name="reload", aliases=["cu", "update"])
    @is_owner()
    async def _reload(self, ctx: Context, cog: str):
        result = self.bot.reload_extension(cog)
        await ctx.send(result)

    @command()
    @is_owner()
    async def unload(self, ctx: Context, cog: str):
        result = self.bot.unload_extension(cog)
        await ctx.send(result)

    @command()
    @is_owner()
    async def load(self, ctx: Context, cog: str):
        result = self.bot.load_extension(cog)
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
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("core")


def setup(bot):
    bot.add_cog(Core(bot))
