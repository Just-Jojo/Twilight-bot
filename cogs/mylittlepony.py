import json
import random

import discord
import wikipedia
from discord.ext import commands
from discord.ext.commands import Cog

twilight_image_links = [
    "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist",
    "https://i.pinimg.com/originals/5f/80/fc/5f80fc95aac0aa4448ccf954d198c3d1.png",
    "https://i.pinimg.com/originals/d5/08/a6/d508a6dae0f0e51bc9157e0d98885846.png",
    "https://upload.wikimedia.org/wikipedia/sco/thumb/5/5b/Twilight_sparkle.png/1200px-Twilight_sparkle.png"
]
with open("pony.json", "r") as f:
    pony = json.load(f)
pony_keys = ", ".join([key for key, _ in pony.items()])


def pony_returner(arg):
    return pony[arg.lower()][0], pony[arg.lower()][1]


class MyLittlePony(Cog, name="mylittlepony"):
    """Main MLP cog."""

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["mlp"], help="About the MLP: FIM show.")
    async def mylittlepony(self, ctx):
        with open("mlp.txt", "r") as f:
            mlp = f.read()
        embed = discord.Embed(color=discord.Color.purple(
        ), description=mlp, title="About My Little Pony: Friendship is Magic")
        embed.set_footer(
            icon_url="https://upload.wikimedia.org/wikipedia/en/thumb/0/0d/My_Little_Pony_Friendship_Is_Magic_logo_-_2017.svg/1200px-My_Little_Pony_Friendship_Is_Magic_logo_-_2017.svg.png",
            text="My Little Pony: Friendship is Magic."
        )
        embed.set_thumbnail(
            url="https://img1.hulu.com/user/v3/artwork/3790ca9f-1a6b-4130-b0b3-e3fc0fe5a5f8?base_image_bucket_name=image_manager&base_image=0fe67d3e-8087-45eb-8e34-188c485d7999&size=400x600&format=jpeg"
        )
        await ctx.send(embed=embed)

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
        embed = discord.Embed(color=discord.Color.purple(
        ), title="Twilight quote", description=random.choice(quotes))
        embed.set_thumbnail(
            url=random.choice(twilight_image_links)
        )
        embed.set_footer(
            text="~Twilight Sparkle"
        )
        await ctx.send(embed=embed)

    @commands.command(help="Get TL:DR's on your favorite ponies!")
    async def pony(self, ctx, pony: str = None):
        if pony != None:
            try:
                name, link = pony_returner(pony.lower())
                embed = discord.Embed(
                    title="Information about {0}".format(pony.lower()),
                    color=discord.Color.blue(),
                    description=name
                )
                embed.set_thumbnail(
                    url=link
                )
                embed.set_footer(text="Twilight's pony TL:DR's")
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(
                    title="Oops!",
                    color=discord.Color.red(),
                    description="Here are all the ponies I have in my database!\n{0}".format(
                        pony_keys)
                )
                embed.set_footer(text="Error!")
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="Ponies!",
                color=discord.Color.light_grey(),
                description="Here are all the ponies I have in my database!\n{0}".format(
                    pony_keys)
            )
            embed.set_footer(text="More ponies!")
            await ctx.send(embed=embed)

    @commands.command(help="Smile song!")
    async def smile(self, ctx):
        await ctx.send("https://www.youtube.com/watch?v=lQKaAlMNvm8")

    @commands.command(name="equestriagirls", aliases=["eg"], help="Equestria Girls")
    async def equestria_girls(self, ctx):
        await ctx.send("Equestria Girls is a weird spin-off collection that Hasbro made for ***some reason***\nIt is basically normal My Little Pony except for the fact that everyone is human, and Twilight has glasses. It exists only to haunt me and Jojo")

    @commands.command(hidden=True, name="episodesearch", aliases=["eps"])
    async def _episode_search(self, ctx, *, episode_num: int = None):
        await ctx.send("Working")


def setup(client):
    client.add_cog(MyLittlePony(client))
