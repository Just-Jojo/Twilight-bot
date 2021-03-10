"""
MIT License

Copyright (c) 2020-2021 Jojo#7711

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


__all__ = ["admin", "guild_owner", "mod"]
Role = typing.Literal["admins", "mods"]
RoleList = typing.List[int]


def guild_owner():
    """Checks if the author is the guild's owner"""

    async def pred(ctx: commands.Context):
        return ctx.guild is not None and ctx.guild.owner == ctx.author

    return commands.check(pred)


def mod():
    """Checks if the author is a mod or higher"""

    async def pred(ctx: commands.Context):
        return await checker(ctx, False)

    return commands.check(pred)


def admin():
    """Checks if the author is an admin"""

    async def pred(ctx: commands.Context):
        return await checker(ctx, True)

    return commands.check(pred)


async def checker(ctx: commands.Context, ad_only: bool) -> bool:
    """Repeating logic is bad"""

    bot = ctx.bot
    guild = ctx.guild
    if guild is None:
        return False
    if await bot.is_owner(ctx.author):
        return True
    conf = bot.guild_config
    author_roles = [x.id for x in ctx.author.roles if x != guild.default_role]
    to_check = conf[str(guild.id)]["admins"]
    if not ad_only:
        to_check.extend(conf[str(guild.id)]["mods"])
    for role in to_check:
        if role in author_roles:
            return True
    return False
