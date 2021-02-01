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
__all__ = ["fraction", "decimal"]
__version__ = "0.0.1"
__author__ = ["kreusada", ]


def fraction(number: float) -> str:
    """Convert an integer/float to a fraction.

    Parameters
    ----------
    number: :class:`float`
        A floating point number to convert to a fraction

    Returns
    -------
    str
        The fractionized version of the decmial
    """
    n = number
    return(f"{(n).as_integer_ratio()[0]}/{(n).as_integer_ratio()[1]}")


def decimal(fraction: str) -> str:
    """Convert a fraction to a decimal.

    Must be in the format `int/int` or `float/float`.

    Parameters
    ----------
    fraction: :class:`str`
        The fraction to convert into a decimal

    Raises
    ------
    TypeError
        If the type isn't int/int or float/float
    """
    f = fraction
    l, r = f.split('/')
    if l.isdigit() and r.isdigit() and '/' in f:
        return(f"{float(l)/float(r)}")
    else:
        raise TypeError("Must be type `int/int` or `float/float`")
