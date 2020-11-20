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

TWISETTINGS_PATH = "./lib/cogs/twisettings.json"


def moderator():
    """The check to see if the user is a mod"""
    async def inner(ctx: Context):
        mod_role = Getters.get_mod_role(ctx.guild)
        admin_role = Getters.get_admin_role(ctx.guild)
        if (
            not await ctx.bot.is_owner(ctx.author) and ctx.author != ctx.guild.owner
            and admin_role not in ctx.author.roles
        ):
            return mod_role in ctx.author.roles
        else:
            return True
    return check(inner)


def administrator():
    """The check to see if the user is an admin"""
    async def inner(ctx: Context):
        admin_role = Getters.get_admin_role(ctx.guild)
        if not await ctx.bot.is_owner(ctx.author) and ctx.author != ctx.guild.owner:
            return admin_role in ctx.author.roles
        return True
    return check(inner)


def guild_owner():
    """Guild owner check in the discord.py library when?"""
    async def inner(ctx: Context):
        return ctx.guild is not None and ctx.author == ctx.guild.owner
    return check(inner)


class Moderation:
    """
        This class allows me to set up some default values for guilds on Twilight joining them.
        It will create a few roles and a channel key and put it inside a JSON file.
        These keys will be assigned `None` or `null` until the server owner sets the channels and roles.
    """

    def setup(self, guild: discord.Guild):
        """Set up a Guild with the default settings"""
        with open(TWISETTINGS_PATH, "r") as f:
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
            "announce_channel": None,
            "modlog": None
        }
        with open(TWISETTINGS_PATH, "w") as f:
            json.dump(twiset, f, indent=4)
        print("Added {} ({}) to Twilight's settings".format(guild.name, guild.id))

    def teardown(self, guild: discord.Guild):
        """Remove a Guild from Twilight's settings"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset: dict = json.load(f)

        if str(guild.id) not in twiset.keys():
            print("{} was not in Twilight's database so I did not remove any data".format(
                guild.name))
            return

        del twiset[str(guild.id)]
        print("Deleted Twilight's data for {} ({})".format(guild.name, guild.id))
        return

    def add_role(self, guild: discord.Guild, role_type: str, role: discord.Role):
        """Set up the Mod or Admin role"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
            print(
                (
                    f"{guild} was not in Twilight's database."
                    "Running the defualt setup..."
                )
            )

        if twiset[str(guild.id)][role_type] == role.id:
            return "This role is already the {} role!".format(role_type)
        twiset[str(guild.id)][role_type] = role.id
        with open(TWISETTINGS_PATH, "w") as f:
            json.dump(twiset, f, indent=4)
        return "Added {} as the {} role".format(role, role_type)

    def remove_role(self, guild: discord.Guild, role_type: str):
        """Remove a Mod or Admin role"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
            print(
                (
                    f"{guild} was not in Twilight's database."
                    "Running the defualt setup..."
                )
            )
            return "Your guild wasn't in my database. So there is no {} role to remove!".format(role_type)

        twiset[str(guild.id)][role_type] = None
        with open(TWISETTINGS_PATH, "w") as f:
            json.dump(twiset, f, indent=4)
        return "Removed the {} role".format(role_type)

    # For removal, there shouldn't be a channel,
    # so requiring a channel is kinda dumb
    def announcement_set(self, remove: bool, guild: discord.Guild, channel: discord.TextChannel = None):
        """Set a Guild's announcement channel"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
            # return "Your guild was not in my settings so I set up the defaults. This means there isn't an announcement chanenl"

        if remove == False:
            twiset[str(guild.id)]["announce_channel"] = channel.id
            with open(TWISETTINGS_PATH, "w") as f:
                json.dump(twiset, f, indent=4)
            print("Added the announcement channel for {} ({})".format(
                guild.name, guild.id))
            return "{} was set up as your guild's announcement channel!".format(channel.mention)

        if twiset[str(guild.id)]["announce_channel"] is None:
            print("{} was just set up so I cancled the removal of the channel (since there wasn't one in the first place)".format(guild.name))
        twiset[str(guild.id)]["announe_channel"] = None
        with open(TWISETTINGS_PATH, "r") as f:
            json.dump(twiset, f, indent=4)
        print("Removed the announcement channel for {} ({})".format(
            guild.name, guild.id))
        return "Removed your guild's announcement channel"

    async def ban_kick(self, ctx: Context, user: discord.Member, kick_ban: str, reason: str, days: int = 0):
        """Ban or kick a user"""
        if ctx.author.id == user.id:
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
                await self.create_case(ctx, ctx.guild, "ban", user)
        else:
            try:
                await user.kick(reason)
                return "Kicked {} for the reason {}".format(user, reason)
            except discord.Forbidden:
                return "I could not kick that member. Sorry"
            else:
                await self.create_case(ctx, ctx.guild, "kick", user)

    async def mute_member(self, ctx: Context, user: discord.Member, channel: discord.TextChannel):
        """Channel mute a member"""
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
        else:
            await self.create_case(ctx, ctx.guild, "mute", user)
        return "Muted {} in {}".format(user.name, channel.mention)

    async def unmute_member(self, ctx: Context, user: discord.Member, channel: discord.TextChannel):
        """Channel unmute a member"""
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
        else:
            await self.create_case(ctx, ctx.guild, "unmute", user)

    def modlog_set(self, channel: discord.TextChannel, guild: discord.Guild):
        """Set up a Guild's modlog channel"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
            print("{} wasn't in Twilight's database. Writing the normal setup...".format(
                guild.name))

        twiset[str(guild.id)]["modlog"] = channel.id
        with open(TWISETTINGS_PATH, "w") as f:
            json.dump(twiset, f, indent=4)
        return "Set {} as your modlog channel".format(channel.mention)

    def modlog_remove(self, guild: discord.Guild):
        """Remove a Guild's modlog channel"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset: dict = json.load(f)
        if str(guild.id) not in twiset.keys():
            self.setup(guild)
            print(
                "{} wasn't in Twilight's database. Writing the normal setup...".format(
                    guild.name
                )
            )
            return "Your guild wasn't in my database! Since it wasn't the modlog channel wasn't set so there isn't need to fret!"

        twiset[str(guild.id)]["modlog"] = None
        with open(TWISETTINGS_PATH, "w") as f:
            json.dump(twiset, f, indent=4)
        return "Reset your guild's modlog channel"

    async def create_case(self, ctx: Context, guild: discord.Guild, action: str, user: discord.Member):
        """Create a case in the modlog"""
        channel: discord.TextChannel = Getters.get_modlog(guild)
        if channel is None:
            return

        embed: discord.Embed = Embed.create(
            self, ctx, title="{} Modlog".format(guild.name),
            color=discord.Color.red(), footer="Twilight bot mod cog"
        )
        embed.add_field(name="Mod", value="{} ({})".format(
            ctx.author.name, ctx.author.id), inline=False)
        embed.add_field(name="Perpetrator", value="{} ({})".format(
            user.name, user.id), inline=False)
        await channel.send(embed)


class Getters:
    @classmethod
    def get_mod_role(cls, guild: discord.Guild):
        """Return a Guild's Mod role id"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset = json.load(f)
        return twiset[str(guild.id)]["moderator"]

    @classmethod
    def get_admin_role(cls, guild: discord.Guild):
        """Retrun a Guild's Admin role id"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset = json.load(f)
        return twiset[str(guild.id)]["administrator"]

    @classmethod
    def get_modlog(cls, guild: discord.Guild):
        """Return a Guild's modlog channel id"""
        with open(TWISETTINGS_PATH, "r") as f:
            twiset = json.load(f)
        return twiset[str(guild.id)]["modlog"]

    @classmethod
    def get_all_announce(cls):
        with open(TWISETTINGS_PATH, "r") as f:
            twiset = json.load(f)
        for guild in twiset.keys():
            yield twiset[guild]["announce_channel"]
