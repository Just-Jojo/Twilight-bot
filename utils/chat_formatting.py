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
  
def box(text: str, lang: str = ''):
  """Returns a string inside a code-block."""
  return "```{}\n{}\n```.format(lang, text)
  
def snake(text: str):
  """Returns a string with snake spaces."""
  return text.replace(' ', '_')

def reverse(text: str):
  """Returns a reversed string."""
  return text[::-1]
