import discord
from discord.ext.commands import Context
from discord import Embed, Color
import requests
import json


twilight_pfp = "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist"


class EmbedCreator:
    def __init__(self, client):
        self.client = client

    async def create(self, ctx, title="",
                     description="", color=Color.blue(),
                     footer=None, footer_image=None,
                     thumbnail=None, image=None):
        """
        Embed creator

        `Title` is the Embed Title
        `Color` is the Embed Color
        `Footer` and `Footer image` is optional
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
