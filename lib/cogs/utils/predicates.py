# Gonna have this since I'd like a message and reaction predicate :D

import discord
from discord.ext.commands import (Context,)
from typing import *


class MessagePredicate(Callable[[discord.Message], bool]):
    def __init__(self, predicate: Callable[["MessagePredicate", discord.Message], bool]):
        self._pred: Callable[
            [
                "MessagePredicate",
                discord.Message
            ],
            bool
        ] = predicate
        self.result = None

    def __call__(self, message: discord.Message = None) -> bool:
        return self._pred(self, message)

    @classmethod
    def same_context(
        cls,
        ctx: Optional[Context] = None,
        channel: Optional[discord.TextChannel] = None,
        user: Optional[discord.abc.User] = None
    ) -> "MessagePredicate":
        if ctx is not None:
            channel = channel or ctx.channel
            user = user or ctx.author
        return cls(
            lambda self, m: (user is None or user.id == m.author.id)
            and (channel is None or channel.id == m.channel.id)
        )

    @classmethod
    def yes_or_no(
        cls,
        ctx: Optional[Context] = None,
        channel: Optional[discord.TextChannel] = None,
        user: Optional[discord.abc.User] = None
    ) -> "MessagePredicate":
        same_context = cls.same_context(ctx, channel, user)

        def predicate(self: MessagePredicate, m: discord.Message):
            if not same_context(m):
                return False
            content = m.content.lower()
            if content in ("yes", "y"):
                self.result = True
            elif content in ("no", "n"):
                self.result = False
            else:
                return False
            return True
        return cls(predicate)


# class ReactionPredicate(Callable[[discord.Message], bool]):
#     def __init__(self, predicate: Callable[["ReactionPredicate", discord.Message]]):
#         pass
