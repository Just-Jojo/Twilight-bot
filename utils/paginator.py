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

"""Changed the plans for making the menu system.
Gonna be working with discord.ext.menus instead
"""


import typing
import discord
from discord.ext import commands, menus
__all__ = ["TwilightEmbedMenu", "TwilightStringMenu", "TwilightBaseMenu"]
__version__ = "0.0.1"
__author__ = ["Jojo#7791"]


class MenuMixin:
    pages: typing.Union[typing.List[discord.Embed],
                        typing.List[str]]
    current_page: typing.Union[discord.Embed, str]
    index: int
    message: discord.Message
    index_pages: bool

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
        if self.index_pages:
            if isinstance(self.current_page, discord.Embed):
                self.current_page.set_footer(
                    text=f"Page {self.index + 1}/{len(self.pages)}")
            else:
                self.current_page += f"\n{self.index + 1}/{len(self.pages)}"

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

    def __init__(self, pages: typing.List[discord.Embed], timeout: float = 30.0, index_pages: bool = False):
        self.pages = pages
        self.current_page = self.pages[0]
        self.index = 0
        self.index_pages = index_pages
        if self.index_pages:
            self.current_page.set_footer(text=f"Page 1/{len(self.pages)}")
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
        await self.message.delete()

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

    def __init__(self, pages: typing.List[str], timeout: float = 30.0, index_pages: bool = False):
        self.pages = pages
        self.current_page = self.pages[0]
        self.index = 0
        self.index_pages = index_pages
        if self.index_pages:
            self.current_page += f"\nPage 1/{len(self.pages)}"
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
    index_pages: :class:`bool`
        Whether or not the current page's index should be displayed
        If True a page will be edited to say "Page ?/?"
    message: :class:`Message`
        The actual message being used for the menu system
    """

    def __init__(self, pages: typing.List[typing.Union[str, discord.Embed]], timeout: float = 30.0, index_pages: bool = False):
        self.pages = pages
        self.index = 0
        self.current_page = self.pages[0]
        self.index_pages = index_pages
        if self.index_pages:
            if isinstance(self.current_page, discord.Embed):
                self.current_page.set_footer(text=f"Page 1/{len(self.pages)}")
            else:
                self.current_page += f"\nPage 1/{len(self.pages)}"
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


class TwilightPages(menus.ListPageSource):
    def __init__(self, data: list, use_embeds: bool, per_page: int = 15):
        self.use_embeds = use_embeds
        super().__init__(entries=data, per_page=per_page)

    def format_page(self, menu: "TwilightMenu", page) -> typing.Union[discord.Embed, str]:
        if self.use_embeds:
            ret = discord.Embed(title="Twilight Menu",
                                description=page, colour=discord.Colour.purple())
            ret.set_footer(
                text=f"Page {menu.current_page + 1}/{self.get_max_pages()}", icon_url=menu.bot.user.avatar_url)
        else:
            ret = page
        return ret


class TwilightMenu(menus.MenuPages, inherit_buttons=False):
    def __init__(
        self, source: menus.PageSource,
        page_start: int = 0,
        clear_reactions_after: bool = True,
        delete_message_after: bool = False,
        timeout: int = 30,
        message: discord.Message = None
    ):
        super().__init__(
            source=source, clear_reactions_after=clear_reactions_after,
            delete_message_after=delete_message_after, timeout=timeout,
            message=message
        )
        self.page_start = page_start

    async def send_initial_message(self, ctx, channel):
        self.current_page = self.page_start
        page = await self._source.get_page(self.page_start)
        kwargs = await self._get_kwargs_from_page(page)
        return await channel.send(**kwargs)

    async def show_check_page(self, page_number: int):
        max_pages = self._source.get_max_pages()
        try:
            if max_pages is None or max_pages > page_number >= 0:
                await self.show_page(page_number)
            elif page_number >= max_pages:
                await self.show_page(0)
            elif page_number < 0:
                await self.show_page(max_pages - 1)
        except IndexError:
            pass

    def _skip_double_triangle_buttons(self):
        return super()._skip_double_triangle_buttons()

    def _skip_single_arrows(self):
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages == 1

    @menus.button("\N{BLACK RIGHTWARDS ARROW}", position=menus.Last(0), skip_if=_skip_single_arrows)
    async def on_right(self, payload):
        await self.show_checked_page(self.current_page + 1)

    @menus.button("\N{LEFTWARDS BLACK ARROW}", position=menus.First(1), skip_if=_skip_single_arrows)
    async def on_left(self, payload):
        await self.show_checked_page(self.current_page - 1)

    @menus.button("\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}", position=menus.First(0), skip_if=_skip_double_triangle_buttons)
    async def on_far_left(self, payload):
        await self.show_checked_page(self.current_page - 5)

    @menus.button("\N{BLACK RIGHT-POINTING DOUBLE TRIANGLE}", position=menus.Last(1), skip_if=_skip_double_triangle_buttons)
    async def on_far_right(self, payload):
        await self.show_checked_page(self.current_page + 5)

    @menus.button("\N{CROSS MARK}")
    async def on_close(self, payload):
        self.stop()
        await self.message.delete()
