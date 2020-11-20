import re
from discord.ext.commands.converter import Converter
from discord.ext.commands import BadArgument

_id_regex = re.compile(r"([0-9]{15,21})$")
_mention_regex = re.compile(r"<@!?([0-9]{15,21})>$")


class RawUserIds(Converter):
    async def convert(self, ctx, argument):
        if match := _id_regex.match(argument) or _mention_regex(argument):
            return int(match.group(1))

        raise BadArgument("That doesn't look like a valid ID")
