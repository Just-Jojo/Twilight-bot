import random

from discord import Embed, Color


rps_word = ["r", "p", "s"]
rps = {
    "r": ["Rock. We tied!", "Paper. I win!", "Scissors. You win!"],
    "p": ["Rock. You win!", "Paper. We tied!", "Scissors. I win!"],
    "s": ["Rock. I win!", "Paper. You win!", "Scissors. We tied!"]
}
rps_arg = ["Rock", "Paper", "Scissors"]


def RockPaperScissors(arg: str = None):
    if arg != None:
        if arg.lower() in rps_word:
            rps_out = random.randint(0, 2)
            act = rps_arg[rps_out]
            act_2 = rps[arg][rps_out]
            x = Embed(
                title="Rock Paper Scissors",
                color=Color.teal(),
            )
            x.add_field(
                name="Your choice",
                value=arg
            )
            x.add_field(
                name="My choice",
                value=act
            )
            x.add_field(
                name="Outcome",
                value=act_2
            )

        else:
            x = Embed(
                title="Oops!", description="You need to supply a valid arugment!\nr, p, or s!", color=Color.red())

    else:
        x = Embed(
            title="Oops!", description="You need to supply a valid arugment!\nr, p, or s!", color=Color.red())

    return x
