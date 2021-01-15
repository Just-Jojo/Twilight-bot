### ~~~ Base imports ~~~ ###
import discord
from discord.ext import commands
import json
from typing import *
### ~~~ Twilight imports ~~~ ###
from ..bot.bot import Twilight


def json_embed_parser(attachments: discord.message.Attachment):
    atc: discord.message.Attachment = attachments[0]
    if not atc.filename.endswith(".json"):
        return None
    embed = discord.Embed()
    try:
        return embed.from_dict()
    except Exception as e:
        return f"Failed for reason {e}"


class Embedder(commands.Cog):
    """A cog that allows a user to create and store an embed"""

    def __init__(self, bot: Twilight):
        self.bot = bot

    @commands.group()
    @commands.guild_only()
    async def embed(self, ctx: commands.Context):
        """Base embed command"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @embed.command()
    async def drop(self, ctx: commands.Context, channel: Optional[discord.TextChannel], embed: str):
        """Send an embed to a channel"""
        channel = channel or ctx.channel  # if the channel is None it will default to command's channel
        result = self._resolve_embed(ctx.guild, embed)
        if not result:
            await channel.send("I'm sorry I couldn't find that embed!")
            return
        await channel.send(embed=discord.Embed.from_dict(result))
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")

    def guild_setup(self, guild_id: int):
        """Set a guild's embeds up"""
        guilds = self._opener()
        guilds[str(guild_id)] = {}  # dict(dict(dict)) for guild embeds... yah
        self._write(guilds)

    def _write(self, writtable: dict):
        with open("./lib/cogs/embeds.json", "w") as embedder:
            json.dump(writtable, embedder, indent=4)

    def _opener(self):
        """Return the dict for guilds"""
        # Because writing this every time is **annoying**
        with open("./lib/cogs/embeds.json", "r") as embedder:
            return json.load(embedder)

    def _resolve_embed(self, guild: discord.Guild, embed_title: str) -> dict:
        embs = self._opener()
        try:
            return embs[guild.name][embed_title]  # Return the embed dict
        except KeyError:
            return None


def setup(bot: Twilight):
    bot.add_cog(Embedder(bot))
