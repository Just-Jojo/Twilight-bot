import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

import random

import time

from rockpaperscissors import RockPaperScissors as RPS


class Fun(Cog, name="fun"):
    """Fun for all the little ponies"""

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("Fun spell is working")

    @commands.command(name="party", help="Throw a party!")
    async def party_time(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        await ctx.send("We're throwing a party for {0}! 🥳".format(member.mention))

    @commands.command(help="Fun!")
    async def fun(self, ctx):
        await ctx.send("Fun! Fun! Fun!")

    @commands.group(name="say")
    async def SAY(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("repeat (Sent what you said as plain text), frepeat (Sent what you said as an embed.)")

    @SAY.command()
    async def repeat(self, ctx, *, args):
        await ctx.send(args)

    @SAY.command()
    async def frepeat(self, ctx, *, args):
        embed = discord.Embed(
            title="Repeat Embed",
            description=args,
            color=discord.Color.blue()
        )
        embed.set_footer(icon_url=ctx.author.avatar_url, text=ctx.author)
        await ctx.send(embed=embed)

    @commands.command(help="Rock paper scissors game. Use `r p s` for the arguments")
    async def rps(self, ctx, arg: str):
        y = arg.lower()[0]
        await ctx.send(embed=RPS(y))

    @commands.command(name=":|", aliases=[":(", ":)"], hidden=True)
    async def _silly_commands(self, ctx):
        await ctx.send(":P")

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx, *, args):
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
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
