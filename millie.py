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
    await ctx.send("Hi, I'm Millie! I help artists combat art theft.")

bot.run(token)