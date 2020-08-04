import asyncio

import os

import discord
from discord.ext import commands

import traceback

client = commands.Bot(command_prefix=">")
client.remove_command("help")

with open("cogs.txt", "r") as f:
    loaded_cogs = f.readlines()

with open("uncogs.txt", "r") as f:
    unloaded_cogs = f.readlines()


@client.event
async def on_ready():
    print("Twilight is in the castle")


@client.command(help="Probably the most important command")
async def about(ctx):
    with open("about.txt", "r") as f:
        about_message = f.read()

    embed = discord.Embed(
        title="About Twilight",
        description=about_message, color=discord.Color.purple()
    )
    embed.set_footer(
        text="Jojo#7791", icon_url="https://media.discordapp.net/attachments/707431591051264121/722163555956162660/Jojospfp.png"
    )
    await ctx.send(embed=embed)


@client.command(help="Pong!")
async def ping(ctx):
    await ctx.send("Pong!")


@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    if extension in unloaded_cogs:
        unloaded_cogs.pop(unloaded_cogs.index(extension))
        loaded_cogs.append(extension)
    await ctx.send(f"Loaded {extension}")


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    if extension in loaded_cogs:
        loaded_cogs.pop(loaded_cogs.index(extension))
        unloaded_cogs.append(extension)
    await ctx.send(f"Unloaded {extension}")


@client.command(aliases=["cu"], hidden=True)
@commands.is_owner()
async def reload(ctx, extension: str = None):
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


@client.command(hidden=True)
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("Shutting down. Goodbye")
    await client.logout()


@client.command(hidden=True)
@commands.is_owner()
async def cogs(ctx):
    lo_cog = ", ".join(loaded_cogs)
    unlo_cog = ", ".join(unloaded_cogs)
    await ctx.send("""```diff
+ Loaded cogs
    {0}
    
- Unloaded cogs
    {1}```""".format(lo_cog, unlo_cog))


@client.command(hidden=True)
@commands.is_owner()
async def invite(ctx):
    await ctx.send("https://discord.com/api/oauth2/authorize?client_id=734159757488685126&permissions=8&scope=bot")

with open("bot_key.txt", "r") as f:
    bot_key = f.read()

for cog in loaded_cogs:
    if cog.endswith("\n"):
        client.load_extension("cogs.{0}".format(cog[:-1]))
    else:
        client.load_extension("cogs.{0}".format(cog))


client.run(bot_key, reconnect=True)
