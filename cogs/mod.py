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
### ~~~ Base Discord and other imports ~~~ ###
import discord
from discord.ext.commands import (
    command, Context, check, Cog,
    guild_only, is_owner
)
from typing import Optional

### ~~~ Utils and others ~~~  ###
from utils import Moderation, Getters, moderator, admin
from ..bot import Twilight


class Mod(Cog):
    """self.mod to make sure everything runs smoothly on your Guild"""

    def __init__(self, bot: Twilight):
        self.bot = bot
        self.moder = Moderation()

    async def ban_kick(self, ctx: Context, user: discord.Member, kick_ban: str, reason: str = None, days: int = 0) -> str:
        """Ban or kick a user"""
        _reason = "Banned {} ({}). Action requested by {} ({})".format(
            user.name, user.id, ctx.author.name, ctx.author.id)
        if reason:
            _reason += f" {reason}"
        if ctx.author.id == user.id:
            return "Self harm is bad 😔"
        if user is ctx.guild.owner:
            return "Trying to pull a coup, eh?"

        if kick_ban == "ban":
            try:
                await user.ban(reason=reason, delete_message_days=days)
                if reason:
                    return "Banned {} for the reason {}".format(user, reason)
                else:
                    return "Banned {}".format(user)
            except discord.Forbidden:
                return "I could not ban that member. Sorry"
            else:
                await self.moder.create_case(ctx, ctx.guild, "ban", user)
        else:
            try:
                await user.kick(reason)
                return "Kicked {} for the reason {}".format(user, reason)
            except discord.Forbidden:
                return "I could not kick that member. Sorry"
            else:
                await self.moder.create_case(ctx, ctx.guild, "kick", user)

    @command()
    @moderator()
    @guild_only()
    async def ban(self, ctx: Context, user: discord.Member, days: Optional[int] = 0, *, reason: str = None):
        """Ban a member

        Example:
        `>ban @Jojo Breaking rules`"""
        result = await self.ban_kick(ctx, user, "ban", reason, days)
        await ctx.send(content=result)

    @command()
    @moderator()
    @guild_only()
    async def kick(self, ctx: Context, user: discord.Member, days: Optional[int] = 0, *, reason: str = None):
        """Kick a member

        Example:
        `>kick @Jojo He deserved it!`"""
        result = await self.ban_kick(ctx, user, "kick", reason, days)
        await ctx.send(result)

    @command()
    @moderator()
    @guild_only()
    async def mute(self, ctx: Context, user: discord.Member, channel: discord.TextChannel = None):
        """Mute a member in a channel

        Example:
        `>mute @Jojo #testing`"""
        if channel is None:
            channel = ctx.channel
        result = await self.mute_member(ctx, user, channel)
        await ctx.send(result)

    @command()
    @moderator()
    @guild_only()
    async def unmute(self, ctx: Context, user: discord.Member, channel: discord.TextChannel = None):
        """Unmute a member in a channel

        Example:
        `>unmute @Jojo #testing"""
        if channel is None:
            channel = ctx.channel
        result = await self.unmute_member(ctx=ctx, user=user, channel=channel)
        await ctx.send(result)

    async def mute_member(self, ctx: Context, user: discord.Member, channel: discord.TextChannel) -> str:
        """Channel mute a member"""
        if ctx.guild is None:
            return "This functionality is only available in guilds!"
        if user is ctx.guild.owner:
            return "You can't mute the owner!"
        if user == ctx.author:
            return "Don't mute yourself lol"
        if (
            Getters.get_admin_role(ctx.guild) in user.roles or
            Getters.get_mod_role(ctx.guild) in user.roles
        ):
            return "This user is a mod/admin therefore I cannot mute them"
        try:
            await channel.set_permissions(user, send_messages=False)
        except discord.Forbidden:
            return "I could not mute this user."
        else:
            await self.moder.create_case(ctx, ctx.guild, "mute", user)
        return "Muted {} in {}".format(user.name, channel.mention)

    async def unmute_member(self, ctx: Context, user: discord.Member, channel: discord.TextChannel) -> str:
        """Channel unmute a member"""
        if ctx.guild is None:
            return "This functionality is only available in guilds!"
        if user is ctx.guild.owner:
            return "Owners can't be muted to be unmuted."
        if user == ctx.author:
            return "Let's think logically for a second... how can you type to tell me to unmute you..."
        if (
            Getters.get_admin_role(ctx.guild) in user.roles or
            Getters.get_mod_role(ctx.guild) in user.roles
        ):
            return "Mods and Admins can't be muted so unmuting an unmutable person would be silly"
        try:
            await channel.set_permissions(user, send_messages=True)
        except discord.Forbidden:
            return "I couldn't unmute the user."
        else:
            await self.moder.create_case(ctx=ctx, guild=ctx.guild, action="unmute", user=user)
        return "Unmuted that user"

    async def cog_check(self, ctx):
        return ctx.guild is not None


def setup(bot: Twilight):
    bot.add_cog(Mod(bot))
