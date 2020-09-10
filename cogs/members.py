import discord
from discord.ext import commands
from twilight_tools import BasicUtils, EmbedCreator


class Members(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.Embeder = EmbedCreator
        self.utils = BasicUtils

    @commands.command()
    @commands.guild_only()
    async def gavin(self, ctx):
        """
        Ping Gavin to tell him to stop

        [p]gavin
        """
        try:
            _gavin = self.client.get_user(747025476152721448)
            await ctx.send("{0.mention} quit it".format(_gavin))
            await ctx.send("Also {0.mention} learn to spell!".format(_gavin))
        except:
            await ctx.send("I cannot find Gavin 👀")

    @commands.command()
    async def shadow(self, ctx):
        _shadow = self.client.get_user(311194319644131328)
        await ctx.send("{0.mention} flex harder will you".format(_shadow))

    @commands.command()
    @commands.guild_only()
    async def cats(self, ctx):
        await ctx.send("Cats! <:RooCheer:708714718864343130>")

    @commands.command()
    @commands.guild_only()
    async def weirdo(self, ctx):
        await ctx.send("Not a horse man, just your Average Weirdo!")

    @commands.command()
    @commands.guild_only()
    async def jojo(self, ctx):
        await ctx.send("Jojo, who is the dev of this bot, is an okay-ish person")


def setup(client):
    client.add_cog(Members(client))
