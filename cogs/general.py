import discord
from discord.ext import commands
from Tools.twilight_tools import BasicUtils, EmbedCreator


class General(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.basicutils = BasicUtils(self)
        self.embed = EmbedCreator(self)

    @commands.Cog.listener()
    async def on_ready(self):
        version = await self.basicutils.get_version()
        await self.client.change_presence(activity=discord.Game(name=">help | Version {version}".format(version=version)))

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong.")

    @commands.command(help="Probably the most important command")
    async def about(self, ctx):
        with open("about.txt", "r") as f:
            about_message = f.read()

        embed = self.EmbedCreator.create(
            title="About Twilight",
            description=about_message, color=discord.Color.purple(),
            footer="Jojo#7791"
        )
        await ctx.send(embed=embed)

    @commands.group()
    async def version(self, ctx):
        if ctx.invoked_subcommand is None:
            version = await self.basicutils.get_version()
            await ctx.send("My version is {0}!".format(version))

    @version.command(hidden=True)
    @commands.is_owner()
    async def update(self, ctx, version: str = None):
        if version is not None:
            await self.basicutils.update_version(version)
            version = await self.basicutils.get_version()
            await self.client.change_presence(activity=discord.Game(name=">help | Version {version}".format(version=version)))
            await ctx.send("Updated version!")
        else:
            await ctx.send("Could not update version")


def setup(client):
    client.add_cog(General(client))
