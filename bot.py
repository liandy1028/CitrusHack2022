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
    if message.author == bot.user:
        return
    if message.channel.id in threads:
        await translate_message(message)
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
            thread = await ctx.message.create_thread(name=threadname, auto_archive_duration=60)
        except discord.errors.HTTPException:
            await ctx.channel.send('Unable to create thread')
            return

        threads[thread.id] = [lang, lang2]
        remove_threads()
          
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
    except ValueError:
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
    lang = lang.lower()
    if lang in googletrans.LANGUAGES:
        return googletrans.LANGUAGES[lang]
    elif lang in googletrans.LANGCODES:
        return lang
    elif lang in specialLang:
        return specialLang[lang]
    else:
        return None

def remove_threads():
    for thread in list(threads):
        if not bot.get_channel(thread):
            del threads[thread]
        elif bot.get_channel(thread).archived:
            del threads[thread]

async def translate_message(message):
    translator = Translator()
    src = googletrans.LANGUAGES[translator.detect(message.content).lang.lower()]
    if src == threads[message.channel.id][0]:
        dest = threads[message.channel.id][1]
    elif src == threads[message.channel.id][1]:
        dest = threads[message.channel.id][0]
    else:
        return
    translated = translator.translate(message.content, src=src, dest=dest).text
    await message.channel.send(translated)

try:
    with open('threads.json', 'r') as f:
        threads = json.load(f)

    bot.run(TOKEN)
finally:
    with open('threads.json', 'w') as f:
        f.write(json.dumps(threads, indent=4))