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
from utils import Embed, TwilightEmbedMenu
from asyncio import iscoroutine as iscoro


async def send_cog_help(
    ctx: commands.Context,
    cog: typing.Union[commands.Cog, str],
) -> discord.Message:
    """Help for a cog. `cog` can either be a :class:`Cog` or :class:`str`

    If the cog is a string it will find the cog using `ctx.bot`

    Parameters
    ----------
    ctx: :class:`Context`
        Context of the help command
    cog: Union[:class:`Cog`, :class:`str`]
        The cog to get help for. If it is a str it will be searched for using `ctx.bot.get_cog`

    Returns
    -------
    :class:`discord.Message`
        The help message
    """
    bot = ctx.bot
    if isinstance(cog, str):
        cog = bot.get_cog(cog)
    if cog is None:
        return await send_help(ctx)
    try:
        can = await cog.cog_check(ctx)
    except ValueError:
        can = cog.cog_check(ctx)
    if can is False:
        return await send_help(ctx)
    # If the author can't run commands don't display them

    coms = []
    for command in cog.walk_commands():
        if await command.can_run(ctx) is True:
            if len(command.parents) > 0:
                pass
            else:
                if command.help is None:
                    coms.append(f"**{command.name}**")
                else:
                    if len(command.help) > 30:
                        coms.append(
                            f"**{command.name}:** {command.help[:30]}...")
                    else:
                        coms.append(f"**{command.name}:** {command.help}")

    paged = await pagify_commands(coms)
    if hasattr(cog, "__version__"):
        description = f"Cog {cog.qualified_name}. Version {cog.__version__}"
    else:
        description = f"Cog {cog.qualified_name}."
    if len(paged) > 1:
        embeds = []
        for page in paged:
            embed = Embed.create(
                ctx, title="Twilight Help Menu", description=description)
            embed.add_field(name="Commands", value=page)
            embeds.append(embed)
        menu = TwilightEmbedMenu(embeds)
        return await menu.start(ctx=ctx, channel=ctx.channel)
    else:
        embed = Embed.create(
            ctx, title="Twilight Help Menu", description=description,
            footer="Twilight Bot Help!")
        embed.add_field(name="Commands", value=paged[0])
        return await ctx.send(embed=embed)


async def pagify_commands(coms: typing.List[str]) -> typing.List[str]:
    """Takes a list of command names and returns a pagified list

    It will return a page of 15 commands

    Parameters
    ----------
    coms: List[:class:`str`]
        The list of commands to iterate over

    Returns
    -------
    :class:`list`
        A list of pagified commands
    """
    ret = []
    combine = ""
    for i, command in enumerate(coms):
        i += 1
        combine += f"\n{command}"
        if i % 15 == 0:
            ret.append(combine)
            combine = ""
    if combine:
        ret.append(combine)
    return ret


async def send_help(
    ctx: commands.Context
) -> discord.Message:
    """The base help system

    This will iterate over each and every cog and command the bot has

    It uses a custom `discord.ext.menus` Menu to provide pagination

    Parameters
    ----------
    ctx: :class:`Context`
        Context of the message

    Returns
    -------
    :class:`discord.Message`
        The help message
    """
    bot = ctx.bot
    cogs: typing.List[discord.Embed] = []
    for cog in bot.cogs:
        cog: commands.Cog = bot.get_cog(cog)
        try:
            can = await cog.cog_check(ctx)
        except ValueError:
            can = cog.cog_check(ctx)
        if can is False:  # Can't run
            pass
        else:
            coms = []
            for command in cog.walk_commands():
                can = await command.can_run(ctx)
                if can is True:
                    if len(command.parents) > 0:
                        pass
                    else:
                        if command.help is None:
                            coms.append(f"**{command.name}**")
                        else:
                            if len(command.help) > 30:
                                coms.append(
                                    f"**{command.name}:** {command.help[:30]}...")
                            else:
                                coms.append(
                                    f"**{command.name}:** {command.help}")
            paged = await pagify_commands(coms)
            for page in paged:
                embed = Embed.create(
                    ctx, title="Twilight Help Menu", description=f"{cog.qualified_name}.",
                    footer="Twilight Bot Help!")
                embed.add_field(name="Commands", value=page)
                cogs.append(embed)

    if len(cogs) > 1:
        menu = TwilightEmbedMenu(cogs)
        return await menu.start(ctx=ctx, channel=ctx.channel)
    else:
        return await ctx.send(embed=cogs[0])


async def send_command_help(
    ctx: commands.Context,
    command: typing.Union[str, commands.Command]
) -> discord.Message:
    """Send help for a command

    This command can either be a Command or a str

    If the command's type is a str it will fetch that command using `ctx.bot`

    Parameters
    ----------
    ctx: :class:`Context`
        The context of the help command
    command: Union[:class:`str`, :class:`Command`]
        The command to get help for. If it is a string it will fetch that command from the bot

    Returns
    -------
    :class:`discord.Message`
        The help message
    """
    bot = ctx.bot
    if isinstance(command, str):
        command: commands.Command = bot.get_command(command)

    can = await command.can_run(ctx)
    if can is False:
        return  # Shouldn't happen but okay
    full_command = ""
    if len(command.parents) > 0:
        full_command = command.full_parent_name
    else:
        full_command = command.name
    params = []
    for key, value in command.clean_params.items():
        if "None" in str(value):
            params.append(f"[{key}]")
        else:
            params.append(f"<{key}>")
    full_command += " " + " ".join(params)
    desc = command.help if command.help is not None else ""
    embed = Embed.create(
        ctx, author="Twilight Help System", author_url=bot.user.avatar_url, title=f"`Syntax {ctx.prefix}{full_command}`",
        description=desc, footer="Twilight Bot Help!"
    )
    await ctx.send(embed=embed)


async def send_help_for(
    ctx: commands.Context,
    thing: str = None
) -> discord.Message:
    """Send help for an object

    If the object is none it will send the normal help menu

    If the object is a command it will send help for the command
    If the object is a cog it will send help for the cog

    Paramaters
    ----------
    ctx: :class:`Context`
        The context to send the message for
    thing: :class:`str`
        The thing to send help

    """
    if thing is None:
        return await send_help(ctx)
    bot = ctx.bot
    maybe_cog = bot.get_cog(thing)
    if maybe_cog:
        return await send_cog_help(ctx=ctx, cog=maybe_cog)
    maybe_com = bot.get_command(thing)
    if maybe_com:
        return await send_command_help(ctx, command=maybe_com)
    return await send_help(ctx)


@commands.command(name="help")
async def twilight_help(ctx, *, thing_to_find: str = None):
    """Twilight's help command!"""
    await send_help_for(ctx, thing=thing_to_find)
