import discord
from discord.ext import commands
from discord.ext.commands import Cog
import json
from twilight_tools import mod_role, guild_owner


class Mod(Cog):
    """Mod cog for wiping away the stain from your servers"""

    def __init__(self, client):
        self.client = client

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


def setup(client):
    client.add_cog(Mod(client))
