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
import discord
from discord.ext import commands
import typing

from cogs.mixin import BaseCog
from utils import is_mod, get_guild_settings, RawUserIds
from utils.mutes_api import mute, unmute, ban, unban, kick


class Mod(BaseCog):
    """Moderation commands to keep your guild clean"""

    @commands.command()
    async def mute(self, ctx, member: RawUserIds, *, reason: str = None):
        """Mute a user
        """
        remove_roles = get_guild_settings(ctx.guild)["mute_remove"]
        result = await mute(ctx=ctx, user=member, reason=reason, remove_roles=remove_roles)
        await ctx.send(result)

    @commands.command()
    async def unmute(self, ctx, member: RawUserIds):
        """Unmute a user
        """
        remove_roles = get_guild_settings(ctx.guild)["mute_remove"]
        result = await unmute(ctx=ctx, user=member, remove_roles=remove_roles)
        await ctx.send(result)

    @commands.command()
    async def ban(self, ctx, user: RawUserIds, *, reason: str):
        """Ban a user
        """
        result = await ban(ctx, user, reason)
        await ctx.send(result)

    @commands.command()
    async def unban(self, ctx, user: RawUserIds, *, reason: str):
        """Unban a user
        """
        result = await unban(ctx, user, reason)
        await ctx.send(result)

    @commands.command()
    async def kick(self, ctx, user: RawUserIds, *, reason):
        """Kick a user
        """
        result = await kick(ctx, user, reason)
        await ctx.send(result)

    async def cog_check(self, ctx: commands.Context):
        return await is_mod(ctx, ctx.author)  # This comes in handy


def setup(bot):
    bot.add_cog(Mod(bot))
