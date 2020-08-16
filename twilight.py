import asyncio
import json
import os
import discord
from discord.ext import commands
import traceback


def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client = commands.Bot(command_prefix=get_prefix)
client.remove_command("help")


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name=">help"))
    print("Twilight is in the castle")


@client.event
async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = ">"

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


@client.command()
@commands.has_guild_permissions(administrator=True)
async def prefix(ctx, arg):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = arg

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send("Your prefix is now `{0}`".format(arg))


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
    await ctx.send(f"Loaded {extension}")


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
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
async def invite(ctx):
    embed = discord.Embed(
        title="Invite/Support server",
        color=discord.Color.blue(),
    )
    embed.add_field(name="Get the bot",
                    value="[bot invite link](https://discord.com/api/oauth2/authorize?client_id=734159757488685126&permissions=8&scope=bot)")
    embed.add_field(name="Support server",
                    value="Join the [server](https://www.discord.gg/9cxxJSp) for help")
    await ctx.send(embed=embed)

with open("bot_key.txt", "r") as f:
    bot_key = f.read()

for cog in os.listdir("./cogs"):
    if cog.endswith(".py"):
        client.load_extension("cogs.{0}".format(cog[:-3]))
        print("{0} online".format(cog[:-3]))

client.run(bot_key, reconnect=True)
