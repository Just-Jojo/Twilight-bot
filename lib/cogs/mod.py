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
### ~~~ Base Discord and other imports ~~~ ###
import discord
from discord.ext.commands import (
    command, Context, check, Cog,
    guild_only
)
from typing import Optional

### ~~~ Utils and others ~~~  ###
from .utils.basic_utils import (
    moderator, administrator,
    Moderation
)
from ..bot import Twilight


class Mod(Cog):
    """self.mod to make sure everything runs smoothly on your Guild"""

    def __init__(self, bot: Twilight):
        self.bot = bot
        self.mod = Moderation

    @command()
    @moderator()
    @guild_only()
    async def ban(self, ctx: Context, user: discord.Member, days: Optional[int] = 0, *, reason: str = None):
        _reason = "Action requested by {} ({})\n".format(
            ctx.author, ctx.author.id)
        if reason is not None:
            _reason += reason
        result = await self.mod.ban_kick(ctx, user, "ban", _reason, days)
        await ctx.send(content=result)

    @command()
    @moderator()
    @guild_only()
    async def kick(self, ctx: Context, user: discord.Member, days: Optional[int] = 0, *, reason: str = None):
        _reason = "Action requested by {} ({})\n".format(
            ctx.author, ctx.author.id)
        if reason is not None:
            _reason += reason
        result = await self.mod.ban_kick(ctx, user, "kick", _reason, days)
        await ctx.send(result)

    @command()
    @moderator()
    @guild_only()
    async def mute(self, ctx: Context, user: discord.Member, channel: discord.TextChannel = None):
        """Mute a member in a channel

        Example:
        `>mute @Jojo #testing`"""
        if channel is None:
            channel = ctx.channel
        result = await self.mod.mute_member(ctx, user, channel)
        await ctx.send(result)

    @command()
    @moderator()
    @guild_only()
    async def unmute(self, ctx: Context, user: discord.Member, channel: discord.TextChannel = None):
        """Unmute a member in a channel

        Example:
        `>unmute @Jojo #testing"""
        if channel is None:
            channel = ctx.channel
        result = await self.mod.unmute_member(ctx=ctx, user=user, channel=channel)
        await ctx.send(result)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mod")


def setup(bot: Twilight):
    bot.add_cog(Mod(bot))
