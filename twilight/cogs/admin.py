"""
MIT License

Copyright (c) 2021 Jojo#7711

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

import json
import logging
import typing

import discord
from discord.ext import commands

from twilight.utils import admin, is_admin, message_pred, ReactionPredicate

from .abc import Cog
from ..menus import TwilightMenu, TwilightPageSource

Roles = typing.Union[int, discord.Role]
Keys = typing.Literal["admins", "mods", "prefixes", "member_welcome", "member_leave"]


class Admin(Cog):
    """A cog to adjust Twilight's settings for your guild"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("twilight.cogs.Admin")

    @commands.command(name="addadminrole")
    async def admin_set(self, ctx, *roles: Roles):
        """Set roles as an admin role"""
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        act = []
        for role in roles:
            if isinstance(role, int):
                act.append(role)
            else:
                act.append(role.id)
        try:
            self.bot.guild_config[str(ctx.guild.id)]["admins"].extend(act)
        except KeyError:
            self.bot.guild_config[str(ctx.guild.id)] = {
                "prefixes": [],
                "member_welcome": ["Welcome {0.mention} to {1.name}"],
                "member_leave": ["Goodbye {0.name}! We'll miss you!"],
                "welcome_channel": None,
                "admins": act,
                "mods": [],
            }
        finally:
            await self.bot.guild_config.save()

    @commands.command(
        name="removeadminrole",
        aliases=[
            "deladmin",
        ],
    )
    async def remove_admin_roles(self, ctx, *roles: Roles):
        """Remove roles from an admin role"""
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        act = []
        for role in roles:
            if isinstance(role, discord.Role):
                role = role.id
            try:
                self.bot.guild_config[str(ctx.guild.id)]["admins"].remove(role)
            except ValueError:
                pass
        await self.bot.guild_config.save()

    @commands.command(name="prefixset")
    async def prefix_set(self, ctx, *prefixes: str):
        """Set Twilight's prefix for your guild!"""
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        try:
            self.bot.guild_config[str(ctx.guild.id)]["prefixes"].extend(prefixes)
        except KeyError:
            self.bot.guild_config[str(ctx.guild.id)] = {
                "prefixes": prefixes,
                "member_welcome": ["Welcome {0.mention} to {1.name}"],
                "member_leave": ["Goodbye {0.name}! We'll miss you!"],
                "welcome_channel": None,
                "admins": [],
                "mods": [],
            }
        finally:
            await self.bot.guild_config.save()

    @commands.command(name="prefixlist")
    async def prefix_list(self, ctx):
        """List Twilight's prefixes in your guild"""
        prefixes = self.bot.guild_config.get(str(ctx.guild.id), None)
        if prefixes is None:
            return await ctx.send("Hm, it seems that I don't have you in my config")
        if not (prefixes := prefixes["prefixes"]):
            await ctx.send("You don't seem to have any prefixes in your guild...")
        else:
            source = TwilightPageSource(prefixes, "Twilight's Prefixes")
            await TwilightMenu(source=source).start(ctx=ctx, channel=ctx.channel)

    @commands.command(name="prefixremove", aliases=["delprefix"])
    async def remove_prefix(self, ctx, *prefixes: str):
        """Remove prefixes from your guild"""
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        for prefix in prefixes:
            try:
                self.bot.guild_config[str(ctx.guild.id)]["prefixes"].remove(prefix)
            except ValueError:
                pass
        await self.bot.guild_config.save()

    @commands.command()
    async def setmodlog(self, ctx, channel: typing.Union[discord.TextChannel, int]):
        """Set a channel as a modlog channel"""
        await ctx.send("That channel is now the modlog channel!")
        if isinstance(channel, discord.TextChannel):
            channel = channel.id
        try:
            self.bot.guild_config[str(ctx.guild.id)]["modlog_channel"] = channel
        except KeyError:
            await self.bot._check_guild(ctx.guild)
            self.bot.guild_config[str(ctx.guild.id)]["modlog_channel"] = channel
        finally:
            await self.bot.guild_config.save()

    @commands.command()
    async def removemodlog(self, ctx):
        """Remove the current modlog channel"""
        if ctx.channel.permissions_for(ctx.me).add_reactions:
            pred = ReactionPredicate("Would you like to clear the modlog?")
            await pred.prompt(ctx)
            result = pred.confirm
        else:
            await ctx.send("Would you like to clear the modlog? (y/n)")
            result = await message_pred(ctx)
        if result is False:
            return await ctx.send("Okay!")
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        try:
            self.bot.guild_config[str(ctx.guild.id)]["modlog_channel"] = None
        except KeyError:
            await self.bot._check_guild(ctx.guild)
        finally:
            await self.bot.guild_config.save()

    async def cog_check(self, ctx: commands.Context):
        return await is_admin(ctx, ctx.author)


def setup(bot):
    bot.add_cog(Admin(bot))
