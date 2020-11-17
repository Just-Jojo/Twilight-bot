import discord
from discord.ext.commands import Bot
from discord import Forbidden
from discord.ext.commands import (
    CommandNotFound, MissingRequiredArgument,
    BadArgument, Context
)
from asyncio import sleep


cogs = [
    "core",
    "general",
    # "fun",
    # "mylittlepony",
    # "mod",
]


class Ready(object):
    def __init__(self):
        for cog in cogs:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print("{} online".format(cog))

    def all_ready(self):
        return all([getattr(self, cog) for cog in cogs])


class Twilight(Bot):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        super().__init__(
            command_prefix=[
                ".", ">"
            ],
            owner_ids=[544974305445019651]
        )

    def setup(self):
        for cog in cogs:
            self.load_extension("lib.cogs.{}".format(cog))
            print("{} online".format(cog))
        print("\nCogs loaded\n")

    def run(self, version: str):
        self.__version__ = version

        print("Setting up the bot...\n")
        self.setup()

        with open("./lib/bot/token.txt", "r") as f:
            token = f.read()

        super().run(token)

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            pass  # Fuck you, command not found
        elif isinstance(exc, MissingRequiredArgument) or isinstance(exc, BadArgument):
            await ctx.send_help(ctx.command)
        elif hasattr(exc, "original"):
            if isinstance(exc, Forbidden):
                await ctx.send("Discord has forbidden me to do this.")
            else:
                raise exc.original
        else:
            await ctx.send("`error in command {}. check your console for details`".format(ctx.command))

    async def on_ready(self):
        if not self.ready:
            while not self.cogs_ready.all_ready():
                await sleep(1.5)

            self.ready = True
        else:
            print("Twilight reconnected")

    async def on_message(self, message):
        if message.author.bot:
            pass  # Pesky, pesky bots
        await self.process_commands(message)

    def reload_extension(self, extension: str):
        extension = extension.lower()

        if extension not in cogs:
            return "{} is not in my cog database".format(extension)

        if extension == "core":
            return "Reloading core is not wise as that would break me"
        super().reload_extension("lib.cogs.{}".format(extension))
        return "Reloaded {}".format(extension)

    def load_extension(self, extension: str):
        extension = extension.lower()

        if extension not in cogs:
            return "{} is not in my cog database".format(extension)

        if extension == "core":
            return "Can't load/unload/reload core as it would break *everything*"
        super().load_extension("lib.cogs.{}".format(extension))
        return "Loaded {}".format(extension)

    def unload_extension(self, extension: str):
        extension = extension.lower()
        if extension not in cogs:
            return "{} is not in my cog database".format(extension)

        if extension == "core":
            return "Can't load/unload/reload core as it would break *everything*"
        super().unload_extension("lib.cogs.{}".format(extension))
        return "Unloaded {}".format(extension)


twilight = Twilight()
