import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
import json
import random
from twilight_tools import EmbedCreator, BasicUtils

import asyncio

twilight_pfp = "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist"


class Fun(Cog):
    """Fun for all the little ponies"""

    def __init__(self, client):
        self.client = client
        self.EmbedCreator = EmbedCreator(self)
        self.BasicUtils = BasicUtils(self)

    @commands.command(name="party", help="Throw a party!")
    @commands.guild_only()
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
            await self.BasicUtils.help_returner(ctx)

    @say.command()
    async def repeat(self, ctx, *, args: str = None):
        """Say repeat

        Have the bot send your arguments in plain text.
        [p]say repeat | Eg. [p]say repeat Test
        """

        if args != None:
            await ctx.send(args)
        else:
            await self.BasicUtils.help_returner(ctx)

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
            embed = await self.EmbedCreator.create(
                ctx, title=title, description=args)
            await ctx.send(embed=embed)
        else:
            await self.BasicUtils.help_returner(ctx)

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
                embed = await self.EmbedCreator.create(ctx, title="Calculator")
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
            await self.BasicUtils.help_returner(ctx)

    @commands.command()
    async def invite(self, ctx):
        """Get the bot invite link and the support server link."""

        embed = await self.EmbedCreator.create(ctx,
                                               title="Invite/Support server link",
                                               description="Get the [bot](https://discord.com/api/oauth2/authorize?client_id=734159757488685126&permissions=8&scope=bot)",
                                               footer="Twilight Bot invite link")
        embed.add_field(name="Support Server link",
                        value="Get the [link](https://discord.gg/9cxxJSp) to the support server")
        await self.BasicUtils.whisper(ctx, ctx.author, embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = "\n".join([str(guild) for guild in self.client.guilds])
        embed = await self.EmbedCreator.create(
            ctx,
            title="Servers",
            color=discord.Color.gold(),
            description=guilds,
            footer="Servers that Twilight is in",
            thumbnail=twilight_pfp
        )
        await ctx.send(embed=embed)

    @commands.command(name="embed")
    async def embed_make(self, ctx, title, *, description):
        embed = await self.EmbedCreator.create(ctx, title=title, description=description)
        await ctx.send(embed=embed)

    @commands.command(name="mute")
    async def _mute(self, ctx, user):
        """Mute a user

        [p]mute <user>
        """
        await ctx.send("no.")

    @commands.command(name="rps")
    async def rock_paper_scissors_com(self, ctx, arg=None):
        await self.BasicUtils.rock_paper_scissors(ctx, arg)


def setup(client):
    client.add_cog(Fun(client))
