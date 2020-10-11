import json
import random

import discord
import wikipedia
from discord.ext import commands
from discord.ext.commands import Cog
from twilight_tools import EmbedCreator, BasicUtils


with open("pony.json", "r") as f:
    pony = json.load(f)
pony_keys = ", ".join([key for key, _ in pony.items()])
# Test


class MyLittlePony(Cog):
    """Main MLP cog."""

    def __init__(self, client):
        self.client = client
        self.EmbedCreator = EmbedCreator(self)
        self.BasicUtils = BasicUtils(self)

    async def pony_returner(self, arg):
        return pony[arg.lower()][0], pony[arg.lower()][1]

    @commands.command(name="quote", aliases=["twq", "twilight"], help="Get a random Twilight quote")
    async def twilight_quotes(self, ctx):
        quotes = [
            "All the ponies in this town are crazy! Do you know what time it is?!",
            "You see, Nightmare Moon, when those Elements are ignited by the... the spark, that resides in the heart of us all, it creates the sixth element: the element of... magic!",
            "Hee-hee! Isn't this exciting? We'll do everything by the book, and that will make my slumber party officially fun.",
            "Everypony everywhere has a special magical connection with her friends, maybe even before she's met them. If you're feeling lonely and you're still searching for your true friends, just look up in the sky. Who knows, maybe you and your future best friends are all looking at the same rainbow.",
            "Move! Look out, here comes Tom!",
            "Clock is ticking, Twilight. Clock. Is. Ticking. Keep it together. If I can't find a friendship problem... I'll make a friendship problem!",
            "Gee, maybe her name should be Princess Demandy-pants.",
            "Huh? I'm pancake...I mean awake!",
            "Soup spoon, salad fork, pasta spoon, strawberry pick, I'm beginning to think that after friendship, the greatest magic of all is proper silverware placement!",
            "As the Princess of Friendship, I try to set an example for all of Equestria. But today, it was Spike who taught me that a new friend can come from anywhere. I guess everypony still has things to learn about friendship. Even me! And if Spike says Thorax is his friend, then he's my friend too."
        ]
        embed = await self.EmbedCreator.create(ctx, color=discord.Color.purple(
        ), title="Twilight quote", description=random.choice(quotes),
            thumbnail=await self.BasicUtils.twilight_pic(),
            footer="~ Twilight Sparkle")
        await ctx.send(embed=embed)

    # @commands.command(help="Get TL:DR's on your favorite ponies!")
    # async def pony(self, ctx, pony: str = None):
    #     if pony != None:
    #         try:
    #             name, link = await self.pony_returner(pony.lower())
    #             embed = await self.EmbedCreator.create(
    #                 ctx,
    #                 title="Information about {0}".format(pony.lower()),
    #                 color=discord.Color.blue(),
    #                 description=name,
    #                 thumbnail=link,
    #                 footer="Twilight's pony TL:DR's"
    #             )
    #             await ctx.send(embed=embed)
    #         except:
    #             embed = await self.EmbedCreator.create(
    #                 ctx,
    #                 title="Oops!",
    #                 color=discord.Color.red(),
    #                 description="Here are all the ponies I have in my database!\n{0}".format(
    #                     pony_keys),
    #                 footer="Error!"
    #             )
    #             await ctx.send(embed=embed)
    #     else:
    #         embed = await self.EmbedCreator.create(
    #             ctx,
    #             title="Ponies!",
    #             description="Here are all the ponies I have in my database!\n{0}".format(
    #                 pony_keys),
    #             footer="More ponies!"
    #         )
    #         await ctx.send(embed=embed)

    @commands.command(help="Smile song!")
    async def smile(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=lQKaAlMNvm8")

    @commands.command(hidden=True, name="episode", aliases=["eps"])
    @commands.is_owner()
    async def _episode_search(self, ctx, *, episode_num: str = None):
        with open("episodes.json", "r") as f:
            episodes = json.load(f)
        ep_list = len(episodes.keys())
        if episode_num is not None:
            try:
                embed = await self.EmbedCreator.create(
                    ctx,
                    title="My Little Pony: Friendship is Magic episode {0}".format(
                        episodes[episode_num][0]),
                    description=episodes[episode_num][1],
                    footer="Twilight bot episode search"
                )
                await ctx.send(embed=embed)
            except IndexError or KeyError:
                await ctx.send(ep_list)
        else:
            await ctx.send("I have {0} episodes in my database right now".format(ep_list))


def setup(client):
    client.add_cog(MyLittlePony(client))
