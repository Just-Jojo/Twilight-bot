def bold(text: str):
    """Return bolded text"""
    return f"**{text}**"


def box(text: str, lang=""):
    """Return text in a markdown block"""
    return f"```{lang}\n{text}```"


def tick(text: str):
    """Add '`' to text"""
    return f"`{text}`"


def italicize(text):
    """Return italicized text"""
    return f"*{text}*"


def spoiler(text):
    """Return text in a spoiler"""
    return f"||{text}||"
