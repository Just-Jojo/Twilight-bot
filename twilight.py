import asyncio
import json
import os
import discord
from discord.ext import commands
import traceback


client = commands.Bot(command_prefix=(">", "."))
with open("version.json", "r") as f:
    __version__ = json.load(f)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=">help | Version {version}".format(version=__version__)))
    print("Twilight is in the castle")


@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Loaded {extension}")


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Unloaded {extension}")


@client.command(name="reload", aliases=["cu"], hidden=True)
@commands.is_owner()
async def reload_cogs(ctx, extension: str = None):
    if extension == None:
        x = [i for i in client.cogs]
        for cog in x:
            client.reload_extension("cogs.{0}".format(cog.lower()))
        await ctx.send("Reloaded cogs. You can use their commands now")
        print("\nreloaded cogs\n")

    elif extension:
        client.reload_extension("cogs.{0}".format(extension))
        await ctx.send("Reloaded {0}".format(extension))
        print("\n{0} was reloaded".format(extension))

    else:
        await ctx.send("I could not find that cog. Sorry")


@client.command(name="version", hidden=True)
@commands.is_owner()
async def versionupdate(ctx, *, version: str = None):
    if version is not None:
        with open("version.json", "w") as f:
            json.dump(version, f)
        with open("version.json", "r") as f:
            __version__ = json.load(f)
        await client.change_presence(activity=discord.Game(name=">help | Version {version}".format(version=__version__)))
        await ctx.send("Version updated to {version}".format(version=version))

    else:
        await ctx.send("My version is {0}".format(__version__))


@client.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down. Goodbye")
    await client.logout()


with open("bot.txt", "r") as f:
    bot_key = f.read()

for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        try:
            client.load_extension("cogs.{0}".format(cog[:-3]))
            print("{0} online".format(cog[:-3]))
        except:
            continue

client.run(bot_key, reconnect=True)
