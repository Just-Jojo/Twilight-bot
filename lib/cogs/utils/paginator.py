# Behold, Perry the Platypus, my Paginator!
# pylint:disable=unused-variables
import discord
from discord.ext.commands import *
from typing import *
from .errors import *
import asyncio
from contextlib import suppress  # This is handy


async def menu(
    ctx: Context,
    pages: List[discord.Embed],
    controls: dict,
    message: discord.Message = None,
    page: int = 0,
    timeout: float = 30.0
):
    """You see, Perry the Platypus, when I was young my family lived far from the newspaper stand..."""
    for key, value in controls.items():
        coro = value

    current_page = pages[page]
    if not message:
        await ctx.send(embed=current_page)
    else:
        try:
            await message.edit(embed=current_page)
        except discord.NotFound:
            return
    pass


async def next_page(
    ctx: Context,
    pages: List[discord.Embed],
    message: discord.Message,
    controls: dict,
    page: int,
    timeout: float,
    emoji: str
) -> None:
    """I was the one they sent out to get a newspaper every morning..."""
    perms = message.channel.permissions_for(ctx.me)
    if perms.manage_messages:
        with suppress(discord.NotFound):
            await message.remove_reaction(emoji, ctx.author)
    if page == len(pages) - 1:
        page = 0
    else:
        page += 1
    return await menu(ctx, pages, controls, message, page, timeout)


async def previous_page(
    ctx: Context,
    pages: List[discord.Embed],
    message: discord.Message,
    controls: dict,
    page: int,
    timeout: float,
    emoji: str
):
    """All of the kids would laugh as I walked up to the newspaper stand to buy a paper..."""
    perms = message.channel.permissions_for(ctx.me)
    if perms.manage_messages:
        with suppress(discord.NotFound):
            await message.remove_reaction(emoji, ctx.author)
    if page == 0:
        page = len(pages) - 1
    else:
        page -= 1
    return await menu(ctx, pages, controls, message, page, timeout)


async def close_menu(
    ctx: Context,
    pages: List[discord.Embed],
    message: discord.Message,
    page: int,
    timeout: float,
    emoji: str
):
    """Now I have built... the Paginator! When I fire it, every newspaper in the tristate area will be under my control!"""
    with suppress(discord.NotFound):
        await message.delete()
