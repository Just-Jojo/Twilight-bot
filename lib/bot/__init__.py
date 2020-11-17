import discord
from discord.ext.commands import Bot as BotBase
from discord import Forbidden
from discord.ext.commands import (
    Context, CommandNotFound, BadArgument, MissingRequiredArgument,
)
from asyncio import sleep


cogs = [
    "general",
    "core",
    "mylittlepony"
]

OWNERS = [544974305445019651, ]
IGNORE_EXECEPTIONS = (CommandNotFound, BadArgument)


class Ready(object):
    def __init__(self):
        for cog in cogs:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)
        print("{} is ready\n".format(cog))

    def all_ready(self):
        return all([getattr(self, cog) for cog in cogs])


class Twilight(BotBase):
    def __init__(self):
        self.ready = False
        self.cogs_ready = Ready()
        super().__init__(command_prefix=">", owner_ids=OWNERS)

    def setup(self):
        for cog in cogs:
            self.load_extension("lib.cogs.{}".format(cog))
            print("{} loaded".format(cog))
        print("Cogs loaded")

    def run(self, version):
        self.VERSION = version

        print("Waking up Twilight")
        self.setup()

        with open("./lib/bot/token.txt", "r") as token:
            self.TOKEN = token.read()

        print("Giving Twilight coffee")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message)
        if ctx.command is not None:
            await self.invoke(ctx)

    async def on_command_error(self, ctx, exc):
        if any([isinstance(exc, error) for error in IGNORE_EXECEPTIONS]):
            return
        elif isinstance(exc, MissingRequiredArgument):
            return await ctx.send_help(ctx.command)
        await ctx.send("`Error in command '{}'. Check your console for details`".format(ctx.command))
        if hasattr(exc, "original"):
            if isinstance(exc, Forbidden):
                await ctx.send("Discord has forbidden me to do that")
            else:
                raise exc.original
        else:
            raise exc

    async def on_ready(self):
        if not self.ready:
            while not self.cogs_ready.all_ready():
                await sleep(1.5)

            self.ready = True
        else:
            print("Bot reconnected")

    async def on_message(self, message):
        if message.author.bot:
            return  # Pesky bots
        await self.process_commands(message)

    def reload_extension(self, extension: str):
        extension = extension.lower()
        if extension not in cogs:
            return "I don't have a cog named `{}`".format(extension)
        if extension == "core":
            return "I can't reload/unload `core` as it would break Twilight"
        else:
            super().reload_extension("lib.cogs.{}".format(extension))
            return "Reloaded `{}`".format(extension)


twilight = Twilight()
