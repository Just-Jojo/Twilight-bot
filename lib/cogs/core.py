import discord
from discord.ext.commands import (
    command, Cog, is_owner, Context
)
import asyncio


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

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("core")


def setup(bot):
    bot.add_cog(Core(bot))
