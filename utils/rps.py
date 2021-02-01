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
import random
from typing import *

from discord import Embed as DEmbed
from discord.ext.commands import Context

from .embed import Embed

embeder = Embed()
rps = {
    "rock": ["Rock. We tied!", "Paper. I win!", "Scissors. You win!"],
    "paper": ["Rock. I win!", "Paper. We tied!", "Scissors. I win!"],
    "scissors": ["Rock. I win!", "Paper. You win!", "Scissors. We tied!"]
}

__all__ = ["rock_paper_scissors"]


def arg_parser(arg: str) -> Tuple[str, int]:
    """This will take an argument and return a full version

    Returns None if the argument doesn't match up to a choice"""
    if arg == "r":
        return "Rock", 0
    if arg == "p":
        return "Paper", 1
    if arg == "s":
        return "Scissors", 2
    return None, 0  # Return 0 to make sure that it doesn't complain when a bad argument is given


async def rock_paper_scissors(ctx: Context, choice: str) -> None:
    """Rock paper scissors, because life is meaningless"""
    choice, numb = arg_parser(choice[0].lower())
    if choice:
        bot_choice = random.choice(list(rps.keys()))
        game_outcome = rps[bot_choice][numb]
        embed: DEmbed = embeder.create(
            ctx, title="Rock Paper Scissors",
            description="Play Rock Paper Scissors!\nUse `>rps <choice>` to play!",
            footer="Twilight bot RPS", thumbnail=ctx.bot.user.avatar_url
        )
        embed.add_field(name="Bot's choice",
                        value=bot_choice.capitalize(), inline=True)
        embed.add_field(name="User's choice", value=choice, inline=True)
        embed.add_field(name="Outcome", value=game_outcome, inline=False)
        await ctx.send(embed=embed)
    else:
        await ctx.send("Bad argument! You can use `Rock, Paper, or Scissors`")
