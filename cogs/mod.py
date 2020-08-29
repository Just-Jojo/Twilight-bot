import discord
from discord.ext import commands
from discord.ext.commands import Cog
import json


class Mod(Cog, name="mod"):
    """Mod cog for wiping away the stain from your servers"""

    def __init__(self, client):
        self.client = client

    @commands.command(help="Bans a member")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason):
        """Ban a member"""
        if not member:
            await ctx.send("You need to supply a member to ban them.")

        else:
            await member.ban(reason=reason)
            await ctx.send("{0} was banned.".format(member))

    @commands.group(name="role", help="Add/Take roles from a member.")
    @commands.has_permissions(manage_roles=True)
    async def ROLES(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @ROLES.command(aliases=["give"])
    async def add(self, ctx, role: discord.Role = None, *, member: discord.Member = None):
        if role == None:
            await ctx.send_help(ctx.command)

        else:
            if member == None:
                member = ctx.author
            await member.add_roles(role)
            await ctx.send("Added {0} to {1}".format(role, member))

    @ROLES.command()
    async def take(self, ctx, role: discord.Role = None, *, member: discord.Member = None):
        if role == None:
            await ctx.send_help(ctx.command)

        else:
            if member == None:
                member = ctx.author
            await member.remove_roles(role)
            await ctx.send("Took {0} from {1}".format(role, member))

    @commands.command(help="Kicks a member")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason: str = None):
        if member == None:
            await ctx.send_help(ctx.command)

        else:
            await member.kick(reason=reason)
            await ctx.send("{0} was kicked".format(member))

    @commands.command(hidden=True)
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = "\n".join([str(guild) for guild in self.client.guilds])
        embed = discord.Embed(
            title="Servers",
            color=discord.Color.gold(),
            description=guilds
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Mod(client))
