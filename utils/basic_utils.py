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
from discord.ext.commands import (
    Context, check
)
import json
from .embed import Embed
import datetime
from typing import *
from os import path

if path.exists("./cogs/settingstings.json"):
    json_path = "./cogs/settingstings.json"
else:
    from twi_secrets import TWI_SETTINGS_PATH as json_path

__all__ = ["moderator", "administrator", "tick", "box", "humanize_timedelta",
           "setup", "teardown", "role_setup", "announce_set", "modlog_add"]
__version__ = "0.1.0"
# Also whoever wrote the humanize_timedelta, I didn't make that
__author__ = ["Jojo#7791", ]


def moderator():
    """The check to see if the user is a mod"""
    async def inner(ctx: Context):
        if ctx.guild is None:
            return False  # Can't use mod commands in dms
        if ctx.author.id == 544974305445019651:  # allow me to use mod commands
            return True
        settings = get_guild_settings(ctx.guild)  # Grab the settings...
        mod = settings.get("mod")  # The role id...
        if mod:
            # And grab the role to see if the author has it
            return ctx.guild.get_role(mod) in ctx.author.roles
        else:
            return False
    return check(inner)


def administrator():
    """The check to see if the user is an admin"""
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


async def tick(message: discord.Message):
    """Add a checkmark to a message"""
    await message.add_reaction("\N{WHITE HEAVY CHECK MARK}")


def guild_owner():
    """Guild owner check in the discord.py library when?"""
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
    ret = "```{}\n{}```".format(lang, text)
    return ret


def setup(guild: discord.Guild) -> None:
    """Set up a Guild with the default settings"""
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
    """Grab the entire settings dict"""
    with open(json_path) as fp:
        return json.load(fp)


def write_settings(settings: dict):
    """Write the settings to a JSON file"""
    with open(json_path, "w") as fp:
        json.dump(settings, fp, indent=4)


def get_guild_settings(guild: discord.Guild) -> dict:
    """Get the settings for a guild"""
    guild_id = str(guild.id)
    with open(json_path) as fp:
        settings = json.load(fp)
    if guild_id not in settings.keys():
        setup(guild)
    return settings[guild_id]


def teardown(guild: discord.Guild):
    """Remove a guild from Twilight's settings"""
    guild_id = str(guild.id)
    with open(json_path) as fp:
        settings = json.load(fp)
    if guild_id not in settings.keys():  # This will *only* happen if the setup fails to trigger or a Twily was in a guild before this was implemented
        print(
            f"{guild.name} was not in Twilight's database so I did not remove any data")
        return
    del settings[guild_id]
    print(f"Removed data for {guild.name}")
    with open(json_path, "w") as fp:
        json.dump(settings, fp, indent=4)


def role_setup(role_type: bool, guild: discord.Guild, role: int) -> str:
    """Set an admin/mod role for a guild

    guild:discord.Guild: Guild to add
    role_type:bool: True = Mod False = Admin"""
    if role_type:
        rtype = "mod"
    else:
        rtype = "admin"
    # Don't worry about KeyErrors here as the grabber will setup a guild not in the database
    settings = get_guild_settings(guild)
    settings[rtype].append(role)
    with open(json_path) as fp:
        _set = json.load(fp)
    _set[str(guild.id)] = settings
    with open(json_path, "w") as fp:
        json.dump(_set, fp, indent=4)
    return f"Added that role as a/an {rtype} role"


def announce_set(guild: discord.Guild, channel: int) -> str:
    """Set an announcement channel for a guild

    guild:discord.Guild: the guild getting setup
    channel:int: the channel id for it
    """
    settings = get_guild_settings(guild)
    settings["announce_channel"] = channel
    with open(json_path) as fp:
        _set = json.load(fp)
    _set[str(guild.id)] = settings
    with open(json_path, "w") as fp:
        json.dump(_set, fp, indent=4)
    return "Set that channel as an announcement channel. You will now be notified of changes/features from Twilight via that channel"


def modlog_add(guild: discord.Guild, channel: int) -> str:
    """Add a channel as the modlog channel"""
    guild_settings = get_guild_settings(guild)
    guild_settings["modlog"] = channel
# class Moderation:
#     """
#         This class allows me to set up some default values for guilds on Twilight joining them.
#         It will create a few roles and a channel key and put it inside a JSON file.
#         These keys will be assigned `None` or `null` until the server owner sets the channels and roles.
#     """

#     def teardown(self, guild: discord.Guild) -> None:
#         """Remove a Guild from Twilight's settings"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings: dict = json.load(f)

#         if str(guild.id) not in settings.keys():
#             print("{} was not in Twilight's database so I did not remove any data".format(
#                 guild.name))
#             return

#         del settings[str(guild.id)]
#         print("Deleted Twilight's data for {} ({})".format(guild.name, guild.id))

#     def add_role(self, guild: discord.Guild, role_type: str, role: discord.Role) -> str:
#         """Set up the Mod or Admin role"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings: dict = json.load(f)
#         if str(guild.id) not in settings.keys():
#             setup(guild)
#             print(
#                 (
#                     f"{guild} was not in Twilight's database."
#                     "Running the defualt setup..."
#                 )
#             )

#         if settings[str(guild.id)][role_type] == role.id:
#             return "This role is already the {} role!".format(role_type)
#         settings[str(guild.id)][role_type] = role.id
#         with open(SETTINGS_JSON, "w") as f:
#             json.dump(settings, f, indent=4)
#         return "Added {} as the {} role".format(role, role_type)

