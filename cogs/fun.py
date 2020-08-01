import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get

import random

import time


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

    @commands.command()
    async def rps(self, ctx, arg: str = None):
        rps_num = random.randint(0, 2)
        rps = ["Rock", "Paper", "Scissors"]
        rps_outcome = {
            "r": ["Rock. We tied!", "Paper. I win!", "Scissors. You win!"],
            "p": ["Rock. You win!", "Paper. We tied!", "Scissors. I win!"],
            "s": ["Rock. I win!", "Paper. You win!", "Scissors. We tied!"]
        }
        if arg != None:
            embed = discord.Embed(
                title="Rock Paper Scissors",
                color=discord.Color.blue()
            )
            embed.add_field(name="Your Choice", value=arg, inline=True)
            embed.add_field(name="My Choice",
                            value=rps[rps_num], inline=True)
            embed.add_field(
                name="Outcome", value=rps_outcome[arg][rps_num], inline=True)
        else:
            embed = discord.Embed(title="Oops!", color=discord.Color.red(
            ), description="You didn't specify an argument!\nYou can say any of these `r, p, s`")
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Fun(client))
