from discord.ext.commands import Cog


class BaseCog(Cog):
    """Base Cog Mixin to remind me to have `on_ready()`"""

    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        """A listener to print out that the Cog is ready"""
        print(f"{self.qualified_name} online")
