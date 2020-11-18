import discord
from discord.ext.commands import (
    Context, check
)
import json


def moderator():
    async def inner(ctx: Context):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset = json.load(f)
        mod_role = ctx.guild.get_role(twiset[str(ctx.guild)]["moderator"])
        if not await ctx.bot.is_owner(ctx.author):
            return mod_role in ctx.author.roles
        else:
            return True
    return check(inner)


def administrator():
    async def inner(ctx: Context):
        with open("./lib/cogs/twisettings.json", "r") as f:
            twiset = json.load(f)
        admin_role = ctx.guild.get_role(
            twiset[str(ctx.guild.id)]["administrator"])
        if not await ctx.bot.is_owner(ctx.author):
            return admin_role in ctx.author.roles
        return True
    return check(inner)


class Moderation:
    def __init__(self, bot):
        self.bot = bot

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
