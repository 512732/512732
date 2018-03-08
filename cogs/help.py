import bs4
import asyncio
import random
import time
import aiohttp
import discord
import requests
from discord.ext import commands
import datetime


class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx):
        embed = discord.Embed(title="<:googlepenguin:359040809024225281> **Help has arrived!** ", colour=0xffffff, url="https://discord.gg/cpxdWTR", description="*All current working bot commands.*", timestamp=datetime.datetime.utcnow())

        embed.set_author(name="{}, Here is your help.".format(ctx.author.name), icon_url="{}".format(ctx.author.avatar_url))
        embed.set_footer(text="Snowy! ", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

        embed.add_field(name="🎵 __**Music Commands**__", value="**s.join -** Joins a specified voice channel. \n**s.summon -** Summons the bot in your voice channel. \n**s.quit -** Stops playing audio and leaves the voice channel. \n**s.stop -** Clears queue and leaves voice channel. \n**s.skip -** Skips current song. \n**s.volume -** Sets volume of current playing song \n**s.play -** Searches/plays a URL of a song. \n**s.playlist -** Adds tracks from a playlist to the queue. \n**s.playing -** Shows info about the currently playing song. \n**s.queue -** Shows the current queue. \n**s.shuffle -** Shuffles the current queue.")
        embed.add_field(name="🎉 __**Fun Commands**__", value="**s.ask  -  **Ask a question \n**s.avatar  -**  Get someones avatar \n**s.coinflip  -**  Flips a coin \n**s.dog  -** Shows random pic of 🐶 \n**s.hug  -** Hug someone or your-self...\n**s.invite  -** Invite for this bot 👍 \n**s.latency  -** Ping! \n**s.now  - 🕐** \n**s.poll  -** Creates a poll \n**s.servericon  -** Sends the icon of the server. \n**s.servers  -**  The amount of users/servers \n**s.urban  -** Searches the urban dictionary \n**s.yomomma  -** Heh good yomomma jokes.")
        embed.add_field(name="🛡 __**Admin Commands**__", value="**s.ban -** Bans a mentioned member of the server. \n**s.kick -** Kicks a mentioned member from the server. \n**s.softban -** Quickly, Bans and Unbans a member from the server.")
        embed.add_field(name="👌 *Sweet bot bro!* ", value="- Thanks this bot was made by **YetiGuy!#6280** you can invite it by [clicking here](https://discordapp.com/oauth2/authorize?client_id=368083703051845633&scope=bot&permissions=1610087679)", inline=False)
        embed.add_field(name="❓ Need more help?", value="[Click here!](https://discord.gg/cpxdWTR) this will take you to the bots offical server", inline=False)

        message = await ctx.send(embed=embed)
        await asyncio.sleep(120)
        await message.delete()

def setup(bot):
    bot.add_cog(Help(bot))
    print("Loaded the Help Bot")
