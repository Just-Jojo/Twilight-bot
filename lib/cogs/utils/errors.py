class TwilightException(Exception):
    """Base exception for all Twilight related things"""
    pass


class BadPages(TwilightException):
    """This is for the paginator so that I don't input a bad list of embeds lol"""
    pass
