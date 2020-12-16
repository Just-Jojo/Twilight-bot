# Why do I do this to myself?
from .embed import Embed
from discord import Embed as DEmbed
from discord.ext.commands import (Context,)
import random
from typing import *

embeder = Embed()
rps = {
    "rock": ["Rock. We tied!", "Paper. I win!", "Scissors. You win!"],
    "paper": ["Rock. I win!", "Paper. We tied!", "Scissors. I win!"],
    "scissors": ["Rock. I win!", "Paper. You win!", "Scissors. We tied!"]
}


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
