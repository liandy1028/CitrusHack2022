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

#@bot.command(name='help')
#async def help(ctx):
#    pass

@bot.command(name='start', help='help me', brief='Starts a live translating thread.')
async def start(ctx):
    embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)
    pass

@bot.command(name='translate')
async def translate(ctx):
    pass

bot.run(TOKEN)