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
import datetime
import json
from os import path
from typing import *

import discord
from discord.ext.commands import Context, check

from .embed import Embed

if path.exists("./cogs/settingstings.json"):
    json_path = "./cogs/settingstings.json"
else:
    from twi_secrets import TWI_SETTINGS_PATH as json_path

__version__ = "0.1.0"
# Also whoever wrote the humanize_timedelta, I didn't make that
__author__ = ["Jojo#7791", ]


def moderator():
    """A decorator that checks if a user has a moderator role

    Returns
    -------
    bool
        If the user is a mod, admin, or the bot owner this will return True, allowing them to use the command
        Otherwise it will return False, raising a check failure
    """
    async def inner(ctx: Context):
        if ctx.guild is None:
            return False  # Can't use mod commands in dms
        if ctx.author.id == 544974305445019651:  # allow me to use mod commands
            return True
        settings = get_guild_settings(ctx.guild)  # Grab the settings...
        mod = settings.get("mod")  # The role id...
        admin = settings.get("admin")
        if admin:
            if ctx.guild.get_role(admin) in ctx.author.roles:
                return True
        if mod:
            # And grab the role to see if the author has it
            return ctx.guild.get_role(mod) in ctx.author.roles
        else:
            return False
    return check(inner)


def administrator():
    """A decorator that checks if a user has an administrator role

    Returns
    -------
    bool
        If the user has an adminstrator role this will return True, allowing them to use that command
        Otherwise it will return False, raising a check failure
    """
    async def inner(ctx: Context):
        if ctx.guild is None:
            return False
        if ctx.author.id == 544974305445019651:
            return True
        settings = get_guild_settings(ctx.guild)
        admin = settings.get("admin")
        if admin:
            return ctx.guild.get_role(admin) in ctx.author.roles
        else:
            return False
    return check(inner)


async def is_mod(ctx: Context, user: discord.Member):
    """|coro|

    A function testing whether a user has a Mod role

    Parameters
    ----------
    ctx: :class:`Context`
        Context of the check
    user: Optional[:class:`discord.Member`]
        The user to run the check on
        Defaults to the Context's author

    Returns
    -------
    bool
        If the user is a mod, admin, or bot owner it will return True
        Otherwise it will return False
    """
    if ctx.guild is None:
        return False
    if await ctx.bot.is_owner(user):
        return True
    settings = get_guild_settings(ctx.guild)
    mod = settings.get("mod")
    admin = settings.get("admin")
    if admin:
        if ctx.guild.get_role(admin) in user.roles:
            return True
    if mod:
        return ctx.guild.get_role(mod) in user.roles
    return False


async def is_admin(ctx: Context, user: Optional[discord.Member] = None):
    """|coro|

    A function testing whether a user has an Admin role

    Parameters
    ----------
    ctx: :class:`Context`
        Context of the check
    user: Optional[:class:`discord.Member`]
        The user to check
        Defaults to the Context's author

    Returns
    -------
    bool
        If the user is an Admin it will return True
        Otherwise it will return False
    """
    if user is None:
        user = ctx.author
    if ctx.guild is None:
        return False
    if await ctx.bot.is_owner(ctx.author):
        return True
    settings = get_guild_settings(ctx.guild)
    admin = settings.get("admin")
    if admin:
        return ctx.guild.get_role(admin) in ctx.author.roles
    return False


async def tick(message: discord.Message):
    """Add a checkmark to a message

    Parameters
    ----------
    message: :class:`discord.Message`
        The message to add the reaction to
    """
    await message.add_reaction("\N{WHITE HEAVY CHECK MARK}")


def guild_owner():
    """A guild owner check

    Returns whether or not the author is a guild or bot owner

    Returns
    -------
    bool
        If the user owns the guild or the bot this will return True
        Otherwise it will return False, raising a check failure
    """
    async def inner(ctx: Context):
        if ctx.author.id == 544974305445019651:  # I need to be able to use guild_owner only commands
            return True
        return ctx.guild is not None and ctx.author == ctx.guild.owner
    return check(inner)


def humanize_timedelta(
    *, timedelta: Optional[datetime.timedelta] = None, seconds: Optional[SupportsInt] = None
) -> str:  # I didn't steal this from red, how silly that would have been :p
    try:
        obj = seconds if seconds is not None else timedelta.total_seconds()
    except AttributeError:
        raise ValueError(
            "You must provide either a timedelta or a number of seconds")

    seconds = int(obj)
    periods = [
        ("year", "years", 60 * 60 * 24 * 365),
        ("month", "months", 60 * 60 * 24 * 30),
        ("day", "days", 60 * 60 * 24),
        ("hour", "hours", 60 * 60),
        ("minute", "minutes", 60),
        ("second", "seconds", 1),
    ]

    strings = []
    for period_name, plural_period_name, period_seconds in periods:
        if seconds >= period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 0:
                continue
            unit = plural_period_name if period_value > 1 else period_name
            strings.append(f"{period_value} {unit}")

    return ", ".join(strings)


