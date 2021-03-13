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

import asyncio

import discord
from discord.ext import commands, menus


__all__ = ["ReactionPredicate", "message_pred"]


class ReactionPredicate(menus.Menu):
    """Custom reaction predicate"""

    def __init__(self, msg: str):
        self.msg = msg
        self._confirm = False
        super().__init__(
            timeout=15.0, delete_message_after=False, clear_reactions_after=False
        )

    async def prompt(self, ctx: commands.Context):
        await self.start(ctx, channel=ctx.channel, wait=True)
        return self._confirm

    @property
    def confirm(self):
        return self._confirm

    async def send_initial_message(self, ctx, channel):
        return await ctx.send(content=self.msg)

    @menus.button("\N{WHITE HEAVY CHECK MARK}")
    async def on_check(self, payload):
        self._confirm = True
        self.stop()

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload):
        self.stop()  # `confirm` is already false


async def message_pred(ctx: commands.Context) -> bool:
    ret = False

    def inner(m: discord.Message):
        return (
            m.author.id == ctx.author.id
            and m.channel.id == ctx.channel.id
            and m.content.lower().startswith(("y", "n"))
        )

    bot = ctx.bot
    try:
        result = await bot.wait_for("message", check=inner, timeout=15.0)
    except asyncio.TimeoutError:
        return False
    else:
        # This will return True for `yes` and False for `no`
        if result.content.lower.startswith("y"):
            ret = True
        return ret
