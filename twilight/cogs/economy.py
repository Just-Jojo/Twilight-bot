"""
MIT License

Copyright (c) 2021 Jojo#7711

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

import logging
import random

import discord
from discord.ext import commands

import typing

from ..utils import Config
from .abc import Cog


def positive_int(arg: str) -> int:
    try:
        ret = int(arg)
    except ValueError:
        raise commands.BadArgument(f"{arg} is not an int")
    else:
        if ret <= 0:
            raise commands.BadArgument(f"{arg} is not positive")
    return ret


class Economy(Cog):
    """Twilight's economy system"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("twilight.cogs.Economy")
        self.config = Config("economy.json")

    @commands.cooldown(1, 300.0, commands.BucketType.user)
    @commands.command()
    async def work(self, ctx):
        """Get some bits (not bites, you're thinking of food)"""
        amount = random.randint(0, 200)
        if amount == 1:
            msg = "You gained one bit!"
        elif not amount:
            msg = "You didn't get any bits"
        else:
            msg = f"You gained {amount} bits"
        await self.config.set(ctx.author.id, self.config.get(ctx.author.id, 0) + amount)
        await ctx.send(msg)

    @commands.command()
    async def balance(self, ctx, user: typing.Optional[discord.Member] = None):
        """Check your balance"""
        if user is None:
            user = ctx.author
        amount = self.config.get(user.id, 0)
        if amount == 1:
            msg = f"{user.name}'s balance is one bit!"
        elif amount == 0:
            msg = f"{user.name}'s balance is zero bits!"
        else:
            msg = f"{user.name}'s balance is {amount} bits!"
        await ctx.send(msg)

    @commands.command()
    async def pay(self, ctx, user: discord.Member, amount: positive_int):
        """Give a user some bits!"""
        aamount = self.config.get(ctx.author.id, 0)
        if aamount <= 0 or aamount < amount:
            await ctx.send("You don't have enough bits to do this!")
        else:
            if amount == 1:
                msg = f"You gave {user.name} one bit!"
            else:
                msg = f"You gave {user.name} {amount} bits!"
            await ctx.send(msg)
            self.config[str(ctx.author.id)] -= amount
            await self.config.set(user.id, self.config.get(user.id, 0) + amount)


def setup(bot):
    bot.add_cog(Economy(bot))
