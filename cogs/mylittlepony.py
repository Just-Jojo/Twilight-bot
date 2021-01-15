"""
MIT License

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
SOFTWARE.
"""
### ~~~ Basic Discord and other utils imports ~~~ ###
import discord
from discord.ext.commands import (
    Context, command, is_owner, Cog
)
from typing import *
### ~~~ Twilight utis imports ~~~ ###
from bot import Twilight  # Type hinting :D
from utils import Embed

MLP_LOGO = "https://cdn.discordapp.com/attachments/766499155669286922/779986290770182144/MLPFiM_logo.jpg"


class MyLittlePony(Cog):
    """The Main MLP cog"""

    def __init__(self, bot: Twilight):
        self.bot = bot

    def mlp_episode_description(
        self, ctx: Context, num: int,
        title: str, description: str, url: str = None
    ) -> discord.Embed:
        """Generate an episode Embed from the given variables"""
        description += "...\nRead more [here]({})".format(url)
        embed = Embed.create(
            ctx, title=title.format(
                num, title),
            description=description,
            thumbnail=MLP_LOGO, footer="Twilight Episode search",
            color=discord.Color.purple()
        )
        return embed

    def mlp_character_description(
        self, ctx: Context, character: str,
        description: str, url: str
    ) -> discord.Embed:
        """Generate a character Embed from the given variables"""
        embed = Embed.create(
            ctx, title=f"{character}'s Bio", description=description,
            image=url, footer="Twilight Character search", color=discord.Color.purple()
        )
        return embed

    @command()
    async def smile(self, ctx):
        """Smile song!"""
        title = "From My Little Pony: Friendship is Magic, Season 2, Episode 18, the Smile song!",
        description = (
            "Pinkie Pie loves to make ponies smile, so she had to sing about it."
            " This song is very upbeat and happy :D\n[Smile!](https://www.youtube.com/watch?v=lQKaAlMNvm8&ab_channel=MyLittlePonyOfficial)"
        )
        embed = Embed.create(ctx, title=title, description=description)
        await ctx.send(embed=embed)

    @command()
    async def episode(self, ctx: Context, episode: Optional[int]):
        """Episode search command"""
        await ctx.send("Whoops! We're rebuilding this command right now. Hang on tight!")

    @command()
    async def character(self, ctx: Context, *, name: Optional[str]):
        """Look for a character"""
        await ctx.send("Whoops! We're rebuilding this command right now. Hang on tight!")


def setup(bot: Twilight):
    bot.add_cog(MyLittlePony(bot))
