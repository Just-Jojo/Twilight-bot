import discord

def fraction(number: float):
  """
  Returns a fraction for the float specified.
  """
  n = number
  return(f"{(n).as_integer_ratio()[0]}/{(n).as_integer_ratio()[1]}")
  # Yes, kreusada did actually figure this one :D
