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
import typing

import discord
from discord.ext import commands, menus
import asyncio


__all__ = ["ReactionPred", "message_pred"]
__author__ = "Jojo#7791"
__version__ = "0.1.0"


async def message_pred(ctx: commands.Context) -> bool:
    """A basic message predicate

    Parameters
    ----------
    ctx: :class:`Context`
        Context used for the message.

    Returns
    -------
    bool
        True for Yes, False for No
    """

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
        return await ctx.send("Timed out!")
    else:
        # This will return True for `yes` and False for `no`
        return result.content.lower().startswith("y")


class ReactionPred(menus.Menu):
    """A reaction predicate working with discord.ext.menus

    Attributes
    ----------
    confirm: :class:`bool`
        A boolean stating Yes/No from the author.
        Defaults to `False`
    """

    def __init__(
        self,
        message: typing.Union[str, discord.Embed],
        timeout: float = 15.0,
        delete: bool = False,
    ):
        self.msg = message
        self.confirm = False
        super().__init__(
            timeout=timeout, delete_message_after=delete, clear_reactions_after=True
        )

    async def send_initial_message(
        self, ctx: commands.Context, channel: discord.TextChannel
    ):
        if isinstance(self.msg, discord.Embed):
            return await channel.send(embed=self.msg)
        else:
            return await channel.send(content=self.msg)

    async def prompt(
        self,
        ctx: commands.Context,
        channel: typing.Optional[discord.TextChannel] = None,
    ):
        """Starts the prompt for the Predicate

        Parameters
        ----------
        ctx: :class:`Context`
            The context used to invoke the prompt
        channel: :class:`Optional[discord.TextChannel]`
            The channel used to send the inital message
            Defaults to `ctx.channel`
        Returns
        -------
        :class: `bool`
            Whether the user has confirmed or denied the action
        """
        if ctx.guild is None or channel is None:
            channel = ctx.channel
        await self.start(ctx=ctx, channel=channel, wait=True)
        return self.confirm

    @menus.button("\N{WHITE HEAVY CHECK MARK}")
    async def on_confirm(self, payload):
        self.confirm = True
        self.stop()

    @menus.button("\N{CROSS MARK}")
    async def on_deny(self, payload):
        self.confirm = False
        self.stop()
