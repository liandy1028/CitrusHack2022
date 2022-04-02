import os
import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
from dotenv import load_dotenv
from languageSupport import specialLang

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

@bot.command(aliases=['t','trans'])
async def translate(ctx, *args):
    translator = Translator()
    if len(args) < 2:
        await ctx.channel.send(f'Please provide a language to translate and the message you want to translate')
        return
    elif args[0] in googletrans.LANGUAGES or args[0] in googletrans.LANGCODES:
        lang = args[0]
    elif args[0] in specialLang:
        lang = specialLang[args[0]]
    else:
        await ctx.channel.send(f'The language `{args[0]}` is not supported.')
        return
    message = ' '.join(args[1:])
    try:
        if bot.get_message(int(message)):
            message = bot.get_message(int(message)).content
    except ValueError as e:
        pass
    translated =translator.translate(message, dest=lang).text
    await ctx.channel.send(translated)
        

bot.run(TOKEN)