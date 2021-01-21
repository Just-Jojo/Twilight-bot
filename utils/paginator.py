"""Changed the plans for making the menu system.
Gonna be working with discord.ext.menus instead
"""
import discord
from discord.ext import menus, commands
import typing

__all__ = ["TwilightEmbedMenu", "TwilightStringMenu", "TwilightBaseMenu"]
__version__ = "0.0.1"
__author__ = ["Jojo#7791"]


class MenuMixin:
    pages: typing.Union[typing.list[discord.Embed],
                        typing.List[discord.Embed, str]]
    current_page: discord.Embed
    index: int
    message: discord.Message

    def index_parser(self, forwards: bool):
        """Calculate the proper index for the next page

        Parameters
        ----------
        forwards: :class:`bool`
            If True the index will jump forwards
            If the index is greater than the length of the pages it will jump to the first

            If False the index will jump backwards
            If the index is less than 0 it will jump to the end of the pages
        """
        page_len = len(self.pages) - 1
        if forwards is True:
            self.index += 1
            if self.index > page_len:
                self.index = 0
        else:
            self.index -= 1
            if self.index < 0:
                self.index = page_len
        self.current_page = self.pages[self.index]

    async def send_initial_message(self, ctx: commands.Context, channel: discord.TextChannel = None):
        if ctx.guild is None or channel is None:
            channel = ctx.channel
        if isinstance(self.current_page, discord.Embed):
            return await channel.send(embed=self.current_page)
        else:
            return await channel.send(content=self.current_page)

    async def on_exit(self, payload):
        """|coro|

        This is the `X` button and must be implimented in each menu as a way to stop

        Type
        ----
        menus.Button
            A reaction that gets added to the message defined in :func:`send_initial_message`

        Parameters
        ----------
        payload: :class:`discord.RawReactionActionEvent`
            This doesn't need to do anything we just need it for the even
        """
        raise NotImplementedError

    async def send_messages(self):
        """|coro|

        Sends a message that is either a string or embed

        *note You must call :func:`index_parser` for this to work

        Returns
        -------
        discord.Message
            The message sent
        """
        if isinstance(self.current_page, discord.Embed):
            return await self.message.edit(embed=self.current_page)
        else:
            return await self.message.edit(content=self.current_page)


class TwilightEmbedMenu(MenuMixin, menus.Menu):
    """Base menu for Twilight things

    Attributes
    ----------
    pages: List[:class:`Embed`]
        The embed pages for the menu
    current_page: :class:`Embed`
        The embed currently displayed in the menu
    index: :class:`int`
        The index of the current_page in pages
    message: :class:`Message`
        The actual message the menu works on
    """

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
        await self.send_messages()

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload: discord.RawReactionActionEvent):
        self.stop()

    @menus.button("\N{BLACK RIGHTWARDS ARROW}")
    async def on_right(self, payload: discord.RawReactionActionEvent):
        self.index_parser(True)
        await self.send_messages()


class TwilightStringMenu(MenuMixin, menus.Menu):
    """A menu system for regular messages

    Attributes
    ----------
    pages: List[:class:`str`]
        The page list to send content
        Must be type :class:`str`
    current_page: :class:`str`
        The current string that's in the message
    index: :class:`int`
        The index of the pages tied to current_page
    message: :class:`Message`
        The message that gets sent on :func:`send_initial_message`
    """

    def __init__(self, pages: typing.List[str], timeout: float = 30.0):
        self.pages = pages
        self.current_page = self.pages[0]
        self.index = 0
        super().__init__(timeout=timeout, delete_message_after=False, clear_reactions_after=True)

    @menus.button("\N{LEFTWARDS BLACK ARROW}")
    async def on_left(self, payload: discord.RawReactionActionEvent):
        self.index_parser(forwards=False)
        await self.send_messages()

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload: discord.RawReactionActionEvent):
        self.stop()

    @menus.button("\N{BLACK RIGHTWARDS ARROW}")
    async def on_right(self, payload: discord.RawReactionActionEvent):
        self.index_parser(forwards=True)
        await self.send_messages()


class TwilightBaseMenu(MenuMixin, menus.Menu):
    """A menu system for strings and embeds mixed together

    Attributes
    ----------
    pages: List[Union[:class:`str`, :class:`Embed`]]
        The menu's pages
        Can be :class:`str` and :class:`Embed`
    current_page: Union[:class:`str`, :class:`Embed`]
        The page currently displayed
        It can be either :class:`str` or :class:`Embed`
    index: :class:`int`
        The index of current_page in pages
    message: :class:`Message`
        The actual message being used for the menu system
    """

    def __init__(self, pages: typing.List[typing.Union[str, discord.Embed]], timeout: float = 30.0):
        self.pages = pages
        self.index = 0
        self.current_page = self.pages[0]
        super().__init__(timeout=timeout, delete_message_after=False, clear_reactions_after=True)

    @menus.button("\N{LEFTWARDS BLACK ARROW}")
    async def on_left(self, payload: discord.RawReactionActionEvent):
        self.index_parser(forwards=False)
        await self.send_messages()

    @menus.button("\N{CROSS MARK}")
    async def on_x(self, payload: discord.RawReactionActionEvent):
        self.stop()

    @menus.button("\N{BLACK RIGHTWARDS ARROW}")
    async def on_right(self, payload: discord.RawReactionActionEvent):
        self.index_parser(forwards=True)
        await self.send_messages()
