def bold(text):
  """Returns a string with boldened characters."""
  return "**{}**".format(text)
  
def italic(text):
  """Returns a string with italicized characters."""
  return "*{}*".format(text)
  
def strike(text):
  """Returns a string with striked characters."""
  return "~~{}~~".format(text)
  
def spoiler(text):
  """Returns a string with hidden characters."""
  return "||{}||".format(text)
  
def quote(text):
  """Returns a quoted string."""
  return ">>> {}".format(text)
  
def backtick(text):
  """Returns a string with backticks"""
  return "`{}`".format(text)
  
def box(text, lang):
  """Returns a string inside a code-block."""
  return "```{}\n{}\n```.format(lang, text)
  
def snake(text):
  """Returns a string with snake spaces."""
  return text.replace(' ', '_')
