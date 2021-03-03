import logging

import discord
from discord.ext import commands


class Cog(commands.Cog):
    """Base cog for Twilight's cogs.

    This mixin has an `on_ready` listener to alert that it is online
    """

    def __init__(self, *_args):
        bot: "Twilight"
        log: logging.Logger

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        try:
            self.log.info(f"{self.qualified_name} is now online")
        except NameError:
            raise RuntimeError(
                f"{self.qualified_name} does not have a logging method. Please add one."
            )
