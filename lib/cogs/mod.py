import discord
from discord.ext import commands
from discord.ext.commands import Cog
import json
from twilight_tools import mod_role, guild_owner


class Mod(Cog):
    """Mod cog for wiping away the stain from your servers"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_guild_join(self, guild):
        guild_settings_default = {
            "modrole": None,
            "adminrole": None,
            "newschannel": None
        }
        with open('twisettings.json', 'r') as twi_read:
            data = json.load(twi_read)
        if guild.id not in data:
            data[int(guild.id)] = guild_settings_default
            with open("twisettings.json", "w") as twi_settings:
                json.dump(data, twi_settings, indent=4)
            print("Joined {} and setup the default settings".format(guild.name))
        else:
            pass

    def fetch_mod(self, guild):
        with open("twisettings.json", "r") as twi:
            data = json.load(twi)
        return data[guild.id]["modrole"]

    def modrole(self):
        async def inner(self, ctx):
            role = self.fetch_mod(ctx.guild)
            if role is None:
                return False
            return commands.has_role(role)
        return commands.check(inner)

    @commands.command(help="Bans a member")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason):
        """Ban a member"""
        # if not member:
        #     await ctx.send("You need to supply a member to ban them.")

        # else:
        #     if member.has_permissions(manage_messages=True):
        #         await ctx.send("I cannot ban that member as they have mod.")
        #     else:
        #         await member.ban(reason=reason)
        #         await ctx.send("{0} was banned.".format(member))

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def addrole(self, ctx, role: discord.Role = None, user: discord.Member = None):
        if user is None:
            user = ctx.author

        try:
            await user.add_roles(role)
            await ctx.send("Added {0} to {1.display_name}".format(role, user))
        except commands.errors.BotMissingPermissions:
            await ctx.send("I can't add roles!")

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    @commands.bot_has_guild_permissions(manage_roles=True)
    async def takerole(self, ctx, role: discord.Role = None, user: discord.Member = None):
        if user is None:
            user = ctx.author

        try:
            await user.remove_roles(role)
            await ctx.send("Took {0} from {1.display_name}".format(role, user))
        except commands.errors.BotMissingPermissions:
            await ctx.send("I can't add roles!")

    @commands.command(help="Kicks a member")
    @commands.has_permissions(kick_members=True)
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member == None:
            await ctx.send_help(ctx.command)

        else:
            if member.has_permissions(manage_message=True):
                await ctx.send("That person is a mod therefore I cannot ban them.")
            else:
                await member.kick(reason=reason)
                await ctx.send("{0} was kicked".format(member))

    @commands.command(aliases=["slow"])
    @commands.guild_only()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_channels=True)
    @mod_role()
    async def slowmode(self, ctx, seconds=None):
        if seconds:
            try:
                seconds = int(seconds)
            except:
                seconds = 0
        if seconds is not None and seconds <= 21600 and seconds != 0:
            try:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.send("Slowmode is now {seconds} seconds long".format(seconds=seconds))
                return
            except:
                pass
        await ctx.channel.edit(slowmode_delay=0)
        await ctx.send("Slowmode cleared.")

    @commands.command()
    @commands.guild_only()
    @mod_role()
    @commands.bot_has_permissions(manage_nicknames=True)
    async def rename(self, ctx, member: discord.Member, *, name: str = None):
        try:
            if name is not None:
                if len(name) <= 32 and len(name) >= 2:
                    try:
                        await member.edit(nick=name)
                        await ctx.send("Done.")
                    except discord.Forbidden:
                        await ctx.send("Could not change that member's nickname.")
                else:
                    await ctx.send("Could not change that members nickname.\nAll nicknames have to be between 2 and 32 characters.")
            else:
                return await ctx.send("Please specify a member")
        except commands.errors.BotMissingPermissions:
            await ctx.send("I can't rename that member as I don't have the proper permissions")

    @commands.command()
    @guild_owner()
    async def modrole(self, ctx, role: discord.Role = None):
        if role is None:
            return await ctx.send("Please input a role")
        with open("twisettings.json", "r") as twi_set:
            settings = json.load(twi_set)
        if int(ctx.guild.id) not in settings:
            guild_settings_default = {
                "modrole": None,
                "adminrole": None,
                "newschannel": None
            }
            settings[int(ctx.guild.id)] = guild_settings_default
            with open("twisettings.json", "w") as twi_settings:
                json.dump(settings, twi_settings, indent=4)
        settings[int(ctx.guild.id)]["modrole"] = role
        with open("twisettings.json", "w") as twi_settings:
            json.dump(settings, twi_settings, indent=4)
        await ctx.send("I have set the mod role as `{}`".format(role))


def setup(bot):
    bot.add_cog(Mod(bot))
