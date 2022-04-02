import os
import discord
from discord.ext import commands
import googletrans
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("ONLINE")

@bot.command(name='help')
async def help(ctx):
    pass

@bot.command(name='start')
async def start(ctx):
    pass

@bot.command(name='translate')
async def translate(ctx):
    pass



bot.run(TOKEN)