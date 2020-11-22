# Yes, I'm rewritting the help command :D

### ~~~ Discord imports and the like ~~~ ###
import discord
from discord.utils import get
from discord.ext.commands import (
    command, Cog, Context, Command
)
from discord.ext.menus import MenuPages, ListPageSource
from typing import Optional
### ~~~ Local imports ~~~ ###
from .utils.basic_utils import administrator, moderator, guild_owner
from .utils.embed import Embed
from ..bot import Twilight  # Type hinting


def cmd_and_aliases(command):
    cmd_names = "|".join([str(command), *command.aliases])
    params = []

    for key, value in command.params.items():
        if key not in ("self", "ctx"):
            params.append(f"[{key}]" if "NoneType" in str(
                value) else f"<{key}>")

    params = " ".join(params)

    return f"```>{cmd_names} {params}```"


class HelpMenu(ListPageSource):
    def __init__(self, ctx: Context, data, version):
        self.ctx = ctx
        self.version = version
        super().__init__(data, per_page=3)

    async def write_page(self, menu, fields=[]) -> discord.Embed:
        offset = (menu.current_page*self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed.create(
            self, ctx=self.ctx, title="Twilight Help command",
            description="Running version {}".format(self.version),
            thumbnail=self.ctx.me.avatar_url, footer=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} commands."
        )
        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        fields = []

        for entry in entries:
            fields.append(
                (entry.help or "No description", cmd_and_aliases(entry))
            )

        return await self.write_page(menu, fields)


class Help(Cog):
    """Help command because the normal one sucks! (Don't kill me, Discord)"""

    def __init__(self, bot: Twilight):
        self.bot = bot
        self.bot.remove_command("help")

    @command(name="help")
    async def _help(self, ctx: Context, command: Optional[str]):
        """Shows this message :D"""
        if not command:
            menu = MenuPages(
                source=HelpMenu(
                    ctx, list(self.bot.commands), version=self.bot.version
                ), delete_message_after=False, timeout=30
            )

            await menu.start(ctx)
        else:
            if (com := get(self.bot.commands, name=command)):
                await self.cmd_help(ctx, com)
            else:
                await ctx.send("That command does not exist.")

    async def cmd_help(self, ctx: Context, command: Command):
        embed = Embed.create(
            self, ctx, title="Twilight help command",
            description="Twilight Help. Running version {}".format(
                self.bot.version),
            color=discord.Color.purple(), footer="Twilight help system."
        )
        embed.add_field(name=cmd_and_aliases(command), value=command.help)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("help")


def setup(bot: Twilight):
    bot.add_cog(Help(bot))
