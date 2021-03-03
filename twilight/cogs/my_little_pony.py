import logging

import discord
from discord.ext import commands

from .abc import Cog


class MyLittlePony(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("twilight.cogs.MLP")

    @commands.command()
    async def gen5(self, ctx):
        """Stuff about Gen 5"""
        await ctx.send(
            "While MLP G5 is coming out soon(ish) Jojo"
            " (the developer of this bot) has no intentions of shifting this project over to it (yet :p)"
        )


def setup(bot: "Twilight"):
    bot.add_cog(MyLittlePony(bot))
