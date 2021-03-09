"""
MIT License

Copyright (c) 2020-2021 Jojo#7711

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
# Since I got a lot of this code from stroupbslayen on github
# I'm gonna include their license here

"""MIT License

Copyright (c) 2020 stroupbslayen

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
SOFTWARE
"""

import typing

import discord
from discord.ext import commands, menus  # I need to write my own menu lol


class TwilightHelpMenu(menus.Menu):
    message: discord.Message

    def __init__(self, embeds: typing.List[discord.Embed], msg: discord.Message):
        super().__init__(
            timeout=30.0,
            delete_message_after=False,
            clear_reactions_after=True,
            check_embeds=False,
            message=msg,
        )
        self.embeds = embeds
        self.current_page = 0

    async def show_checked_page(self, page_number: int):
        max_pages = len(self.embeds)
        try:
            if max_pages is None or max_pages > page_number >= 0:
                await self.show_page(page_number)
            elif page_number >= max_pages:
                await self.show_page(0)
            elif page_number < 0:
                await self.show_page(max_pages - 1)
        except IndexError:
            pass

    async def show_page(self, page_number: int):
        """Show a page"""
        page = self.embeds[page_number]
        self.current_page = page_number
        await self.message.edit(embed=page)

    @menus.button("\N{LEFTWARDS BLACK ARROW}", position=menus.First(0))
    async def go_to_previous_page(self, payload):
        await self.show_checked_page(self.current_page + 1)

    @menus.button("\N{BLACK RIGHTWARDS ARROW}", position=menus.Last(0))
    async def go_to_next_page(self, payload):
        await self.show_checked_page(self.current_page + 1)

    @menus.button("\N{CROSS MARK}")
    async def stop_pages(self, payload):
        self.stop()
        await self.message.delete()

    async def send_initial_message(self, ctx, channel):
        raise RuntimeError("Should have sent a message")


class Paginator:
    """Paginator for Twilight's help command"""

    def __init__(self, colour: int = 0x00FFFF):
        self.colour = colour
        self.char_limit = 6000
        self.ending_note = None
        self.clear()

    def clear(self):
        self._pages = []

    def _check_embed(self, embed: discord.Embed, *chars: str):
        return len(embed) + sum(len(char) for char in chars if char) < self.char_limit

    def _new_page(self, title: str, description: str) -> discord.Embed:
        ret = discord.Embed(title=description, colour=self.colour)
        ret.set_author(name=title)
        return ret

    def _add_page(self, page: discord.Embed):
        self._pages.append(page)

    def add_cog(
        self,
        title: typing.Union[str, commands.Cog],
        commands_list: typing.List[commands.Command],
    ):
        cog = isinstance(title, commands.Cog)
        if not commands_list:
            return

        page_title = title.qualified_name if cog else title
        embed = self._new_page(page_title, (title.description or "") if cog else "")

        self._add_commands(embed, page_title, commands_list)

    def _add_commands(
        self, embed: discord.Embed, page_title: str, coms: typing.List[commands.Command]
    ):
        for command in coms:
            if not self._check_embed(
                embed,
                self.ending_note,
                command.name,
                command.short_doc,
            ):
                self._add_page(embed)
                embed = self._new_page(page_title, embed.title)

            if command.help:
                to_add = f"**{command.name}: **"
                if len(command.help) > 30:
                    to_add += command.help[:27] + "..."
                else:
                    to_add += command.help
            else:
                to_add = f"**{command.name}**"
            try:
                embed.description += f"\n{to_add}"
            except TypeError:
                embed.description = to_add
        self._add_page(embed)

    @staticmethod
    def __command_info(command: typing.Union[commands.Command, commands.Group]) -> str:
        info = ""
        if command.description:
            info += command.description + "\n\n"
        if command.help:
            info += command.help + "\n\n"
        if not info:
            return "None"
        return info

    def add_command(self, prefix: str, command: commands.Command, signature: str):
        page = self._new_page(
            title=f"{prefix}{command.qualified_name}",
            description=self.__command_info(command) or "",
        )
        if command.aliases:
            page.title += (
                f"\nAliases: {self.prefix}{', '.join(command.aliases)}{self.suffix}"
            )
        page.description = f"Usage:\n```{signature}```"
        self._add_page(page)

    def add_group(self, group: commands.Group, com_list: typing.List[commands.Command]):
        page = self._new_page(
            group.name,
            self.__command_info(group),
        )
        self._add_commands(page, group.name, com_list)

    def add_index(self, include: bool, title: str, bot: commands.Bot):
        if include:
            index = self._new_page(title=title, description=bot.description or "")

            for num, page in enumerate(self._pages, 1):
                index.add_field(
                    name=f"({num}) {page.title}",
                    value=page.description or "No Description",
                    inline=False,
                )
            index.set_footer(text=self.ending_note)
            self._pages.insert(0, index)
        else:
            self._pages[0].description = bot.description

    @property
    def pages(self):
        if len(self._pages) == 1:
            return self._pages
        ret = []
        for num, page in enumerate(self._pages, 1):
            page.set_footer(text=f"Page: {num}/{len(self._pages)}")
            ret.append(page)
        return ret


