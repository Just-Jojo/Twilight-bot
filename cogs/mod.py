import discord
from discord.ext import commands
from discord.ext.commands import Cog


class Mod(Cog, name="mod"):
    """Mod cog for wiping away the stain from your servers"""

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_read(self):
        print("Mod online")

    @commands.command(help="Bans a member")
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *reason):
        if not member:
            await ctx.send("You need to supply a member to ban them.")

        else:
            await member.ban(reason=reason)
            await ctx.send("{0} was banned.".format(member))

    @commands.group(name="role")
    async def _roles(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                """```Role:
    Add, Take```"""
            )

    @_roles.command()
    async def add(self, ctx, role: discord.Role = None, member: discord.Member = None):
        if role == None:
            await ctx.send("You need to give a role to attach it to someone")

        else:
            if member == None:
                member = ctx.author
            await member.add_roles(role)
            await ctx.send("Added {0} to {1}".format(role, member))

    @_roles.command()
    async def take(self, ctx, role: discord.Role = None, member: discord.Member = None):
        if role == None:
            await ctx.send("You have to give a role to take it from someone")

        else:
            if member == None:
                member = ctx.author
            await member.remove_roles(role)
            await ctx.send("Took {0} from {1}".format(role, member))

    @commands.command(help="Kicks a member")
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None):
        if member == None:
            await ctx.send("I can't kick a member if you don't tag one")

        else:
            await member.kick(reason=None)
            await ctx.send("{0} was kicked".format(member))

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm sorry that person could not be banned because *one* of us has improper permissions.")

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm sorry that person could not be kicked because *one* of us has improper permissions.")

    @add.error
    async def add_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm sorry that person could not have a role added because *one* of us has improper permissions.")

    @take.error
    async def take_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("I'm sorry that person could not have their roles taken because *one* of us has improper permissions.")


def setup(client):
    client.add_cog(Mod(client))
