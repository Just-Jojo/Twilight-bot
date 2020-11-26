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
        thumbnail: str = None, image: str = None
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
        data.timestamp = datetime.utcnow()

        return data
