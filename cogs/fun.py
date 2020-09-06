import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
import json
import random
from .embed_create import EmbedCreator

import asyncio


class Fun(Cog, name="fun"):
    """Fun for all the little ponies"""

    def __init__(self, client):
        self.client = client
        self.EmbedCreator = EmbedCreator(self)

    @commands.command(name="party", help="Throw a party!")
    async def party_time(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        await ctx.send("We're throwing a party for {0.mention}! 🥳".format(member))

    @commands.command(help="Fun!")
    async def fun(self, ctx):
        await ctx.send("Fun! Fun! Fun!")

    @commands.group()
    async def say(self, ctx):
        """
        Say

        Makes the bot send your arguments either as an embed or as plan text
        [p]say [repeat]|[frepeat] <args>
        """

        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @say.command()
    async def repeat(self, ctx, *, args: str = None):
        """Say repeat

        Have the bot send your arguments in plain text.
        [p]say repeat | Eg. [p]say repeat Test
        """

        if args != None:
            await ctx.send(args)
        else:
            await ctx.send_help(ctx.command)

    @say.command()
    async def frepeat(self, ctx, title: str = None, *, args: str = None):
        """
        Say frepeat

        Have the bot send your arguments in a fancy embed.
        [p]say frepeat <args> | Eg. [p]say frepeat Test
        """
        if title is None:
            title = "Embed Repeater"

        if args != None:
            embed = self.EmbedCreator.create(
                ctx, title=title, description=args)
            await ctx.send(embed=embed)
        else:
            await ctx.send_help(ctx.command)

    @commands.command(name=":|", aliases=[":(", ":)"], hidden=True)
    async def _silly_commands(self, ctx):
        await ctx.send(":P")

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx, *, args: str = None):
        """
        Math is fun!

        [p]calculator|calc <args>
        """
        if args != None:
            try:
                embed = discord.Embed(
                    title="Calculator",
                    color=discord.Color.blue()
                )
                embed.add_field(
                    name="Input",
                    value=args,
                    inline=False
                )
                embed.add_field(
                    name="Output",
                    value=eval(args),
                    inline=False
                )
                embed.set_footer(text="Twilight bot Calculator",
                                 icon_url="https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist")
                await ctx.send(embed=embed)
            except:
                await ctx.send("There was an error in the calculation!")
        else:
            await ctx.send_help(ctx.command)

    async def whisper(self, ctx: commands.Context, user: discord.Member, message: str):
        await user.send(message)

    @commands.command(name="dm", aliases=["whisper"], hidden=True)
    @commands.is_owner()
    async def dm_user(self, ctx, user: discord.Member, message: str):
        await self.whisper(ctx, user, message)


def setup(client):
    client.add_cog(Fun(client))
