import discord

from discord.ext import commands

token = open("TOKEN.txt", "r").readline()

description = "Hi, I'm Millie! I help artists combat art theft."

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)

@bot.event
async def on_ready():
    print("Millie is ready for action!")

@bot.command()
async def info(ctx):
    """Provides the author with info about Millie."""
    info = discord.Embed(
        title="Hi, I'm Millie! I'm here to help artists combat art theft.",
        description="""
        As a digital artist, it can be incredibly frustrating when someone steals your work and tries to profit off of it.
        Thankfully, there's a law called the Digital Millenium Copyright Act (DMCA) that can help you get your stolen content removed.
        Many websites have __online forms__ for submitting your DMCA takedown notice.
        If such a form doesn't exist, you can __contact the site's DMCA agent directly__ or __reach out to the web host or ISP__.

        Type **!email** to learn more about DMCA takedown emails.
        Type **!forms** for help with DMCA forms for a particular site.
        """,
        color=0xe6c9ff
        )
    await ctx.send(embed=info)

bot.run(token)