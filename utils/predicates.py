# Gonna have this since I'd like a message and reaction predicate :D

import discord
from discord.ext import menus, commands
import typing

__all__ = ["ReactionPred", ]
__author__ = "Jojo#7791"
__version__ = "0.1.0"


class ReactionPred(menus.Menu):
    """A reaction predicate working with discord.ext.menus

    Attributes
    ----------
    confirm: :class:`bool`
        A boolean stating Yes/No from the author.
        Defaults to `False`
    """

    def __init__(self, message: typing.Union[str, discord.Embed], timeout: float = 15.0, delete: bool = False):
        self.msg = message
        self.confirm = False
        super().__init__(timeout=timeout, delete_message_after=delete, clear_reactions_after=True)

    async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel):
        if isinstance(self.msg, discord.Embed):
            return await channel.send(embed=self.msg)
        else:
            return await channel.send(content=self.msg)

    async def prompt(self, ctx: commands.Context, channel: typing.Optional[discord.TextChannel] = None):
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
