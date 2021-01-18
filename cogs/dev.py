#pylint: disable=unused-variables
import discord
from discord.ext import commands
from discord.ext.commands import *
from utils import box, tick, Embed
import asyncio
import re
import ast
import inspect
from bot import Twilight
from cogs.mixin import BaseCog
from twi_secrets import LONG_TRACEBACK

START_CODE_BLOCK_RE = re.compile(
    r"^((```py)(?=\s)|(```))")  # this is Red's. I don't understand regex lol


class DevCommands(BaseCog):
    """Commands for Jojo mostly debugging Twilight."""

    def __init__(self, bot: Twilight):
        self.bot = bot

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
    def sanitize_output(ctx: Context, input_: str):
        token = ctx.bot.http.token
        return re.sub(re.escape(token), "[EXPUNGED]", input_, re.I)

    @command()
    async def debug(self, ctx: Context, *, code: str):
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
        tick(ctx.message)

    @command()
    async def error(self, ctx: Context, _long: bool = False):
        """Error the bot"""
        if _long:
            raise Exception(LONG_TRACEBACK)
        raise Exception("Used command `error`")

    @command()
    async def reloadcore(self, ctx: Context, confirm: bool = False):
        """Reload the core cog. Very dangerous"""
        if not confirm:
            await ctx.send(content="Please confirm that you want to reload core using `>reloadcore True`")
            return
        self.bot.reload_extension("x", True)
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    async def cog_check(self, ctx):
        return ctx.author.id == 544974305445019651


def setup(bot: Twilight):
    bot.add_cog(DevCommands(bot))
