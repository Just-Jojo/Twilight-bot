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
