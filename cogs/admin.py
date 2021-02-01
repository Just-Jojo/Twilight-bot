from typing import List, Union

import discord
from bot import grab_prefix, help
from bot.help import send_help_for
from discord.ext import commands
from utils import (get_guild_settings, get_settings, guild_setup, is_admin,
                   write_settings)

from .mixin import BaseCog


class Admin(BaseCog):
    """Administration commands for Twilight"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="set")
    async def twilight_settings(self, ctx):
        """Base Twilight settings"""
        if ctx.invoked_subcommand is None:
            await send_help_for(ctx, ctx.command.name)

    @twilight_settings.group()
    async def prefix(self, ctx, prefix: str = None):
        """Set Twilight's prefix!"""
        if ctx.invoked_subcommand is None:
            if prefix is None:
                return await send_help_for(ctx=ctx, thing=ctx.command.qualified_name)
            prefixes = grab_prefix(self.bot, ctx.message)
            if prefix in prefixes:
                return await ctx.send("That is already a prefix!")
            settings = get_settings()
            try:
                settings[str(ctx.guild.id)]["prefixes"].append(prefix)
            except KeyError:
                guild_setup(ctx.guild)
                settings = get_settings()
                settings[str(ctx.guild.id)]["prefixes"].append(prefix)
            write_settings(settings)
            await ctx.send("Added that as a prefix!")

    @prefix.command(aliases=("del",))
    async def remove(self, ctx, prefix: str = None):
        """Remove a prefix from Twilight's prefixes"""
        if prefix is None:
            return await send_help_for(ctx=ctx, thing=ctx.command.qualified_name)
        prefixes = grab_prefix(bot=self.bot, msg=ctx.message)
        try:
            self.settings_handler(prefix, guild=ctx.guild, delete=True)
        except ValueError:
            await ctx.send("I could not find that prefix!")
        else:
            await ctx.send("Removed that prefix!")

    def prefix_settings_handler(self, *settings: str, guild: discord.Guild, delete: bool):
        """Write prefix settings without having to rewrite the logic

        Parameters
        ----------
        settings: List[:class:`str`]
            The settings to write
        guild: :class:`discord.Guild`
            The guild to write the settings for
        """
        guild_settings = get_guild_settings(guild=guild)
        base_settings = get_settings()  # This needs to be below since if the guild
        if delete is True:              # isn't in the database `get_guild_settings` will add it
            for prefix in settings:
                guild_settings["prefixes"].remove(prefix)
        else:
            for prefix in settings:
                guild_settings["prefixes"].append(prefix)
        base_settings[str(guild.id)] = guild_settings
        write_settings(settings=base_settings)

    async def cog_check(self, ctx: commands.Context):
        """Admin checks"""
        return await is_admin(ctx, ctx.author)


def setup(bot):
    bot.add_cog(Admin(bot))
