import discord
from discord.ext import commands as com
from discord.ext.commands import Cog

import random

import wikipedia

twilight_image_links = [
    "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist",
    "https://i.pinimg.com/originals/5f/80/fc/5f80fc95aac0aa4448ccf954d198c3d1.png",
    "https://i.pinimg.com/originals/d5/08/a6/d508a6dae0f0e51bc9157e0d98885846.png",
    "https://upload.wikimedia.org/wikipedia/sco/thumb/5/5b/Twilight_sparkle.png/1200px-Twilight_sparkle.png"
]
with open("ponies.txt", "r") as pon:
     pon_list = pon.readlines()
     ponies = {
         "twilight": pon_list[0],
         "applejack": pon_list[1]
     }
 with open("ponyurl.txt", "r") as some:
     pon_list = some.readlines()
     pony_url = {
         "twilight": pon_list[0],
         "applejack": pon_list[1]
     }


def PonyReturner(arg):
    return ponies[arg], pony_url[arg]


class MyLittlePony(Cog, name="mylittlepony"):
    """Main MLP cog."""

    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_ready(self):
        print("MLP spells ready")

    @com.command(name="episode", hidden=True)
    async def episode_search(self, ctx, *args):
        pass

    @com.command(aliases=["mlp"], help="About the MLP: FIM show.")
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

    @com.command(name="quote", aliases=["twq", "twilight"], help="Get a random Twilight quote")
    async def twilight_quotes(self, ctx):
        x = []
        with open("twilightquote.txt", "r") as f:
            for line in f.readlines():
                x.append(line)
        embed = discord.Embed(color=discord.Color.purple(
        ), title="Twilight quote", description=x[random.randrange(0, len(x))])
        embed.set_thumbnail(
            url=twilight_image_links[random.randrange(
                0, len(twilight_image_links))]
        )
        embed.set_footer(
            text="~Twilight Sparkle"
        )
        await ctx.send(embed=embed)

    @com.command(hidden=True)
    async def pony(self, ctx, pony: str = None):
        if pony == None:
            pon_keys = "\n".join(ponies.keys())
            embed = discord.Embed(
                title="Ponies listing",
                description="Here are all the ponies I have TL:DR's on:\n\n{0}".format(
                    pon_keys),
                color=discord.Color.green()
            )

        else:
            if pony.lower() in ponies.keys():
                pon, pon_rl = PonyReturner(pony)
                embed = discord.Embed(
                    title="About {0}".format(pony),
                    color=discord.Color.teal(),
                    description=pon
                )
                embed.set_thumbnail(
                    url=pon_rl
                )

            else:
                embed = discord.Embed(
                    title="Oops!",
                    color=discord.Color.red(),
                    description="I could not find that pony!"
                )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(MyLittlePony(client))
