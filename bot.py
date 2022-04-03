from ast import alias
import os
import discord
from discord.ext import commands
import googletrans
from googletrans import Translator
from dotenv import load_dotenv
from languageSupport import specialLang
from proverbs import proverbs
from random import randrange
import json

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="!help"))
    print("ONLINE")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

@bot.command(
    alias=['s'],
    name='start', 
    help='Creates a thread wherein the 2 languages are translated to each other!', 
    brief='Starts a live translating thread.'
)
async def start(ctx, *args):
    if len(args) >= 2:
        if not (lang := setLang(args[0])):
            await ctx.channel.send(f'The language `{args[0]}` is not supported.')
            return
        if not (lang2 := setLang(args[1])):
            await ctx.channel.send(f'The language `{args[1]}` is not supported.')
            return
        if len(args) >= 3:
            threadname = ' '.join(args[2:])
        else:
            threadname = f'{lang} and {lang2}'
        isValid = True
    else:
        isValid = False

    if isValid is True:
        try:
            thread = await ctx.message.create_thread(name=threadname)
        except discord.errors.HTTPException:
            await ctx.channel.send('Unable to create thread')
            return
        
        with open('threads.json', 'r') as f:
            threads = json.load(f)
        threads[thread.id] = [lang, lang2]
        with open('threads.json', 'w') as f:
            f.write(json.dumps(threads, indent=4))
        # await bot.remove_threads()
          
@bot.command(
    aliases=['t','trans'], 
    help='Translates any short excerpt you wish to translate from one language to another!', 
    brief='Instantly translates any statement.'
)
async def translate(ctx, *args):
    translator = Translator()
    if len(args) < 2:
        await ctx.channel.send(f'Please provide a language to translate and the message you want to translate')
        return
    elif lang := setLang(args[0]):
        pass
    else:
        await ctx.channel.send(f'The language `{args[0]}` is not supported.')
        return
    message = ' '.join(args[1:])
    try:
        if bot.get_message(int(message)):
            message = bot.get_message(int(message)).content
    except ValueError as e:
        pass
    translated = translator.translate(message, dest=lang).text
    await ctx.channel.send(translated)

@bot.command(
    aliases=['q'],
    name = 'quotes',
    help = 'Use this command to display a random quote, courtesy of https://thecultureur.com/around-the-world-in-52-proverbs/',
    brief = 'Witness the glory and culture of 52 regions!'
)
async def quotes(ctx):
    await ctx.channel.send(proverbs[str(randrange(52)+1)])
        
def setLang(lang):
    if lang in googletrans.LANGUAGES or lang in googletrans.LANGCODES:
        return lang
    elif lang in specialLang:
        return specialLang[lang]
    else:
        return None

bot.run(TOKEN)