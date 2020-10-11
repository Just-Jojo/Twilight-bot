import asyncio
import json
import os
import discord
from discord.ext import commands
import traceback
import twilight_tools
import subprocess as subp

client = commands.Bot(
    command_prefix=commands.when_mentioned_or("."))


@client.event
async def on_ready():
    print("Twilight is in the castle")

# Only have the load/unload/reload/off commands here
# Every other command (including owner only) should at least go into General


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
        relo_cogs = []
        fail_cog = []
        for cog in x:
            try:
                client.reload_extension("cogs.{0}".format(cog.lower()))
                relo_cogs.append(cog)
            except:
                fail_cog.append(cog)
        await ctx.send("Reloaded cogs. You can use their commands now\nReloaded: {0}, Failed (if any): {1}".format(relo_cogs, fail_cog))
        print("\nreloaded cogs\n")

    elif extension:
        client.reload_extension("cogs.{0}".format(extension))
        await ctx.send("Reloaded {0}".format(extension))
        print("\n{0} was reloaded".format(extension))

    else:
        await ctx.send("I could not find that cog. Sorry")


@client.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down. Goodbye")
    await client.logout()


@client.command(hidden=True)
@commands.is_owner()
async def pull(ctx):
    try:
        subp(["git", "pull"], shell=False)
        await asyncio.sleep(5)
        await ctx.send("Pulled the code. Please reload the cogs")
    except:  # Gonna have a bare except here because uh... I don't know what type of errors it's going to throw
        await ctx.send("There was an error!")
        traceback.print_exc()


with open("bot.txt", "r") as f:
    bot_key = f.read()

for cog in os.listdir("./cogs"):
    test = []
    if cog.endswith(".py"):
        try:
            client.load_extension("cogs.{0}".format(cog[:-3]))
            print("{0} online".format(cog[:-3]))
            test.append(cog[:-3])
        except commands.errors.NoEntryPointError:
            continue
        except:
            traceback.print_exc()
            continue
    test_ = ", ".join(test)

client.run(bot_key, reconnect=True)
