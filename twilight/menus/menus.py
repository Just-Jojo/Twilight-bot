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
from discord.ext import commands, menus


class TwilightPageSource(menus.ListPageSource):
    """A PageSource extension for Twilight's menu"""

    def __init__(self, entries, title: str):
        super().__init__(entries, per_page=1)
        self.title = title

    def is_paginating(self):
        return True

    async def format_page(self, menu: menus.Menu, page: str):
        """Format the page for the menu"""
        bot = menu.bot
        ctx = menu.ctx
        footnote = f"Page {menu.current_page + 1}/{self.get_max_pages()}"

        if ctx.channel.permissions_for(ctx.me).embed_links:
            embed = discord.Embed(
                title=self.title, description=page, colour=discord.Colour.purple()
            )
            embed.set_footer(text=footnote)
            return embed
        else:
            return page + f"\n{footnote}"


class TwilightMenu(menus.MenuPages, inherit_buttons=False):
    _source: TwilightPageSource
    message: discord.Message

    def __init__(
        self,
        source: TwilightPageSource,
        timeout: float = 30.0,
        delete_message_after: bool = False,
        clear_reactions_after: bool = True,
    ):
        super().__init__(
            source=source,
            timeout=timeout,
            delete_message_after=delete_message_after,
            clear_reactions_after=clear_reactions_after,
        )

    async def send_initial_message(
        self, ctx: commands.Context, channel: discord.TextChannel
    ):
        page = await self._source.get_page(0)
        kwargs = await self._get_kwargs_from_page(page)
        return await channel.send(**kwargs)

    async def show_checked_page(self, page_number: int):
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
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages < 5

    def _skip_single_buttons(self):
        max_pages = self._source.get_max_pages()
        if max_pages is None:
            return True
        return max_pages == 1

    # I kinda wrote the buttons in a weird way lol

    @menus.button(
        "\N{BLACK LEFT-POINTING DOUBLE TRIANGLE}",
        skip_if=_skip_double_triangle_buttons,
        position=menus.First(0),
    )
    async def go_to_first_page(self, payload):
        await self.show_checked_page(0)

    @menus.button(
        "\N{BLACK RIGHT-POINTING DOUBlE TRIANGLE}",
        skip_if=_skip_double_triangle_buttons,
        position=menus.Last(1),
    )
    async def go_to_last_page(self, payload):
        await self.show_checked_page(page_number=self._source.get_max_pages() - 1)

    @menus.button(
        "\N{BLACK RIGHTWARDS ARROW}",
        skip_if=_skip_single_buttons,
        position=menus.Last(0),
    )
    async def go_to_next_page(self, payload):
        await self.show_checked_page(page_number=self.current_page + 1)

    @menus.button(
        "\N{LEFTWARDS BLACK ARROW}",
        skip_if=_skip_single_buttons,
        position=menus.First(1),
    )
    async def go_to_previous_page(self, payload):
        await self.show_checked_page(page_number=self.current_page - 1)

    @menus.button("\N{CROSS MARK}")
    async def stop_pages(self, payload):
        self.stop()
        await self.message.delete()
