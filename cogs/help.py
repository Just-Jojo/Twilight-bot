import discord
from discord.ext import commands


"""This custom help command is a perfect replacement for the default one on any Discord Bot written in Discord.py!
However, you must put "bot.remove_command('help')" in your bot, and the command must be in a cog for it to work.
Written by Jared Newsom (AKA Jared M.F.)!"""

class Help(commands.Cog, name="help"):
    """A helpful cog"""

    def __init__(self, client):
        self.client = client

    @commands.command(pass_context=True)
    async def help(self, ctx, *cog):
        """
        Lists all the commands and cogs in the bot

        This command will list the commands not bound to a cog and all the cogs if a cog is not specified. If a cog is specified though it will list all of the commands in that cog.
        [p]help [cog]
        *note that cog is optional
        """
        try:
            if not cog:
                """Cog listing.  What more?"""
                halp = discord.Embed(title='Cog Listing and Uncatergorized Commands',
                                     color=discord.Color.blue(),
                                     description='Use `help <cog>` to find out more about them!\n(BTW, the Cog Name Must Be in Title Case, Just Like this Sentence.)')
                cogs_desc = ''
                for x in self.client.cogs:
                    cogs_desc += ('{} - {}'.format(x,
                                                   self.client.cogs[x].__doc__)+'\n')
                halp.add_field(
                    name='Cogs', value=cogs_desc[0:len(cogs_desc)-1], inline=False)
                halp.set_footer(text="Help command written by Jared Newsom.")
                cmds_desc = ''
                for y in self.client.walk_commands():
                    if not y.cog_name and not y.hidden:
                        cmds_desc += ('{} - {}'.format(y.name, y.help)+'\n')
                halp.add_field(name='Uncatergorized Commands',
                               value=cmds_desc[0:len(cmds_desc)-1], inline=False)
                halp.set_author(name="Twilight Bot",
                                icon_url="https://cdn.discordapp.com/attachments/707431591051264121/734176068751196200/twlight_sparkle.png")
                await ctx.send(embed=halp)
            else:
                """Helps me remind you if you pass too many args."""
                if len(cog) > 1:
                    halp = discord.Embed(
                        title='Error!', description='That is way too many cogs!', color=discord.Color.red())
                    await ctx.send(embed=halp)
                else:
                    """Command listing within a cog."""
                    found = False
                    for x in self.client.cogs:
                        for y in cog:
                            if x == y:
                                halp = discord.Embed(
                                    title=cog[0]+' Command Listing', color=discord.Color.blue(), description=self.client.cogs[cog[0]].__doc__)
                                halp.set_footer(
                                    text="Help command written by Jared Newsom.")
                                for c in self.client.get_cog(y).get_commands():
                                    if not c.hidden:
                                        halp.add_field(
                                            name=c.name, value=c.help, inline=False)
                                found = True
                    if not found:
                        """Reminds you if that cog doesn't exist."""
                        halp.set_footer(
                            text="Help command written by Jared Newsom.")
                        halp = discord.Embed(
                            title='Error!', description='How do you even use "'+cog[0]+'"?', color=discord.Color.red())
                    else:
                        halp.set_author(name="Twilight Bot",
                                        icon_url="https://cdn.discordapp.com/attachments/707431591051264121/734176068751196200/twlight_sparkle.png")
                        await ctx.send(embed=halp)
        except:
            await ctx.send("Excuse me, I can't send embeds.")


def setup(client):
    client.add_cog(Help(client))
