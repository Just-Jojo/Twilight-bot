"""MIT License

Copyright (c) 2020 Jojo#7711

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
SOFTWARE."""

import discord
from discord.ext import commands
import typing


def maybe_cog(bot: "Twilight", cog: str) -> typing.Union[commands.Cog, commands.Command, None]:
    """Check if a string is a cog or command"""
    maybe = bot.get_cog(cog)
    if maybe:
        return maybe
    maybe = bot.get_command(cog)
    if maybe:
        return maybe
    return None


def cog_parser(bot: "Twilight", cog: commands.Cog) -> discord.Embed:
    """Parse a cog's commands and return in a neat embed"""
    embed = discord.Embed(title=f"{cog.qualified_name} Help")
    embed.set_author(name="Twilight Help System", icon_url=bot.user.avatar_url)
    coms = []
    for command in cog.walk_commands():
        if command.help is not None:
            coms.append(
                f"**{command.qualified_name}:** {command.help[:30] if len(command.help) > 30 else command.help}...")
        else:
            coms.append(f"**{command.qualified_name}**")
    embed.description = "\n".join(coms)
    embed.set_footer(text="Use `>help` for help!")
    return embed


def command_parser(bot: "Twilight", command: commands.Command) -> discord.Embed:
    """Parse a command's parameters and help and return it in a neat embed"""
    embed = discord.Embed()
    embed.set_author(name="Twilight Help System", icon_url=bot.user.avatar_url)
    params = []
    for key, value in command.clean_params.items():
        if "None" in str(value):
            params.append(f"[{key}]")
        else:
            params.append(f"<{key}>")
    com_description = f"`>{command.name} {' '.join(params)}`" if len(
        params) > 0 else f"`>{command.name}`"
    embed.description = f"{com_description}\n\n**{command.help}**" if command.help is not None else com_description
    embed.set_footer(text="Use `>help`")
    return embed


async def send_help(ctx: commands.Context, bot: "Twilight"):
    embed = discord.Embed(title="Twilight Main Help")
    embed.set_author(name="Twilight Help System", icon_url=bot.user.avatar_url)
    for cog in bot.cogs.items():
        embed.add_field(name=cog[0], value=", ".join(
            [f"`{x}`" for x in cog[1].walk_commands()]), inline=False)
    await ctx.send(embed=embed)


async def send_help_for(ctx: commands.Context, thing: str):
    """Send help for a thing"""
    bot = ctx.bot
    if thing is None:
        return await send_help(ctx, bot)
    parsed = maybe_cog(bot, thing)
    if not parsed:
        return await send_help(ctx, bot)
    if isinstance(parsed, commands.Cog):
        embed = cog_parser(bot, parsed)
    else:
        embed = command_parser(bot, parsed)
    await ctx.send(embed=embed)


@commands.command()
async def help(ctx, *, thing: str = None):
    """Help for all!"""
    await send_help_for(ctx, thing)
