import json
import random

import discord
import requests
from discord import Color, Embed
from discord.ext import commands
from discord.ext.commands import Context

twilight_pfp = "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist"
twilight_image_links = [
    "https://vignette.wikia.nocookie.net/p__/images/c/c7/Twilight_Sparkle_Alicorn_vector.png/revision/latest?cb=20151125231105&path-prefix=protagonist",
    "https://i.pinimg.com/originals/5f/80/fc/5f80fc95aac0aa4448ccf954d198c3d1.png",
    "https://i.pinimg.com/originals/d5/08/a6/d508a6dae0f0e51bc9157e0d98885846.png",
    "https://upload.wikimedia.org/wikipedia/sco/thumb/5/5b/Twilight_sparkle.png/1200px-Twilight_sparkle.png"
]


class EmbedCreator:
    def __init__(self, client):
        self.client = client

    async def create(self, ctx, title="",
                     description="", color=Color.blue(),
                     footer=None, footer_image=None,
                     thumbnail=None, image=None):
        """
        Embed creator
        Make an discord Embed object with arguments

        context, title of the embed, description of the embed, color (defaults to blue), footer (optional), footer image (also optional), thumbnail, image
        """
        data = Embed(title=title, color=color)
        if description is not None:
            data.description = description
        data.set_author(name=ctx.author.display_name,
                        icon_url=ctx.author.avatar_url)

        if footer is None:
            footer = "Twilight Embed"
        if footer_image is None:
            footer_image = twilight_pfp
        data.set_footer(text=footer, icon_url=footer_image)

        if image is not None:
            data.set_image(url=image)

        if thumbnail is not None:
            data.set_thumbnail(
                url=thumbnail
            )
        return data


class BasicUtils:
    def __init__(self, client):
        self.client = client

    async def whisper(self, ctx: Context, user: discord.Member, message: str = '', embed: discord.Embed = None):
        if embed is not None:
            await user.send(message, embed=embed)
            return
        await user.send(message)

    async def json_dumper(self, json_file: str, content):
        with open("{0}.json".format(json_file), "a") as f:
            json.dump(f)

    async def help_returner(self, ctx: Context):
        await ctx.send_help(ctx.command)

    async def twilight_pic(self):
        return random.choice(twilight_image_links)

    async def rock_paper_scissors(self, ctx: Context, arg: str = None):
        rps_arguments = ["rock", "paper", "scissors"]
        rps_outcome = {
            "rock": ["We tied!", "I win!", "You win!"],
            "paper": ["You win!", "We tied!", "I win!"],
            "scissors": ["I win!", "You win!", "We tied!"]
        }
        if arg is not None:
            if arg.lower() in rps_arguments:
                _main = random.randint(0, 2)
                bot_choice = rps_arguments[_main]
                embed = await EmbedCreator.create(
                    self, ctx, title="Rock Paper Scissors",
                    description="Rock Paper Scissors game between {0} and Me!".format(
                        ctx.author),
                    footer="Twilight bot Rock Paper Scissors")
                embed.add_field(
                    name="Your choice", value=arg.lower(),
                    inline=True
                )
                embed.add_field(
                    name="My choice", value=bot_choice,
                    inline=True
                ),
                embed.add_field(
                    name="Outcome",
                    value=rps_outcome[arg.lower()][_main],
                    inline=False
                )
                await ctx.send(embed=embed)
            else:
                embed = await EmbedCreator.create(
                    self, ctx, title="Whoops!",
                    color=discord.Color.red(),
                    description="I'm sorry I didn't recognize that argument!\nThe arguments you can use are `Rock, Paper, and Scissors`!",
                    footer="Twilight Rock, Paper, Scissors"
                )
                await ctx.send(embed=embed)
        else:
            embed = await EmbedCreator.create(
                self, ctx, title="Whoops", color=discord.Color.red(),
                description="You didn't specify an argument!\nThe arguments you can use are `Rock, Paper, Scissors`",
                footer="Twilight Rock, Paper, Scissors")
            await ctx.send(embed=embed)
