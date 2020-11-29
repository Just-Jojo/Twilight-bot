"""
MIT License

Copyright (c) 2020 Jojo#7711

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import discord
from discord import Embed as Emb
from discord import Color
from discord.ext import commands
from datetime import datetime


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
        thumbnail: str = None, image: str = None, author: str = None, author_url: str = None
    ) -> discord.Embed:
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
            Returns: discord.Embed
        """
        data = Emb()
        if title:
            data.title = title
        if description:
            data.description = description

        if not color:
            color = ctx.author.color
        data.color = color

        if not footer:
            footer = "Twilight bot Embed"
        if not footer_url:
            footer_url = ctx.bot.user.avatar_url
        data.set_footer(text=footer, icon_url=footer_url)

        if image:
            data.set_image(url=image)
        if thumbnail:
            data.set_thumbnail(url=thumbnail)
        data.timestamp = datetime.utcnow()
        if not author_url:
            author_url = ctx.author.avatar_url
        if not author:
            author = ctx.author.display_name
        data.set_author(name=author, icon_url=author_url)

        return data

    def create_from_dict(self, ctx: commands.Context, **kwargs) -> discord.Embed:
        """
        Creates a Discord embed from a dictionary

        ~~~
        :title: str
        :description: str
        :color: Optional[discord.Color]
        :image: str
        :thumbnail: str
        ~~~
        Returns: discord.Embed
        """
        data = Emb()
        data.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        try:
            data.title = kwargs["title"]
        except KeyError:
            pass
        try:
            data.description = kwargs["description"]
        except KeyError:
            pass
        try:
            color = kwargs["color"]
        except KeyError:
            color = ctx.author.color
        data.color = color

        try:
            footer = kwargs["footer"]
        except KeyError:
            footer = "Twilight Embed maker"
        try:
            footer_url = kwargs["footer_url"]
        except KeyError:
            footer_url = ctx.me.avatar_url
        data.set_footer(text=footer, icon_url=footer_url)

        try:
            data.set_image(url=kwargs["image"])
        except KeyError:
            pass
        try:
            data.set_thumbnail(url=kwargs["thumbnail"])
        except KeyError:
            pass

        return data
