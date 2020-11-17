import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.utils import get
import json
import random
from twilight_tools import BasicUtils, EmbedCreator
import asyncio

twilight_pfp = "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist"


class Fun(Cog):
    """Fun for all the little ponies"""

    def __init__(self, bot):
        self.bot = bot
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

        await ctx.send(args)

    @say.command()
    async def frepeat(self, ctx, *, args: str = None):
        """
        Say frepeat

        Have the bot send your arguments in a fancy embed.
        [p]say frepeat <args> | Eg. [p]say frepeat Test
        """
        embed = await self.EmbedCreator.create(
            ctx, description=args, footer=ctx.author)
        await ctx.send(embed=embed)

    @commands.command(aliases=["calc"])
    async def calculator(self, ctx, *, args: str = None):
        """
        Math is fun!

        [p]calculator|calc <args>
        """
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

    @commands.command(hidden=True)
    @commands.is_owner()
    async def servers(self, ctx):
        guilds = "\n".join([str(guild) for guild in self.bot.guilds])
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
    @commands.guild_only()
    async def _mute(self, ctx, user):
        """Mute a user

        [p]mute <user>
        """
        await ctx.send("no.")

    @commands.command(name="rps")
    async def rock_paper_scissors_com(self, ctx, arg=None):
        """Rock Paper Scissors

        [p]rps <arg>
        ``.rps Rock``
        """
        await self.BasicUtils.rock_paper_scissors(ctx, arg)

    @commands.group(name="swearjar", aliases=["sj", "swearj", "jar"])
    async def swear_jar(self, ctx):  # , user: discord.Member = None):
        if ctx.invoked_subcommand is None:
            await self.BasicUtils.help_returner(ctx)

    @swear_jar.command()
    async def add(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        with open("swear_jar.json", "r") as f:
            jar = json.load(f)

        try:
            jar[str(user.id)] += 1
        except KeyError:
            jar[str(user.id)] = 1

        with open("swear_jar.json", "w") as f:
            json.dump(jar, f, indent=4)
        await ctx.send("Update {0.display_name}'s counter in the swear jar".format(user))


def setup(bot):
    bot.add_cog(Fun(bot))