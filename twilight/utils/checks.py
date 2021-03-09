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

import os.path
import typing
import json


__all__ = ["admin", "guild_owner", "mod"]
Role = typing.Literal["admins", "mods"]
RoleList = typing.List[int]

if os.path.exists("./data/guild_data.json"):
    path = "./data/guild_data.json"
else:
    from twi_secrets import GUILD_DATAPATH as path


def get_role(guild: discord.Guild, role: Role) -> RoleList:
    ret = []
    with open(path) as fp:
        items = json.load(fp)
    if role == "admins":
        ret = items["admins"]
    mods = items["mods"]
    if ret:
        ret.extend(mods)
    else:
        ret = mods
    return ret


def guild_owner():
    """Checks if a user owns the guild"""

    async def pred(ctx: commands.Context):
        return ctx.guild is not None and ctx.author == ctx.guild.owner

    return commands.check(pred)


def admin():
    """Checks if a user is an admin or higher"""

    async def pred(ctx: commands.Context):
        if ctx.guild is None:
            return False
        if await ctx.bot.is_owner(ctx.author):
            return True
        roles = get_role(ctx.guild, "admins")
        for role in roles:
            _ = ctx.guild.get_role(role)
            if _ in ctx.author.roles:
                return True
        return False

    return commands.check(pred)


def mod():
    """Checks if the user is a mod or higher"""

    async def pred(ctx: commands.Context):
        if ctx.guild is None:
            return False
        if await ctx.bot.is_owner(ctx.author):
            return True
        roles = get_role(ctx.guild, "mods")
        for role in roles:
            _ = ctx.guild.get_role(role)
            if _ in ctx.author.roles:
                return True
        return False

    return commands.check(pred)
