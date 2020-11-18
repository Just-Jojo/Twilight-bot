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


def moderator():
    async def inner(ctx: Context):
        mod_role = Getters.get_mod_role(ctx.guild)
        admin_role = Getters.get_admin_role(ctx.guild)
        if (
            not await ctx.bot.is_owner(ctx.author) and ctx.author is not ctx.guild.owner
            and admin_role not in ctx.author.roles
        ):
            return mod_role in ctx.author.roles
        else:
            return True
    return check(inner)


def administrator():
    async def inner(ctx: Context):
        admin_role = Getters.get_admin_role(ctx.guild)
        if not await ctx.bot.is_owner(ctx.author) and ctx.author is not ctx.guild.owner:
            return admin_role in ctx.author.roles
        return True
    return check(inner)


def guild_owner():
    async def inner(ctx: Context):
        return ctx.guild is not None and ctx.author is ctx.guild.owner
    return check(inner)


class Moderation:
    """
        This class allows me to set up some default values for guilds on Twilight joining them.
        It will create a few roles and a channel key and put it inside a JSON file.
        These keys will be assigned `None` or `null` until the server owner sets the channels and roles.
    """

    def setup(self, guild: discord.Guild):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset: dict = json.load(f)

        if str(guild.id) in twiset.keys():
            print(
                "{} ({}) was already in Twilight's database so I skipped over it".format(
                    guild.name, guild.id)
            )
            return
        twiset[str(guild.id)] = {
            "administrator": None,
            "moderator": None,
            "announce_channel": None
        }
        with open("./lib/cogs/twisettings.json", "w") as f:
            json.dump(twiset, f, indent=4)
        print("Added {} ({}) to Twilight's settings".format(guild.name, guild.id))

    def teardown(self, guild: discord.Guild):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset: dict = json.load(f)

        if str(guild.id) not in twiset.keys():
            print("{} was not in Twilight's database so I did not remove any data".format(
                guild.name))
            return

        del twiset[str(guild.id)]
        print("Deleted Twilight's data for {} ({})".format(guild.name, guild.id))
        return

    def add_role(self, guild: discord.Guild, role_type: str, role: discord.Role):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)

        if twiset[str(guild.id)][role_type] == role.id:
            return "This role is already the {} role!".format(role_type)
        twiset[str(guild.id)][role_type] = role.id
        with open("./lib/cogs/twisettings.json", "w") as f:
            json.dump(twiset, f, indent=4)
        return "Added {} as the {} role".format(role, role_type)

    def remove_role(self, guild: discord.Guild, role_type: str):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
            return

        twiset[str(guild.id)][role_type] = None
        with open("./lib/cogs/twisettings.json", "w") as f:
            json.dump(twiset, f, indent=4)
        return "Removed the {} role".format(role_type)

    # For removal, there shouldn't be a channel,
    # so requiring a channel is kinda dumb
    def announcement_set(self, remove: bool, guild: discord.Guild, channel: discord.TextChannel = None):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
        if twiset[str(guild.id)]["announce_channel"] is None:
            print("{} was just set up so I cancled the removal of the channel (since there wasn't one in the first place)".format(guild.name))
            return "Your guild was not in my settings so I set up the defaults. This means there isn't an announcement chanenl"

        if remove == True:
            twiset[str(guild.id)]["announce_channel"] = channel.id
            with open("./lib/cogs/twisettings.json", "w") as f:
                json.dump(twiset, f, indent=4)
            print("Added the announcement channel for {} ({})".format(
                guild.name, guild.id))
            return "{} was set up as your guild's announcement channel!".format(channel.mention)

        twiset[str(guild.id)]["announe_channel"] = None
        with open("./lib/cogs/twisettings.json", "r") as f:
            json.dump(twiset, f, indent=4)
        print("Removed the announcement channel for {} ({})".format(
            guild.name, guild.id))
        return "Removed your guild's announcement channel"

    async def ban_kick(self, ctx: Context, user: discord.Member, kick_ban: str, reason: str, days: int = 0):
        if ctx.author == user:
            return "Self harm is bad 😔"
        if user is ctx.guild.owner:
            return "Trying to pull a coup, eh?"

        if kick_ban == "ban":
            try:
                await user.ban(reason=reason, delete_message_days=days)
                return "Banned {} for the reason {}".format(user, reason)
            except discord.Forbidden:
                return "I could not ban that member. Sorry"
        else:
            try:
                await user.kick(reason)
                return "Kicked {} for the reason {}".format(user, reason)
            except discord.Forbidden:
                return "I could not kick that member. Sorry"

    async def mute_member(self, ctx: Context, user: discord.Member, channel: discord.TextChannel):
        if ctx.guild is None:
            return "This functionality is only available in guilds!"
        if user is ctx.guild.owner:
            return "You can't mute the owner!"
        if user == ctx.author:
            return "Don't mute yourself lol"

        if (
            Getters.get_admin_role(ctx.guild) in user.roles or
            Getters.get_mod_role(ctx.guild) in user.roles
        ):
            return "This user is a mod/admin therefore I cannot mute them"
        try:
            await channel.set_permissions(user, send_messages=False)
        except discord.Forbidden:
            return "I could not mute this user."
        return "Muted {} in {}".format(user.name, channel.mention)

    async def unmute_member(self, ctx: Context, user: discord.Member, channel: discord.TextChannel):
        if ctx.guild is None:
            return "This functionality is only available in guilds!"
        if user is ctx.guild.owner:
            return "Owners can't be muted to be unmuted."
        if user == ctx.author:
            return "Let's think logically for a second... how can you type to tell me to unmute you... if you're muted?"

        if (
            Getters.get_admin_role(ctx.guild) in user.roles or
            Getters.get_mod_role(ctx.guild) in user.roles
        ):
            return "Mods and Admins can't be muted so unmuting an unmutable person would be silly"
        try:
            await channel.set_permissions(user, send_messages=True)
        except discord.Forbidden:
            return "I couldn't unmute the user."


class Getters:
    @classmethod
    def get_mod_role(cls, guild: discord.Guild):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset = json.load(f)
        return twiset[str(guild.id)]["moderator"]

    @classmethod
    def get_admin_role(cls, guild: discord.Guild):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset = json.load(f)
        return twiset[str(guild.id)]["administrator"]
