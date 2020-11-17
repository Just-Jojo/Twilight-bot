from discord import Embed as Emb
from discord import Color
from discord.ext import commands


class Embed:
    """
        Creates a Discord embed object and sets some defaults to it

        Arguments:
        ~~~
        title: str
        description: str
        color: discord.Color
        author: str
        author_url: str
        footer: str
        footer_url: str
        thumbnail: str
        image: str
        ~~~
    """

    def __init__(self, bot):
        self.bot = bot

    def create(
        self, ctx: commands.Context, title: str = None, description: str = None,
        color: Color = None, footer: str = None, footer_url: str = None,
        thumbnail: str = None, image: str = None
    ):
        """
            Creates a Discord embed object and sets some defaults to it

            Arguments:
            ~~~
            title: str
            description: str
            color: discord.Color
            author: str
            author_url: str
            footer: str
            footer_url: str
            thumbnail: str
            image: str
            ~~~
        """
        data = Emb()
        if title is not None:
            data.title = title
        if description is not None:
            data.description = description

        if color is None:
            color = ctx.author.color
        data.color = color

        if footer is None:
            footer = "Twilight bot Embed"
        if footer_url is None:
            footer_url = ctx.bot.user.avatar_url
        data.set_footer(text=footer, icon_url=footer_url)

        if image is not None:
            data.set_image(url=image)
        if thumbnail is not None:
            data.set_thumbnail(url=thumbnail)

        return data