class TwilightHelp(commands.HelpCommand):
    """A custom help command by Jojo"""

    def __init__(self, **options):
        self.timeout = options.pop("timeout", 30.0)
        self.index_title = options.pop("index_title", "Categories")
        self.colour = options.pop("colour", 0x00FFFF)
        self.dm_help = options.pop("dm_help", False)
        self.no_category = options.pop("no_category", "No Category")
        self.sort_commands = options.pop("sort_commands", True)
        self.show_index = options.pop("show_index", True)
        self.paginator = Paginator(colour=self.colour)

        super().__init__(**options)

    async def prepare_help_command(
        self, ctx: commands.Context, command: commands.Command = None
    ):
        if ctx.guild is not None:
            perms = ctx.channel.permissions_for(ctx.me)
            if not perms.embed_links:
                raise commands.BotMissingPermissions(["embed links"])
            if not perms.read_message_history:
                raise commands.BotMissingPermissions(["read message history"])
            if not perms.add_reactions:
                raise commands.BotMissingPermissions(["add reactions"])
        self.paginator.clear()
        self.paginator.ending_note = self.get_ending_note()
        await super().prepare_help_command(ctx, command)

    def get_ending_note(self) -> str:
        return (
            "Type {0}{1} command for more info on a command.\n"
            "You can also type {0}{1} category for more info on a category".format(
                self.clean_prefix, self.invoked_with
            )
        )

    async def send_pages(self):
        total = len((pages := self.paginator.pages))
        destination = self.get_destination()

        msg = await destination.send(embed=pages[0])

        if total > 1:
            await TwilightHelpMenu(embeds=pages, msg=msg).start(
                ctx=self.context, channel=destination
            )

    def get_destination(self) -> typing.Union[discord.Member, discord.TextChannel]:
        if self.dm_help:
            return self.context.author
        else:
            return self.context.channel

    async def send_bot_help(self, mapping: dict):
        bot = self.context.bot
        channel = self.get_destination()
        mapping = dict((name, []) for name in mapping)
        help_filtered = (
            filter(lambda c: c.name != "help", bot.commands)
            if len(bot.commands) > 1
            else bot.commands
        )
        for command in await self.filter_commands(
            help_filtered, sort=self.sort_commands
        ):
            mapping[command.cog].append(command)
        self.paginator.add_cog(self.no_category, mapping.pop(None))
        sorted_map = sorted(
        mapping.items(),
        key=lambda cg: cg[0].qualified_name
        if isinstance(cg[0], commands.Cog)
        else str(cg[0]),
        )
        for cog, com_list in sorted_map:
            self.paginator.add_cog(cog, com_list)
        self.paginator.add_index(self.show_index, self.index_title, bot)
        await self.send_pages()

    async def send_command_help(self, command: commands.Command):
        filtered = await self.filter_commands([command])
        if filtered:
            self.paginator.add_command(
                self.clean_prefix, command, self.get_command_signature(command)
            )
            await self.send_pages()

    async def send_group_help(self, group: commands.Group):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                group.commands, sort=self.sort_commands
            )
            self.paginator.add_group(group, filtered)
        await self.send_pages()

    async def send_cog_help(self, cog: commands.Cog):
        async with self.get_destination().typing():
            filtered = await self.filter_commands(
                cog.get_commands(), sort=self.sort_commands
            )
            self.paginator.add_cog(cog, filtered)
        await self.send_pages()
