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

import json
import logging
import typing
from contextlib import contextmanager
from os import path

import discord
from discord.ext import commands

from . import Embed, edit_guild_settings, get_guild_settings

log = logging.getLogger("mutes-api")
if path.exists("./cogs/mutes.json"):
    mutes_path = "./cogs/mutes.json"
else:
    from twi_secrets import MUTES_PATH as mutes_path


Member = typing.Union[discord.Member, discord.User]


@contextmanager
def edit_member_settings(user: Member):
    """|context manager|

    Open the mutes path and append roles to it

    Parameters
    ----------
    user: :class:`Member`
        The member to get settings for
    """
    try:
        with open(mutes_path) as fp:
            member_set = json.load(fp)
        member: list = member_set.get(str(user.id), False)
        if member is False:
            member = []

        yield member
    finally:
        member_set[str(user.id)] = member
        with open(mutes_path, "w") as fp:
            json.dump(member_set, fp, indent=4)


async def mute(
    ctx: commands.Context, user: Member,
    reason: str = None, remove_roles: bool = True
) -> str:
    """|coro|

    Mute a member

    Parameters
    ----------
    ctx: :class:`Context`
        The context of the command
    user: :class:`Member`
        The user to mute
    reason: Optional[:class:`str`]
        Reason for the mute
    remove_roles: :class:`bool`
        Whether or not to remove the user's roles
    """
    guild: discord.Guild = ctx.guild
    role = guild.get_role(get_guild_settings(guild)["muted_role"])
    if not role:
        return (
            "You don't have a muted role set up!"
            f"\nUse `{ctx.prefix}muteset role <id>` to setup a role!"
        )
    await user.add_roles(role, reason=reason)
    if remove_roles:
        with edit_member_settings(user=user) as mem:
            for role in user.roles:
                try:
                    await user.remove_roles(role, reason=reason)
                except discord.Forbidden:
                    log.info(
                        f"Could not remove {role.name} from {user.name}...")
                else:
                    mem.append(role.id)
    await modlog(ctx=ctx, user=user, action="Mute", reason=reason)
    return f"Muted {user.name}!"


async def unmute(
    ctx: commands.Context, user: Member,
    remove_roles: bool
) -> str:
    """|coro|

    Unmute a user

    Parameters
    ----------
    ctx: :class:`Context`
        Context of the command
    user: :class:`Member`
        The user being unmuted
    remove_roles: :class:`bool`
        Whether or not to add the roles back or not

    Returns
    -------
    str
        The message to send
    """
    guild: discord.Guild = ctx.guild
    role = guild.get_role(get_guild_settings(guild)["muted_role"])
    if not role:
        return (
            "You don't have a muted role!"
            f"\nUse `{ctx.prefix}muteset role <id>` to setup a role!"
        )
    await user.remove_roles(role)
    if remove_roles:
        with edit_member_settings(user=user) as mem:
            for role in mem:
                try:
                    await user.add_roles(guild.get_role(role))
                except discord.Forbidden:
                    log.info(f"Could not add role `{role}`")
                else:
                    mem.remove(role)
    modlog(ctx=ctx, user=user, action="Unmute", reason=None)
    return f"Unmuted {user.name}!"


async def kick(
    ctx: commands.Context,
    user: Member,
    reason: str = None,
):
    """|coro|

    Ban a user from the guild

    Parameters
    ----------
    ctx: :class:`Context`
        The context of the command
    user: :class:`Member`
        The member to kick
    reason: :class:`str`
        The reason for the kick
    """
    try:
        await ctx.guild.kick(user, reason=reason)
    except discord.Forbidden:
        log.info(f"Could not kick {user}")
        return f"I could not kick {user}!"
    else:
        await modlog(ctx=ctx, user=user, action="Kick", reason=reason)
    return f"Kicked {user}"


async def ban(
    ctx: commands.Context,
    user: Member,
    reason: str = None
):
    """|coro|

    Ban a user from the guild

    Parameters
    ----------
    ctx: :class:`Context`
        The context of the command
    user: :class:`Member`
        The member to ban
    reason: :class:`str`
        The reason for the ban
    """
    try:
        await ctx.guild.ban(user, reason=reason)
    except discord.Forbidden:
        err = f"I could not ban {user}!"
        log.info(err)
        return err
    else:
        await modlog(ctx=ctx, user=user, action="Ban", reason=reason)
    return f"Banned {user}"


async def unban(
    ctx: commands.Context,
    user: int,
    reason: str = None
):
    bans = await ctx.guild.bans()
    bans = [be.user for be in bans]
    user = discord.utils.get(bans, id=user)
    if not user:
        return "Hm, that user doesn't seem to be banned!"
    try:
        await ctx.guild.unban(user, reason=reason)
    except discord.HTTPException:
        return "Hm, something went wrong unbanning that user"
    else:
        await modlog(
            ctx=ctx,
            user=user,
            action="Unban",
            reason=reason
        )
    return f"Unbanned {user}"


async def modlog(
    ctx: commands.Context, user: Member,
    action: str, reason: str = None
):
    """|coro|

    Log a message to the modlog

    Parameters
    ----------
    action: :class:`str`
        The action you are logging
        If the action is a ban it will set that as the action
    user: :class:`Member`
        The user who had the action done to
        This will set this as the member in the log
    ctx: :class:`Context`
        Context of the command
    reason: :class:`str`
        Optional reason for the log
        Defaults to `None`
    """
    channel = ctx.bot.get_channel(get_guild_settings(ctx.guild)["modlog"])
    if not channel:
        # Since we've gotten here it's fair to assume that the channel was set
        # but the channel matching the id has been removed
        # So enter into the settings and set it to `None`
        log.info(f"{ctx.guild.name} has no modlog channel")
        with edit_guild_settings(ctx.guild) as session:
            session["modlog"] = None
        return
    embed = Embed.create(
        ctx=ctx, title=action.capitalize(),
        description=f"{user.name} was {action}(ed) by {ctx.author.name}",
        author=f"{ctx.guild.name} Moderation log", author_url=ctx.guild.icon_url
    )
    for key, value in {"Member": user.name, "Moderator": ctx.author.name, "Reason": reason}:
        if value is not None:
            embed.add_field(name=key, value=value)
    await channel.send(embed=embed)
