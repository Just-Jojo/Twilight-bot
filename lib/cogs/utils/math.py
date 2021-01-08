import discord

def fraction(number: float):
  """
  Convert an integer/float to a fraction.
  """
  n = number
  return(f"{(n).as_integer_ratio()[0]}/{(n).as_integer_ratio()[1]}")

def decimal(fraction: str):
  """
  Convert a fraction to a decimal.
  Must be in the format `int/int`.
  """
  f = fraction
  l, r = f.split('/')
  if l.isdigit() and r.isdigit() and '/' in f:
    return(f"{float(l)/float(r)}")
  else:
    return("Invalid fraction")
