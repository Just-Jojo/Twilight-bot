### ~~~ General Discord and other utils imports ~~~ ###
import discord
from discord.ext import commands
import asyncio
import random
from typing import *
### ~~~ Twilight bot utils imports ~~~ ###
from bot import Twilight  # Type hinting
from utils import admin, mod, Embed, rps_game
from .mixin import BaseCog


class General(BaseCog):
    """General, fun commands"""

    def __init__(self, bot: Twilight):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, channel: Optional[discord.TextChannel], *, message):
        """Have the bot repeat you"""
        # await ctx.send(message)
        channel = channel or ctx.channel
        await channel.send(message)

    @commands.command()
    async def roll(self, ctx, amount: int = 6):
        """Roll a dice"""
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

    @commands.command()
    async def flip(self, ctx):
        """Flip a coin"""
        heads_tails = ["HEADS", "TAILS"]
        await ctx.send("*Flips a coin and..... {}!!!*".format(random.choice(heads_tails)))

    @commands.command(aliases=["rps", ])
    async def rockpaperscissors(self, ctx, choice: str):
        """Play a game of rock paper scissors with Twilight"""
        await rps_game(ctx, choice)


def setup(bot: Twilight):
    bot.add_cog(General(bot))
