import discord
from discord.ext.commands import (
    Context, command, is_owner, Cog
)
from .utils.embed import Embed


class MyLittlePony(Cog):
    """The Main MLP cog"""

    def __init__(self, bot):
        self.bot = bot

    @command()
    async def smile(self, ctx):
        title = "From My Little Pony: Friendship is Magic, Season 2, Episode 18, the Smile song!",
        description = (
            "Pinkie Pie loves to make ponies smile, so she had to sing about it."
            " This song is very upbeat and happy :D\n[Smile](https://www.youtube.com/watch?v=lQKaAlMNvm8&ab_channel=MyLittlePonyOfficial)"
        )
        embed = Embed.create(self, ctx, title=title, description=description)
        # embed.video(
        #     url="https://www.youtube.com/watch?v=lQKaAlMNvm8&ab_channel=MyLittlePonyOfficial"
        # )
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("mylittlepony")


def setup(bot):
    bot.add_cog(MyLittlePony(bot))
