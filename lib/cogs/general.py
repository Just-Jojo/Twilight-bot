### ~~~ General Discord and other utils imports ~~~ ###
import discord
from discord.ext.commands import (
    Context, command, Cog, is_owner
)
import asyncio
import random
from typing import Optional
### ~~~ Twilight bot utils imports ~~~ ###
from ..bot import Twilight  # Type hinting
from .utils.embed import Embed
from .utils.basic_utils import administrator, moderator
from .utils.rps import rock_paper_scissors


class General(Cog):
    """General commands"""

    def __init__(self, bot: Twilight):
        self.bot = bot

    @command()
    async def say(self, ctx: Context, channel: Optional[discord.TextChannel], *, message):
        """Have the bot repeat you"""
        await ctx.send(message)

    @command()
    async def roll(self, ctx: Context, amount: int = 6):
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

    @command()
    async def flip(self, ctx: Context):
        """Flip a coin"""
        heads_tails = ["HEADS", "TAILS"]
        await ctx.send("*Flips a coin and..... {}!!!*".format(random.choice(heads_tails)))

    @command(aliases=["rps", ])
    async def rockpaperscissors(self, ctx: Context, choice: str):
        """Play a game of rock paper scissors with Twilight"""
        await rock_paper_scissors(ctx, choice)

    @command()
    @is_owner()
    async def test(self, ctx: Context):
        """This is my testing command :D"""
        await ctx.send(ctx.command.help)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("general")


def setup(bot: Twilight):
    bot.add_cog(General(bot))
