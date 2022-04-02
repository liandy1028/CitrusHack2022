from asyncio.windows_events import NULL
from ctypes import sizeof
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
async def start(ctx, *args):
    isValid = False
    if len(args) == 3:
        lang = args[0]
        lang2 = args[1]
        threadname = args[2]
        isValid = True
    elif len(args) == 2:
        lang = args[0]
        lang2 = args[1]
        threadname = lang+" and "+lang2
        isValid = True
    else:
        pass

    if isValid is True:
        await ctx.channel.send("BEEP BOOP THREAD CREATED")
        await ctx.message.create_thread(name=threadname)

        while not ctx.message.locked:
            msg = await ctx.message.thread.wait_for('message')
            translate(lang2, msg)
        pass
    pass

@bot.command(
    aliases=['t','trans'], 
    help='Instantly translates any statement', 
    brief='Translates any short excerpt you wish to translate from one language to another!'
)
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