import os
import discord
from discord.ext import commands
import googletrans
from dotenv import load_dotevn

load_dotevn()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.run(TOKEN)