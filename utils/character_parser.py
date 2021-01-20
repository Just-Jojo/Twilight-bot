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

import re
import wikia
import discord
import aiohttp
from twi_secrets import MLP_FIM_LOGO

__all__ = ["char_embed", ]
__version__ = "0.0.1"
__author__ = ["Jojo#7791", ]


def parse_numbers(string: str) -> str:
    r"""Parse a decimal

    eg. 'Something important 1 Not needed info 1.1 sub not needed' -> 'Something important'

    Parameters
    ----------
    string: :class:`str`
        String to parse through.
        Note this will return the base string if it doesn't find any decimals

    Returns
    -------
    :class:`str`
        The parsed out string
    """
    pattern = re.compile(r"\s\d")
    match = pattern.search(string)
    if match is not None:
        string = string.split(match[0])[0]
    return string


def char_embed(character: str, image_url: str = None) -> discord.Embed:
    """Create a character embed based on the character

    Parameters
    ----------
    character: :class:`str`
        A MLP:FiM character to search for.
        Note: the character can have whitespaces as it will replace them with underscores
    image_url: :class:`Optional[str]`
        The image url used for the embed
        Defaults to the MLP:FiM logo

    Raises
    ------
    wikia.WikiaError
        This will happen if the character is not found

    Returns
    -------
    :class:`discord.Embed`
        The actual Embed with text and image
    """
    data = discord.Embed(title=character)
    try:
        page = wikia.WikiaPage("mlp", character.replace(" ", "_"))
    except wikia.WikiaError as e:
        raise e
    content = page.summary.split(".")
    for i in range(0, 1):
        content.pop(i)
    content = ". ".join(content)
    pattern = re.compile(r"^note")
    matches = pattern.finditer(content)
    for match in matches:
        content = "".join(content.split(match))
    content = parse_numbers(content)
    if content.endswith((".", "?", "!")):
        description = content[:-1] + \
            f"... For more, read the [wiki page]({page.url.replace(' ', '_')})"
    else:
        description = content + \
            f"... For more, see [the wiki page]({page.url.replace(' ', '_')}) for {character}"
    data.description = description
    data.colour = discord.Colour.purple()  # Because Twilight
    data.set_footer(text="Built using Wikia api for Python",
                    icon_url="https://cdn.discordapp.com/attachments/707431591051264121/800802724823695390/iconfinder_Asset_27_6467920.png")
    if image_url:
        data.set_thumbnail(url=image_url)
    else:
        data.set_thumbnail(url=MLP_FIM_LOGO)
    return data
