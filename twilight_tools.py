import json
import random

import discord
import requests
from discord import Color, Embed
from discord.ext import commands
from discord.ext.commands import Context

twilight_pfp = "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist"
twilight_image_links = [
    "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist",
    "https://i.pinimg.com/originals/5f/80/fc/5f80fc95aac0aa4448ccf954d198c3d1.png",
    "https://i.pinimg.com/originals/d5/08/a6/d508a6dae0f0e51bc9157e0d98885846.png",
    "https://upload.wikimedia.org/wikipedia/sco/thumb/5/5b/Twilight_sparkle.png/1200px-Twilight_sparkle.png"
]


class EmbedCreator:
    def __init__(self, client):
        self.client = client

    async def create(self, ctx, title="",
                     description="", color=Color.blue(),
                     footer=None, footer_image=None,
                     thumbnail=None, image=None):
        """
        Embed creator

        context, title of the embed, description of the embed, color (defaults to blue), footer (optional), footer image (also optional), thumbnail, image
        """
        data = Embed(title=title, color=color)
        if description is not None:
            data.description = description
        data.set_author(name=ctx.message.author.display_name,
                        icon_url=ctx.message.author.avatar_url)

        if footer is None:
            footer = "Twilight Embed"
        if footer_image is None:
            footer_image = twilight_pfp
        data.set_footer(text=footer, icon_url=footer_image)

        if image is not None:
            data.set_image(url=image)

        if thumbnail is not None:
            data.set_thumbnail(
                url=thumbnail
            )
        return data


class BasicUtils:
    def __init__(self, client):
        self.client = client

    async def whisper(self, ctx: Context, user: discord.Member, message: str = '', embed: discord.Embed = None):
        if embed is not None:
            await user.send(message, embed=embed)
            return
        await user.send(message)

    async def json_dumper(self, json_file: str, content):
        with open("{0}.json".format(json_file), "a") as f:
            json.dump(f)

    async def help_returner(self, ctx: Context):
        await ctx.send_help(ctx.command)

    async def twilight_pic(self):
        return random.choice(twilight_image_links)

    async def something(self):
        pass


class General(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong.")

    @client.command(help="Probably the most important command")
    async def about(self, ctx):
        with open("about.txt", "r") as f:
            about_message = f.read()

        embed = self.EmbedCreator.create(
            title="About Twilight",
            description=about_message, color=discord.Color.purple(),
            footer="Jojo#7791"
        )
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(General(client))
