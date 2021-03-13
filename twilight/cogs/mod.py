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

import logging
import typing

import discord
from discord.ext import commands

from .abc import Cog, MetaClass
from .abc.mod_events import KickBanMixin

from ..utils import mod, is_mod


class Mod(KickBanMixin, Cog, metaclass=MetaClass):
    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("twilight.cogs.Mod")

    @commands.command()
    async def kick(
        self, ctx, user: discord.Member, *, reason: str = "No reason provided"
    ):
        """Kick a member from your guilid"""
        await self.kick_user(ctx=ctx, user=user, reason=reason)

    @commands.command()
    async def ban(
        self, ctx, user: discord.Member, *, reason: str = "No reason provided"
    ):
        """Ban a member from your guild"""
        await self.ban_user(ctx=ctx, user=user, reason=reason)

    async def cog_check(self, ctx: commands.Context):
        return await is_mod(ctx, ctx.author)

    async def create_modlog_case(
        self, ctx: commands.Context, case_type: str, user: discord.Member, reason: str
    ):
        try:
            modlog = self.bot.guild_config[str(ctx.guild.id)]["modlog_channel"]
        except KeyError:  # TODO Remove this soon
            modlog = None
            await self.bot._check_guild(ctx.guild)
        modlog = ctx.guild.get_channel(modlog)
        if modlog is None:
            return
        data = await self.create_default_embed(
            ctx,
            case_type,
            (user.name, user.id, user.avatar_url),
            ctx.author.name,
            ctx.author.id,
            reason,
        )
        if modlog.permissions_for(ctx.me).embed_links:
            kwargs = {"embed": data[1]}
        else:
            kwargs = {"content": data[0]}
        await modlog.send(**kwargs)

    async def create_default_embed(
        self,
        ctx: commands.Context,
        case_type: str,
        user_data: typing.Tuple[str, int, str],
        mod_name: str,
        mod_id: int,
        reason: str,
    ) -> typing.Tuple[str, discord.Embed]:
        _default_embed = {
            "author": {"name": str(user_data[0]), "icon_url": str(user_data[2])},
            "title": f"{ctx.guild.name} Modlog.",
            "description": f"**Type**: {case_type}",
            "color": 0x00FFFF,
            "fields": [
                {"name": "Case Type", "value": case_type.capitalize(), "inline": False},
                {
                    "name": "User",
                    "value": f"{user_data[0]} ({user_data[1]})",
                    "inline": False,
                },
                {
                    "name": "Moderator",
                    "value": f"{mod_name} ({mod_id})",
                    "inline": False,
                },
                {"name": "Reason", "value": reason, "inline": False},
            ],
            "footer": {
                "text": f"{ctx.guild.name} Moderation",
                "icon_url": str(ctx.guild.icon_url),
            },
        }
        _default = (
            f"{ctx.guild.name} Modlog.\n"
            f"**Type:** {case_type}\n"
            f"**User:** {user_data[0]} ({user_data[1]})\n"
            f"**Moderator:** {mod_name} ({mod_id})\n"
            f"**Reason:** {reason}"
        )
        return _default, discord.Embed.from_dict(_default_embed)

    @commands.Cog.listener()
    async def on_mod_event(
        self, ctx: commands.Context, case_type: str, user: discord.Member, reason: str
    ):
        self.log.info("Testing!")
        await self.create_modlog_case(ctx, case_type, user, reason)


def setup(bot):
    bot.add_cog(Mod(bot))