#     def remove_role(self, guild: discord.Guild, role_type: str) -> str:
#         """Remove a Mod or Admin role"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings: dict = json.load(f)
#         if str(guild.id) not in settings.keys():
#             setup(guild)
#             print(
#                 (
#                     f"{guild} was not in Twilight's database."
#                     "Running the defualt setup..."
#                 )
#             )
#             return "Your guild wasn't in my database. So there is no {} role to remove!".format(role_type)

#         settings[str(guild.id)][role_type] = None
#         with open(SETTINGS_JSON, "w") as f:
#             json.dump(settings, f, indent=4)
#         return "Removed the {} role".format(role_type)

#     # For removal, there shouldn't be a channel,
#     # so requiring a channel is kinda dumb
#     def announcement_set(self, remove: bool, guild: discord.Guild, channel: discord.TextChannel = None) -> str:
#         """Set a Guild's announcement channel"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings: dict = json.load(f)
#         if str(guild.id) not in settings.keys():
#             setup(guild)
#             # return "Your guild was not in my settings so I set up the defaults. This means there isn't an announcement chanenl"

#         if remove == False:
#             settings[str(guild.id)]["announce_channel"] = channel.id
#             with open(SETTINGS_JSON, "w") as f:
#                 json.dump(settings, f, indent=4)
#             print("Added the announcement channel for {} ({})".format(
#                 guild.name, guild.id))
#             return "{} was set up as your guild's announcement channel!".format(channel.mention)

#         if settings[str(guild.id)]["announce_channel"] is None:
#             print("{} was just set up so I cancled the removal of the channel (since there wasn't one in the first place)".format(guild.name))
#         settings[str(guild.id)]["announe_channel"] = None
#         with open(SETTINGS_JSON, "r") as f:
#             json.dump(settings, f, indent=4)
#         print("Removed the announcement channel for {} ({})".format(
#             guild.name, guild.id))
#         return "Removed your guild's announcement channel"

#     def modlog_set(self, channel: discord.TextChannel, guild: discord.Guild) -> str:
#         """Set up a Guild's modlog channel"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings: dict = json.load(f)
#         if str(guild.id) not in settings.keys():
#             setup(guild)
#             print("{} wasn't in Twilight's database. Writing the normal setup...".format(
#                 guild.name))

#         settings[str(guild.id)]["modlog"] = channel.id
#         with open(SETTINGS_JSON, "w") as f:
#             json.dump(settings, f, indent=4)
#         return "Set {} as your modlog channel".format(channel.mention)

#     def modlog_remove(self, guild: discord.Guild) -> str:
#         """Remove a Guild's modlog channel"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings: dict = json.load(f)
#         if str(guild.id) not in settings.keys():
#             setup(guild)
#             print(
#                 "{} wasn't in Twilight's database. Writing the normal setup...".format(
#                     guild.name
#                 )
#             )
#             return "Your guild wasn't in my database! Since it wasn't the modlog channel wasn't set so there isn't need to fret!"

#         settings[str(guild.id)]["modlog"] = None
#         with open(SETTINGS_JSON, "w") as f:
#             json.dump(settings, f, indent=4)
#         return "Reset your guild's modlog channel"

#     async def create_case(self, ctx: Context, guild: discord.Guild, action: str, user: discord.Member):
#         """Create a case in the modlog"""
#         channel: int = Getters.get_modlog(guild)
#         if channel is None:
#             return

#         channel = guild.get_channel(channel)  # int -> discord.TextChannel
#         embed: discord.Embed = Embed.create(
#             self, ctx, title="{} Modlog".format(guild.name),
#             color=discord.Color.red(), footer="Twilight bot mod cog",
#             thumbnail=user.avatar_url
#         )
#         embed.description = f"{ctx.author.display_name} used {action} on {user.display_name}"
#         embed.add_field(name="Mod", value="{} ({})".format(
#             ctx.author.name, ctx.author.id), inline=False)
#         embed.add_field(name="Perpetrator", value="{} ({})".format(
#             user.name, user.id), inline=False)
#         await channel.send(embed=embed)


# class Getters:
#     @classmethod
#     def get_mod_role(cls, guild: discord.Guild):
#         """Return a Guild's Mod role id"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings = json.load(f)
#         try:
#             return settings[str(guild.id)]["moderator"]
#         except KeyError:
#             setup(guild)
#             return None

#     @classmethod
#     def get_admin_role(cls, guild: discord.Guild):
#         """Retrun a Guild's Admin role id"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings = json.load(f)
#         try:
#             return settings[str(guild.id)]["administrator"]
#         except KeyError:
#             setup(guild)
#             return None

#     @classmethod
#     def get_modlog(cls, guild: discord.Guild):
#         """Return a Guild's modlog channel id"""
#         with open(SETTINGS_JSON, "r") as f:
#             settings = json.load(f)
#         try:
#             return settings[str(guild.id)]["modlog"]
#         except KeyError:
#             setup(guild)
#             return None

#     @classmethod
#     def get_all_announce(cls):
#         with open(SETTINGS_JSON, "r") as f:
#             settings = json.load(f)
#         for guild in settings.keys():
#             yield settings[guild]["announce_channel"]
