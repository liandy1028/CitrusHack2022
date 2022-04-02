import os
import discord
from discord.ext import commands
from googletrans import Translator
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("ONLINE")

@bot.command(name='start', help='help me', brief='Starts a live translating thread.')
async def start(ctx):
    embed=discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/", description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)
    await ctx.message.create_thread(name="TRNASLATE")
    pass

@bot.command()
async def translate(ctx, lang, *args):
    translator = Translator()
    message = ' '.join(args)
    translated =translator.translate(message, dest=lang).text
    await ctx.channel.send(translated)

bot.run(TOKEN)