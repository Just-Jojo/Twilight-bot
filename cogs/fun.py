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

    @commands.command(help="Repeats what you said")
    async def repeat(self, ctx, *, args):
        await ctx.send(args)


def setup(client):
    client.add_cog(Fun(client))
