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

from abc import ABC

import discord
from discord.ext import commands

import logging

from ...utils import is_mod


class Meta(ABC):
    bot: commands.Bot
    log: logging.Logger


class KickBanMixin(Meta):
    async def kick_user(self, ctx: commands.Context, user: discord.Member, reason: str):
        if await is_mod(ctx, user):
            return await ctx.send("That user is a mod!")
        if user == ctx.author:
            return await ctx.send("Don't kick yourself, you're doing awesome!")

        try:
            await ctx.guild.kick(user, reason=reason)
        except discord.Forbidden:
            await ctx.send("Hm, I couldn't kick that user")
        else:
            self.bot.dispatch("mod_event", ctx, "kick", user, reason)

    async def ban_user(self, ctx: commands.Context, user: discord.Member, reason: str):
        if await is_mod(ctx, user):
            return await ctx.send("That user is a mod!")
        if user == ctx.author:
            return await ctx.send("Don't ban yourself, you're doing great!")

        try:
            await ctx.guild.ban(user, reason=reason)
        except discord.Forbidden:
            await ctx.send("Hm, I couldn't ban that user")
        else:
            self.bot.dispatch("mod_event", ctx, "ban", user, reason)
