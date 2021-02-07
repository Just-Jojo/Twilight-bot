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


def bold(text: str):
    """Returns a string with boldened characters."""
    return "**{}**".format(text)


def italic(text: str):
    """Returns a string with italicized characters."""
    return "*{}*".format(text)


def strike(text: str):
    """Returns a string with striked characters."""
    return "~~{}~~".format(text)


def spoiler(text: str):
    """Returns a string with hidden characters."""
    return "||{}||".format(text)


def quote(text: str):
    """Returns a quoted string."""
    return ">>> {}".format(text)


def backtick(text: str):
    """Returns a string with backticks"""
    return "`{}`".format(text)


def box(text: str, lang: str = ""):
    """Returns a string inside a code-block."""
    return "```{}\n{}\n```".format(lang, text)


def snake(text: str):
    """Returns a string with snake spaces."""
    return text.replace(" ", "_")


def reverse(text: str):
    """Returns a reversed string."""
    return text[::-1]
