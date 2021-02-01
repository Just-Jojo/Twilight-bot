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
import random
import typing

import discord
from bot import Twilight  # Type hinting
from discord.ext import commands
from utils import Embed, admin, mod, rps_game

from .mixin import BaseCog


class General(BaseCog):
    """General, fun commands"""

    def __init__(self, bot: Twilight):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, channel: typing.Optional[discord.TextChannel], *, message):
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
