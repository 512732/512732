import discord
from discord.ext import commands
import asyncio
import youtube_dl
import os
import sys
import traceback
import random
import aiohttp
import requests
import datetime
import time
import subprocess
import textwrap
from contextlib import redirect_stdout
import io
import json


with open("token.txt", 'r') as f:
    token = f.read().strip('\n')

def get_prefix(bot, message):
    prefixes = ['s.', 'S.']

    if not message.guild:
        return '?'

    return commands.when_mentioned_or(*prefixes)(bot, message)


initial_extensions = ['cogs.events', 'cogs.Music', 'cogs.ErrorHandler', 'cogs.insults', 'cogs.Fun', 'cogs.Admin', 'cogs.help']


bot = commands.Bot(command_prefix=get_prefix, description='New bot new snowy..')

bot.remove_command("help")



def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

@bot.event
async def on_ready():
    print("Username: {}".format(bot.user))
    print("ID: {}".format(bot.user.id))
    print("Guild Count: {}".format(len(bot.guilds)))
    print("User Count: {}".format(len(bot.users)))
    print("discord.py v{}".format(discord.__version__))
    Nothing = bot.get_channel(368086135244587024)
    while 1 == 1:
        servs = (len(bot.guilds))
        users = (len(set(bot.get_all_members())))
        chans = (len(set(bot.get_all_channels())))
        await bot.change_presence(game=discord.Game(type=3, name="the snow fall"))
        await asyncio.sleep(15.5)
        await bot.change_presence(game=discord.Game(name="Hello, {} users".format(users)))
        await asyncio.sleep(15.5)
        await bot.change_presence(game=discord.Game(type=2, name='your tunes!'))
        await asyncio.sleep(15.5)
        await bot.change_presence(game=discord.Game(name='Like the bot? Follow the creator', type=1, url='https://www.twitch.tv/yetiguyoffical'))
        await asyncio.sleep(15.5)
        await bot.change_presence(game=discord.Game(name="with {} channels".format(chans)))
        await asyncio.sleep(15.0)
        await bot.change_presence(game=discord.Game(name="in the snow"))
        await asyncio.sleep(15.5)
        await bot.change_presence(game=discord.Game(name="with {} servers".format(servs)))
        await asyncio.sleep(15.5)
        await bot.change_presence(game = discord.Game(name = "Online 24/7" ))


if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print('Failed to load extension {}.'.format(extension), file=sys.stderr)
            traceback.print_exc()

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def boobs(ctx):
    '''You know what this does'''
    if not ctx.channel.is_nsfw():
      await ctx.send("**This aint an NSFW channel**")
      return
    """Random"""
    api_base = 'http://api.oboobs.ru/boobs/'
    number = random.randint(1, 10303)
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.json()
            data = data[0]
    image_url = 'http://media.oboobs.ru/' + data['preview']
    em = discord.Embed(color=0xffffff)
    em.set_author(name="Random image")
    em.set_image(url=image_url)
    em.set_footer(text=f"Request {ctx.message.author.name}")
    await ctx.send(embed=em)

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ass(ctx):
    '''You know what this does'''
    if not ctx.channel.is_nsfw():
      await ctx.send("**This aint an NSFW channel**")
      return
    """Random butts!"""
    api_base = 'http://api.obutts.ru/butts/'
    number = random.randint(1, 4296)
    url_api = api_base + str(number)
    async with aiohttp.ClientSession() as session:
        async with session.get(url_api) as data:
            data = await data.json()
            data = data[0]
    image_url = 'http://media.obutts.ru/' + data['preview']
    em = discord.Embed(color=0xffffff)
    em.set_author(name="Random NSFW Image")
    em.set_image(url=image_url)
    em.set_footer(text=f"Request by {ctx.message.author.name}")
    await ctx.send(embed=em)



@bot.event
async def on_command_completion(ctx):
    await asyncio.sleep(5.0)
    try:
        await ctx.message.delete()
    except Exception as e:
        print(e)


@bot.command()
@commands.is_owner()
async def load(ctx, cogName: str = None):
    try:
        bot.load_extension(cogName.lower())
        await ctx.send("{} loaded.".format(cogName.lower()))
    except Exception as e:
        message = await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        await asyncio.sleep(15)
        await message.delete()

@bot.command()
@commands.is_owner()
async def unload(ctx, cogName: str = None):
    try:
        bot.unload_extension(cogName.lower())
        await ctx.send("{} unloaded.".format(cogName.lower()))
    except Exception as e:
        message = await ctx.send("```py\n{}: {}\n```".format(type(e).__name__, str(e)))
        await asyncio.sleep(15)
        await message.delete()

@bot.command()
@commands.is_owner()
async def leaveguild(ctx, guild):
    to_leave = discord.utils.get(bot.guilds, id=str(guild))
    try:
        await bot.leave_guild(to_leave)
    except:
        message = await ctx.send('Failed.')
        await asyncio.sleep(15)
        await message.delete()
    else:
        message = await ctx.send('Successfully left {}'.format(to_leave.name))
        await asyncio.sleep(15)
        await message.delete()

#@bot.command(pass_context=True, hidden=True)
#async def botleavep(ctx, serverid: str):
#    '''Leave server(BOT OWNER ONLY)
#    example:
#    -----------
#    :leaveserver 102817255661772800
#    '''
#    server = bot.get_server(serverid)
#    if server:
#        await bot.leave_server(server)
#        msg = ':door:  {} = Left server!'.format(server.name)
#    else:
#        msg1 = ':x: Could not find the ID of that server/Forgot to say ID of server!'
#       return await bot.say(msg1)
#    await bot.say(msg)


@bot.command()
@commands.is_owner()
async def blacklist(ctx, user_id: str = None):
    with open('cogs/blacklists.json') as f:
        data = json.loads(f.read())
        data = data[user_id] = "blacklisted"
        data = json.dumps(data, indent=4, sort_keys=True)
    with open('cogs/blacklists.json', 'w') as f:
        f.write(data)
        message = await ctx.send('Succesfully blacklisted id {}'.format(user_id))
        await asyncio.sleep(15)
        await message.delete()


@bot.command()
@commands.is_owner()
async def update(ctx):
    print('Running pull...')
    await ctx.send("Pulling...(Updating)", delete_after=5)
    subprocess.call(['git', 'pull'])
    os.system("cd /root/Snowy")
    os.system("git pull https://github.com/danymo1221/NotToBeUsedUnstableAsHell")
    print('Restarting now!')
    await ctx.send("Restarting now!", delete_after=5)
    os.system("pm2 restart Snowy")


@bot.command(hidden=True, name='eval')
@commands.is_owner()
async def _eval(ctx, *, body: str):
    '''Evaluate python code'''
    env = {
        'bot': bot,
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    try:
        exec(to_compile, env)
    except Exception as e:
        return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        try:
            await ctx.message.add_reaction('\u2705')
        except:
            pass

        if ret is None:
            if value:
                await ctx.send(f'```py\n{value}\n```')
        else:
            await ctx.send(f'```py\n{value}{ret}\n```')


bot.run(token)
