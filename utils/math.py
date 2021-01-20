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
