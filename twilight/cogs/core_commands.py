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
import logging
import random

import discord
from discord.ext import commands

from .abc import Cog

_license_info = (
    "Twilight is a custom Discord bot written in Python by Jojo#7791\n"
    "Her source code is licensed under MIT and is available at https://github.com/Just-Jojo/Twilight-Bot"
)


class Core(Cog):
    """Core commands and others"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("twilight.cogs.Core")

    @commands.command()
    async def licenseinfo(self, ctx):
        """Get information about Twilight's license"""
        await ctx.reply(_license_info)

    @commands.command()
    async def ping(self, ctx):
        await ctx.reply("Pong.")

    @commands.command()
    async def flip(self, ctx):
        """Flip a coin!"""
        msg = "Flipping a coin..."
        await ctx.send(msg)
        await asyncio.sleep(1)
        await ctx.send(f"{random.choice(['Heads', 'Tails'])}!")
