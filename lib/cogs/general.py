import discord
from discord.ext.commands import (
    Context, command, Cog
)
import asyncio
import random


class General(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command()
    async def say(self, ctx, *, message):
        """Have the bot repeat you"""
        await ctx.send(message)

    @command()
    async def roll(self, ctx, amount: int = 6):
        if amount < 2:
            await ctx.send("You can't roll a dice with less that 2 sides, silly")
        elif amount > 4000:
            await ctx.send(
                (
                    "Why would you make me A. roll that dice"
                    " B. Make me *read the result* C. Like you anymore?!"
                )
            )
        else:
            await ctx.send("🎲 {} 🎲".format(random.randint(1, amount)))

    @command()
    async def flip(self, ctx):
        await ctx.send("*Flips a coin and..... {}!!!*".format(random.choice(["HEADS", "TAILS"])))

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready():
            self.bot.cogs_ready.ready_up("core")


def setup(bot):
    bot.add_cog(General(bot))
