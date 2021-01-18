__all__ = ["fraction", "decimal"]
__version__ = "0.0.1"
__author__ = ["kreusada", ]


def fraction(number: float) -> str:
    """
    Convert an integer/float to a fraction.
    """
    n = number
    return(f"{(n).as_integer_ratio()[0]}/{(n).as_integer_ratio()[1]}")


def decimal(fraction: str) -> str:
    """
    Convert a fraction to a decimal.
    Must be in the format `int/int` or `float/float`.
    """
    f = fraction
    l, r = f.split('/')
    if l.isdigit() and r.isdigit() and '/' in f:
        return(f"{float(l)/float(r)}")
    else:
        return("Invalid fraction")
