import ast
import asyncio
import inspect
import json
import os
import random
import re
import typing

import discord
from bot import Twilight
from discord.ext import commands, tasks
from tabulate import tabulate
from twi_secrets import LONG_TRACEBACK
from utils import (Embed, ReactionPred, TwilightEmbedMenu, TwilightMenu,
                   TwilightPages, box, get_settings, tick)

from cogs.mixin import BaseCog

START_CODE_BLOCK_RE = re.compile(
    r"^((```py)(?=\s)|(```))")


class DevCommands(BaseCog):
    """Commands for Jojo mostly debugging Twilight."""
    __version__ = "0.1.2"

    def __init__(self, bot: Twilight):
        self.bot = bot
        self.save_database.start()

    def cog_unload(self):
        self.save_database.cancel()

    @staticmethod
    def cleanup_code(content):
        if content.startswith("```") and content.endswith("```"):
            return START_CODE_BLOCK_RE.sub("", content)[:-3]
        return content.strip("` \n")

    @staticmethod
    def async_compile(source: str, filename: str, mode: str):
        return compile(source, filename, mode, flags=ast.PyCF_ALLOW_TOP_LEVEL_AWAIT, optimize=0)

    @staticmethod
    async def maybe_await(coro):
        for i in range(2):
            if inspect.isawaitable(coro):
                coro = await coro
            else:
                return coro
        return coro

    @staticmethod
    def get_syntax_error(e):
        if e.text is None:
            return box("{0.__class__.__name__}: {0}".format(e), lang="py")
        return box(
            "{0.text}\n{1:>{0.offset}}\n{2}: {0}".format(e, "^", type(e).__name__), lang="py"
        )

    @staticmethod
    def sanitize_output(ctx, input_: str):
        token = ctx.bot.http.token
        return re.sub(re.escape(token), "[EXPUNGED]", input_, re.I)

    @commands.command(name="reload", aliases=["cu", "update"])
    async def twilight_cog_reload(self, ctx, cog: str):
        """Reload a cog"""
        cog = cog.lower()
        cogs = self.bot.grab_cogs()
        if cog not in cogs.keys():
            await ctx.send(f"I don't have a cog named `{cog}`")
            return  # Return here to not break it
        self.bot.reload_extension(cog)
        await ctx.send(f"Reloaded `{cog}`")

    @commands.command()
    async def shutdown(self, ctx):
        """Shuts Twilight down"""
        await ctx.send("Shutting down Twilight")
        await self.bot.async_stop(0)

    @commands.command()
    async def restart(self, ctx):
        """Attempts to restart the bot"""
        await ctx.send("Restarting...")
        await self.bot.async_stop(4)

    @commands.command()
    async def trace(self, ctx):
        """Sends the latest traceback error"""
        if self.bot.last_exception == None:
            return await ctx.send("No exceptions have occured yet!")
        if len(self.bot.last_exception) > 2000:
            embeds = []
            trace = self.long_traceback()
            for line in trace:
                embed = Embed.create(
                    ctx, title="Traceback Error", description=line)
                embeds.append(embed)
            menu = TwilightEmbedMenu(embeds)
            await menu.start(ctx=ctx, channel=ctx.channel)
        else:
            embed = Embed.create(
                ctx, title="Traceback Error", description=box(self.bot.last_exception, "py"))
            await ctx.send(embed=embed)

    def long_traceback(self):
        traceback = self.bot.last_exception.split("\n")
        returning = []
        ret = ""
        for line in traceback:
            if len(ret + f"\n{line}") > 2000:
                returning.append(box(ret, "py"))
                ret = ""
            ret += f"\n{line}"
        if ret:  # Just in case it didn't get added
            returning.append(box(ret, "py"))
        return returning

    @commands.command()
    async def debug(self, ctx, *, code: str):
        """Debug Python code"""
        env = {
            "ctx": ctx,
            "bot": ctx.bot,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "aysncio": asyncio,
            "discord": discord,
            "commands": commands,
            "__name__": "__main__"
        }
        code = self.cleanup_code(code)
        try:
            compiled = self.async_compile(code, "<string>", "eval")
            result = await self.maybe_await(eval(compiled, env))
        except SyntaxError as e:
            await ctx.send(self.get_syntax_error(e))
            return
        except Exception as e:
            await ctx.send(box("{}: {!s}".format(type(e).__name__, e), lang="py"))
            return

        result = self.sanitize_output(ctx, str(result))
        await ctx.send(box(result, lang="py"))
        await tick(ctx.message)

    @commands.command()
    async def error(self, ctx, long_trace: bool = False):
        """Error the bot"""
        if long_trace:
            raise Exception(LONG_TRACEBACK)
        raise Exception("Used command `error`")

    @commands.group()
    async def blocklist(self, ctx):
        """Base command for the blocklist settings"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @blocklist.group()
    async def guild(self, ctx):
        """Base guild related blocklist"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @guild.command(name="list")
    async def guild_list(self, ctx):
        """List the blocklisted guilds"""
        if len(self.bot.blocklist["guilds"]) < 1:
            return await ctx.send("There aren't any guilds in the blocklist!")
        paged = self.guild_paginate()
        embeds = []
        for page in paged:
            embed = Embed.create(
                ctx, title="Blocklisted guilds", description=box(page))
            embeds.append(embed)
        if len(embeds) == 1:
            return await ctx.send(embed=embeds[0])
        menu = TwilightEmbedMenu(embeds)
        await menu.start(ctx=ctx, channel=ctx.channel)

    def guild_paginate(self):
        """Paginate the guild blocklist"""
        blocked = self.bot.blocklist["guilds"]
        ret = []
        string = ""
        for guild in blocked:
            if len(string + f"\n{guild}") > 1800:
                ret.append(string)
                string = ""
            string += f"\n{guild}"
        if string:
            ret.append(string)
        return ret

    @guild.command(name="add")
    async def guild_add(self, ctx, guild_id: int):
        """Add a guild to the blocklist via id"""
        try:
            guild = await self.bot.fetch_guild(guild_id)
            await guild.leave()
        except:
            pass
        self.bot.guild_blocklist.append(guild_id)
        self.bot.save_blocklist()
        await ctx.send("Added that guild to the blocklist")

    @guild.command(name="remove", aliases=["del", ])
    async def member_remove(self, ctx, guild_id: int):
        """Remove a guild from the blocklist via id"""
        self.bot.guild_blocklist.pop(self.bot.guild_blocklist.index(guild_id))
        self.bot.save_blocklist()
        await ctx.send("Removed that guild from the blocklist")

    @blocklist.command(name="list")
    async def member_list(self, ctx):
        """List the members in the blocklist"""
        if len(self.bot.blocklist["users"]) < 1:
            return await ctx.send("There aren't any members in the blocklist yet!")
        paged = self.paginate_blocked()
        embeds = []
        for page in paged:
            embed = Embed.create(
                ctx, title="Blocklisted members", description=box(paged))
            embeds.append(embed)
        if len(embeds) == 1:
            return await ctx.send(embed=embeds[0])
        menu = TwilightEmbedMenu(embeds)
        await menu.start(ctx=ctx, channel=ctx.channel)

    def paginate_blocked(self):
        """Paginate blocklisted members"""
        user_block = self.bot.blocklist["users"]
        ret = []
        string = ""
        for users in user_block:
            if len(string + f"\n{users}") > 1800:
                ret.append(string)
                string = ""
            string += f"\n{users}"
        if ret:
            ret.append(string)
        return ret

    @blocklist.command()
    async def add(self, ctx, member: typing.Union[discord.Member, int]):
        """Add a user to the blocklist"""
        if isinstance(member, discord.Member):  # If the user isn't an int get the id
            member = member.id
        if member in self.bot.blocklist["users"]:
            return await ctx.send("That user is already in the blocklist!")
        self.bot.blocklist["users"].append(member)
        self.bot.save_blocklist()  # save it from the command incase it doesn't work
        await ctx.send(f"Added that user to the blocklist")

    @blocklist.command()
    async def remove(self, ctx, member: typing.Union[discord.Member, int]):
        """Remove a user from the blocklist"""
        if isinstance(member, int):  # Same thing
            self.bot.blocklist.pop(member)
        else:
            self.bot.blocklist.pop(member.id)
        self.bot.save_blocklist()  # save it from the command incase it doesn't work
        await ctx.send("Removed that user from the blocklist")

    @commands.command()
    async def load(self, ctx, cog: str):
        """Load a cog"""
        self.bot.load_extension(cog)
        await ctx.send(content=f"Loaded `{cog}`")

    @commands.command()
    async def unload(self, ctx, cog: str):
        """Unload a cog"""
        if cog.lower() == "dev":
            await ctx.send(content="Mate... what are you doing?")
            return
        self.bot.unload_extension(cog)
        await ctx.send(content=f"Unloaded `{cog}`")

    @commands.command()
    async def cogs(self, ctx):
        """List the cogs and their loaded state"""
        cogs = self.bot.grab_cogs()
        embed = Embed.create(ctx, title="Cogs")
        cogs_list = []
        for key, value in cogs.items():
            _list = []
            _list.append(key)
            _list.append(value)
            # Not the prettiest thing ever but it'll work...
            cogs_list.append(_list)
        embed.description = box(
            tabulate(cogs_list, ("Cog Name", "Loaded")), "md")
        await ctx.send(embed=embed)

    @commands.command()
    async def test(self, ctx):
        """Testing command"""
        text = LONG_TRACEBACK.split("\n")
        pages = TwilightPages(data=text, use_embeds=True)
        menu = TwilightMenu(source=pages)
        await menu.start(ctx=ctx, channel=ctx.channel)

    async def cog_check(self, ctx):
        return ctx.author.id == 544974305445019651

    @tasks.loop(hours=4)  # This *should* be called every 4 hours
    async def save_database(self):
        """Save the database in case I fuck up"""
        current_settings = get_settings()
        from twi_secrets import TEMP_DATABASE
        file_ext = random.randint(10000000, 5000000000)
        full_path = os.path.join(TEMP_DATABASE, f"db_backup.{file_ext}.json")
        with open(full_path, "w+") as fp:
            json.dump(current_settings, fp, indent=4)
        print("Saved to database")


def setup(bot: Twilight):
    bot.add_cog(DevCommands(bot))