def box(text: str, lang: str = "") -> str:
    """Put content in a code block

    Parameters
    ----------
    text: :class:`str`
        The text to place in the code block
    lang: :class:`str`
        The language for the block
        Defaults to an empty string
    """
    ret = "```{}\n{}```".format(lang, text)
    return ret


def guild_setup(guild: discord.Guild) -> None:
    r"""Set up a Guild with the default settings

    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild object to setup
    """
    with open(json_path, "r") as fp:
        settings: dict = json.load(fp)

    if str(guild.id) in settings.keys():
        print(f"{guild.name} was in the database already.")
        return
    settings[str(guild.id)] = {
        "admin": [],
        "mod": [],
        "announce_channel": None,
        "modlog": None,
        "prefixes": []  # prefixes: list(str)
    }
    with open(json_path, "w") as fp:
        json.dump(settings, fp, indent=4)
    print("Added {} ({}) to Twilight's settings".format(guild.name, guild.id))


def get_settings() -> dict:
    """Grab the entire settings dict

    Returns
    -------
    dict
        The settings dictionary
    """
    with open(json_path) as fp:
        return json.load(fp)


def write_settings(settings: dict):
    """Write the settings dict to a JSON file

    Parameters
    ----------
    settings: :class:`dict`
        The settings dictionary
    """
    with open(json_path, "w") as fp:
        json.dump(settings, fp, indent=4)


def get_guild_settings(guild: discord.Guild) -> dict:
    """Get the settings dict for a guild

    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild object to grab the settings for

    Returns
    -------
    dict
        The dictionary settings for the guild
    """
    guild_id = str(guild.id)
    with open(json_path) as fp:
        settings = json.load(fp)
    if guild_id not in settings.keys():
        guild_setup(guild)
    return settings[guild_id]


def teardown(guild: discord.Guild):
    """Remove a guild from Twilight's settings

    This should only be called when leaving a guild

    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild to remove data from
        In the case that the guild wasn't in Twilight's database
    """
    guild_id = str(guild.id)
    settings = get_settings()
    if guild_id not in settings.keys():
        # This will *only* happen if the setup fails to trigger or a Twily was in a guild before this was implemented
        print(
            f"{guild.name} was not in Twilight's database so I did not remove any data")
        return
    del settings[guild_id]
    print(f"Removed data for {guild.name}")
    write_settings(settings=settings)


def role_setup(role_type: bool, guild: discord.Guild, role: int) -> str:
    """Set an admin/mod role for a guild

    Parameters
    ----------
    role_type: :class:`bool`
        The type of role to setup

        If it is True the type will be "mod"
        If it is False the type will be "admin"
    guild: :class:`discord.Guild`
        The guild to set the role for
    role: :class:`int`
        The id of the role being setup

    Returns
    -------
    str
        The message confirming that the setup was sucessful
    """
    if role_type:
        rtype = "mod"
    else:
        rtype = "admin"
    # Don't worry about KeyErrors here as the grabber will setup a guild not in the database
    settings = get_guild_settings(guild)
    settings[rtype].append(role)
    base_settings = get_settings()
    base_settings[str(guild.id)] = settings
    write_settings(settings=base_settings)
    return f"Added that role as a/an {rtype} role"


def announce_set(guild: discord.Guild, channel: int) -> str:
    """Set an announcement channel for a guild

    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild to set the announcement channel for
    channel: :class:`int`
        The channel id to setup

    Returns
    -------
    str
        The confirmation message
    """
    settings = get_guild_settings(guild)
    settings["announce_channel"] = channel
    base_settings = get_settings()
    base_settings[str(guild.id)] = settings
    write_settings(settings=base_settings)
    return "Set that channel as an announcement channel. You will now be notified of changes/features from Twilight via that channel"


def modlog_add(guild: discord.Guild, channel: int) -> str:
    """Add a channel as the modlog channel

    Parameters
    ----------
    guild: :class:`discord.Guild`
        The guild to set the modlog channel
    channel: :class:`int`
        The channel id for the channel

    """
    guild_settings = get_guild_settings(guild)
    guild_settings["modlog"] = channel
    settings = get_settings()
    settings[str(guild.id)] = guild_settings
    write_settings(settings=settings)
    return "Set that channel as the modlog channel. Moderation actions will now be logged there"
