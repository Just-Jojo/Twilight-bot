"""Changed the plans for making the menu system.
Gonna be working with discord.ext.menus instead
"""
import discord
from discord.ext import menus
import typing

__all__ = ["TwilightEmbedMenu", "TwilightStringMenu", "TwilightBaseMenu"]
__version__ = "0.0.1"
__author__ = ["Jojo#7791"]


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


class TwilightBaseMenu(menus.Menu):
    """A menu system for strings and embeds mixed together"""

    def __init__(self, pages: typing.List[typing.Union[str, discord.Embed]], timeout: float = 30.0):
        self.pages = pages
        self.index = 0
        self.current_page = self.pages[0]
        super().__init__(timeout=timeout, delete_message_after=False, clear_reactions_after=True)

    async def send_initial_message(self, ctx: commands.Context, channel: discord.Channel):
        if isinstance(self.current_page, discord.Embed):
            return await channel.send(embed=self.current_page)
        else:
            return await channel.send(content=self.current_page)

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
        await self.send_messages(False)

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload: discord.RawReactionActionEvent):
        self.stop()
        await self.message.delete()

    @menus.button("\N{BLACK RIGHTWARDS ARROW}")
    async def on_right(self, payload: discord.RawReactionActionEvent):
        await self.send_messages(True)

    async def send_messages(self, forwards: bool):
        """Since the logic is just a bit too lengthy to do it for both"""
        self.index_parser(forwards=forwards)
        self.current_page = self.pages[self.index]
        if isinstance(self.current_page, discord.Embed):
            return await self.message.edit(embed=self.current_page)
        else:
            return await self.message.edit(content=self.current_page)
