from discord.ext.commands import Cog


class BaseCog(Cog):
    """Base Cog Mixin

    This inherits from :class:`Cog` so passing that in won't matter

    Methods
    -------
    on_ready
        The actual reason I made this
        This will print that the cog is online when the bot is ready

        If overwriting is required for something, call super().on_ready()
    """

    @Cog.listener()
    async def on_ready(self):
        """A listener to print out that the Cog is ready"""
        print(f"{self.qualified_name} online")
