import asyncio
import json
import os
import discord
from discord.ext import commands
import traceback


def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return str(prefixes[str(message.guild.id)])


client = commands.Bot(
    command_prefix=commands.when_mentioned_or(str(get_prefix), "."))


@client.event
async def on_ready():
    print("Twilight is in the castle")


@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send('Hey there! this is the message i send when i join a server')
        break


@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    try:
        prefixes.pop(str(guild.id))

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)
    except:
        pass


@client.group()
async def prefix(ctx):
    if ctx.invoked_subcommand is None:
        prefix = get_prefix(ctx)
        await ctx.send("Your prefix is `{0}`!".format(prefix))


@prefix.command()
@commands.has_permissions(administrator=True)
async def update(ctx, prefix):
    if prefix:
        with open("prefixes.json", "r") as f:
            prefixes = json.load(f)

        prefixes[str(ctx.guild.id)] = prefix

        with open("prefixes.json", "w") as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send("Your new prefix is `{0}`!".format(prefix))
    else:
        await ctx.send("You can't make an empty prefix, silly!")


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
