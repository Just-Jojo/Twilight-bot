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

import logging
from copy import copy

import discord
from discord.ext import commands, tasks

from twi_secrets import LOG_PATH
from twilight.menus import TwilightMenu, TwilightPageSource
from twilight.utils.formatting import tick, box

from .abc import Cog


class Dev(Cog):
    """Developer commands for Twilight"""

    def __init__(self, bot: "Twilight"):
        self.bot = bot
        self.log = logging.getLogger("twilight.cogs.Dev")
        self.clear = False
        self.clear_logs.start()

    @commands.command()
    async def load(self, ctx, cog: str):
        """Load a cog!"""
        try:
            self.bot.load_extension(f"twilight.cogs.{cog}")
        except commands.ExtensionAlreadyLoaded:
            await ctx.send("That cog has already been loaded!")
        except commands.ExtensionNotFound:
            await ctx.send("Hm, I couldn't find that cog")
        except (commands.ExtensionFailed, Exception) as exc:
            msg = tick(f"Error in loading '{cog}'. Please check your logs")
            await ctx.send(content=msg)
            await ctx.send(f"Details:\n{box(exc, 'py')}")
            self.log.exception(
                f"Could not load {cog} for the following reason:\n", exc_info=exc
            )
        else:
            await ctx.send(f"Loaded '{cog}'")

    @commands.command()
    async def unload(self, ctx, cog: str):
        """Unload a cog!"""
        try:
            self.bot.unload_extension(f"twilight.cogs.{cog}")
        except commands.ExtensionNotLoaded:
            await ctx.send("That cog wasn't loaded")
        except commands.ExtensionNotFound:
            await ctx.send("Hm, I couldn't find that cog")
        except (commands.ExtensionFailed, Exception) as exc:
            msg = tick(f"Error in unloading '{cog}'. Please check your logs")
            await ctx.send(content=msg)
            await ctx.send(f"Details:\n{box(exc, 'py')}")
            self.log.exception(
                f"Could not load {cog} for the following reason:\n", exc_info=exc
            )
        else:
            await ctx.send(f"Unloaded '{cog}'")

    @commands.command(name="reload")
    async def reload_cog(self, ctx, cog: str):
        """Reload a cog!"""
        try:
            self.maybe_reload(cog)
        except commands.ExtensionNotFound:
            await ctx.send("Hm, I couldn't find that cog")
        except (commands.ExtensionFailed, Exception) as exc:
            msg = tick(f"Error in reloading '{cog}'. Please check your logs")
            await ctx.send(content=msg)
            await ctx.send(f"Details:\n{box(exc, 'py')}")
            self.log.exception(
                f"Could not load {cog} for the following reason:\n", exc_info=exc
            )
        else:
            await ctx.send(f"Reloaded '{cog}'")

    def maybe_reload(self, cog: str):
        try:
            self.bot.reload_extension(f"twilight.cogs.{cog}")
        except commands.ExtensionNotLoaded:
            self.bot.load_extension(f"twilight.cogs.{cog}")

    @commands.command()
    async def shutdown(self, ctx):
        """Have Twilight shutdown"""
        await ctx.send("Okay, I'm shutting down!")
        await self.bot.shutdown()

    @commands.command()
    async def restart(self, ctx):
        """Restart Twilight"""
        await ctx.send("Okay, I'm restarting!")
        await self.bot.shutdown(True)

    @commands.command()
    async def mock(self, ctx, user: discord.Member, *, command: str):
        """Use a command as a user"""
        msg = copy(ctx.message)
        msg.author = user
        msg.content = ctx.prefix + command

        self.bot.dispatch("message", msg)

    @commands.group()
    async def blacklist(self, ctx):
        """Commands for working with Twilight's Blacklist"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @blacklist.command(name="add")
    async def blacklist_add(self, ctx, id: int):
        """Add an id to the blacklist"""
        await self.bot.add_to_blacklist(id)
        await ctx.send("Added that id to the blacklist")

    @blacklist.command(name="remove", aliases=["del", "rm"])
    async def blacklist_remove(self, ctx, id: int):
        """Remove an id from the blacklist"""
        await self.bot.remove_from_blacklist(id)
        await ctx.send("Removed that id from the blacklist")

    @blacklist.command(name="list")
    async def blacklist_list(self, ctx):
        """List the ids in the blacklist"""
        if len(self.bot.blacklist):
            await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
            source = TwilightPageSource(
                list(self.bot.blacklist.keys()), title="Blacklist List"
            )
            await TwilightMenu(source=source).start(
                ctx=ctx, channel=ctx.author.dm_channel
            )
        else:
            await ctx.send("The blacklist is empty!")

    @commands.command()
    async def trace(self, ctx):
        """Send the latest traceback"""
        sending = await self.format_trace()
        if sending is None:
            return await ctx.send("No Exception has occured!")
        source = TwilightPageSource(sending, "Traceback")
        await TwilightMenu(source=source).start(ctx)

    async def format_trace(self):
        trace = self.bot.trace
        if trace is None:
            return None
        ret = []
        to_app = ""
        for i in trace.split("\n"):
            i = f"\n{i}"
            if len(to_app + i) > 2000:
                ret.append(box(to_app, "py"))
                to_app = ""
            to_app += i
        if to_app:
            ret.append(box(to_app, "py"))
        return ret

    @tasks.loop(hours=24)
    async def clear_logs(self):
        # I wouldn't like the bot to wipe logs
        # every time this cog is reloaded
        # so I added a simple switch
        if self.clear:
            with open(LOG_PATH, "w+"):
                pass
            self.log.info("Cleared Logs.")
        else:
            self.clear = True

    async def cog_check(self, ctx: commands.Context):
        return await ctx.bot.is_owner(ctx.author)
