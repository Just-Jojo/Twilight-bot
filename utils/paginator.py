"""Changed the plans for making the menu system.
Gonna be working with discord.ext.menus instead
"""
import discord
from discord.ext import menus
import typing


class TwilightEmbedMenu(menus.Menu):
    """Base menu for Twilight things"""

    def __init__(self, pages: typing.List[discord.Embed], timeout: float = 30.0):
        self.pages = pages
        self.current_page = self.pages[0]
        self.index = 0
        super().__init__(timeout=timeout, delete_message_after=False,
                         clear_reactions_after=True)  # Don't delete the message

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.current_page)

    @menus.button("\N{LEFTWARDS BLACK ARROW}")
    async def on_left(self, payload: discord.RawReactionActionEvent):
        self.index_parser(False)
        self.current_page = self.pages[self.index]
        return await self.message.edit(embed=self.current_page)

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload: discord.RawReactionActionEvent):
        self.stop()
        await self.message.delete()

    @menus.button("\N{BLACK RIGHTWARDS ARROW}")
    async def on_right(self, payload: discord.RawReactionActionEvent):
        self.index_parser(True)
        self.current_page = self.pages[self.index]
        return await self.message.edit(embed=self.current_page)

    def index_parser(self, forwards: bool):
        """Handy tool for the Indexing of embeds"""
        pages_len = len(self.pages) - 1
        if forwards:
            self.index += 1
            if self.index > pages_len:
                self.index = 0
        else:
            self.index -= 1
            if self.index < 0:
                self.index = pages_len


class TwilightStringMenu(menus.Menu):
    """A menu system for regular messages"""

    def __init__(self, pages: typing.List[str], timeout: float = 30.0):
        self.pages = pages
        self.current_page = self.pages[0]
        self.index = 0
        super().__init__(timeout=timeout, delete_message_after=False, clear_reactions_after=True)

    def index_parser(self, forwards: bool):
        pages_len = len(self.pages) - 1
        if forwards:
            self.index += 1
            if self.index > pages_len:
                self.index = 0
        else:
            self.index -= 1
            if self.index < 0:
                self.index = pages_len

    @menus.button("\N{LEFTWARDS BLACK ARROW}")
    async def on_left(self, payload: discord.RawReactionActionEvent):
        self.index_parser(False)
        self.current_page = self.pages[self.index]
        return await self.message.edit(content=self.current_page)

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload: discord.RawReactionActionEvent):
        self.stop()

    @menus.button("\N{BLACK RIGHTWARDS ARROW}")
    async def on_right(self, payload: discord.RawReactionActionEvent):
        self.index_parser(True)
        self.current_page = self.pages[self.index]
        return await self.message.edit(content=self.current_page)
