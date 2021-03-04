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

# This is a complex-simple Rock Paper Scissors game built for Discord
# I might make this into a package later because it's awesome as heck lol

import discord
import random
import typing

GAME_PIECES = {
    "Rock": ["Rock. We tied!", "Paper. I win!", "Scissors. You win!"],
    "Paper": ["Rock. You win!", "Paper. We tied!", "Scissors. I win!"],
    "Scissors": ["Rock. I win!", "Paper. You win!", "Scissors. We tied!"],
}

GAME_KEYS = {
    "r": "Rock",
    "p": "Paper",
    "s": "Scissors",
}


# Parser parses if an argument is capable of being used for RPS
# if it doesn't it will return an error string (not really an `error` but a little `I couldn't understand that!`)
def parser(arg: str) -> str:
    """Parse a string and return the proper argument"""
    arg = arg[0].lower()
    return GAME_KEYS.get(arg, "null")


def rps_game(
    arg: str, extra_info: bool = False
) -> typing.Union[str, typing.Tuple[str, str, str]]:
    """Main RPS game"""
    # Remove the whitespace at the beginning and end
    arg = arg.strip()
    maybe_piece = parser(arg)
    # If the argument was invalid ask the user if they want to play again
    if maybe_piece == "null":
        return "Hm, I didn't understand that. Try again, perhaps?"
    else:
        # Now we get the computer's choice
        bot_choice = random.randint(0, 2)
        # Since the game pieces have the result return that
        result = GAME_PIECES[maybe_piece][bot_choice]
        if extra_info:
            return result, list(GAME_KEYS.values())[bot_choice], maybe_piece
        return result
