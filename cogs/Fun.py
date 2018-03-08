import bs4
import asyncio
import random
import time
import aiohttp
import discord
import requests
from discord.ext import commands
import datetime
import json

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8ball"])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ask(self, ctx, *, question=None):
        '''Ask a question'''
        question = question.lower()

        if question.startswith("should"):
            responses = ("Yes", "No", "Definitely", "Sure", "Of course", "Maybe",
                         "Probably" "Definitely not", "No way", "Please don't",
                         "Go ahead!", "I mean, if you want to, sure", "Sure, but be careful",
                         "That's probably not a good idea")
        elif question.startswith("where"):
            fast_food_chains = ("McDonald's", "Wendy's", "Burger King", "A&W", "KFC", "Taco Bell")
            responses = ("Just over there", "In your closet", "Probably hiding from you",
                         f"At the nearest {random.choice(fast_food_chains)}",
                         "Right behind you", "At the store", "Just a few blocks away",
                         "Nowhere near here")
        elif question.startswith("when"):
            time_units = ("years", "months", "days", "hours", "minutes", "seconds")
            responses = ("In a few hours", "Sometime this month", "When pigs fly",
                         "Not anythime soon, that's for sure", "By the end of the week",
                         "Let's hope that never happens", "I am genuinely unsure",
                         "Soon", "No idea, but be sure to tell me when it does",
                         "In a dog's age", "I don't know, but hopefully it's in my lifetime",
                         f"In {random.randint(1, 101)} {random.choice(time_units)}")
        elif question.startswith("who"):
            html = await fetch(ctx.session, "https://www.randomlists.com/random-celebrities?a", timeout=15, return_type='text')
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all(class_="crux")
            celebrities = []
            for tag in tags:
                celebrities.append(tag.text)
            responses = celebrities
        elif question.startswith(("what movie should", "what film should")):
            html = await fetch(ctx.session, "https://www.randomlists.com/random-movies?a", timeout=15, return_type='text')
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all(class_="support")
            movies = []
            for tag in tags:
                movies.append(tag.text)
            responses = movies
        elif question.startswith(("what game should", "what video game should", "what videogame should")):
            html = await fetch(ctx.session, "https://www.randomlists.com/random-video-games?a", timeout=15, return_type='text')
            soup = BeautifulSoup(html, "html.parser")
            tags = soup.find_all(class_="support")
            games = []
            for tag in tags:
                games.append(tag.text)
            responses = games
        else:
            responses = ("Yes", "No", "Definitely", "Sure", "Of course", "Maybe",
                         "Probably", "Most likely", "Definitely not", "No way",
                         "I hope not", "Better be", "I don't think so")

        if question is None:
            embed = discord.Embed(description="You forgot to ask a question", color=0xffffff)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await message.delete()
        else:
            embed = discord.Embed(description="{}".format(random.choice(responses)), color=0xffffff)
            message = await ctx.send(embed=embed)
            await asyncio.sleep(15)
            await message.delete()

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def yomomma(self, ctx):
        resource = 'http://api.yomomma.info/'
        async with aiohttp.ClientSession() as session:
            async with session.get(resource) as data:
                data = await data.read()
                data = json.loads(data)
            joke = data['joke']
            if not joke.endswith('.'):
                joke += '.'
            embed = discord.Embed(color = 0xffffff, description = joke)
            embed.set_author(name = "Here is your yomommajoke.", icon_url = ctx.message.author.avatar_url)
            message = await ctx.send(embed = embed)
            await asyncio.sleep(15)
            await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(description="Thanks! Bot invite link here: [Click here](https://discordapp.com/oauth2/authorize?client_id=368083703051845633&scope=bot&permissions=1610087679)")
    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coinflip(self, ctx):
        '''Flips a coin'''
        responses = ["Heads", "Tails"]
        e = discord.Embed(description="{}".format(random.choice(responses)), color=0xffffff)
        message = await ctx.send(embed=e)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dog(self, ctx):
        api = "https://api.thedogapi.co.uk/v2/dog.php"
        async with aiohttp.ClientSession() as session:
            async with session.get(api) as r:
                if r.status == 200:
                    response = await r.json()
                    embed = discord.Embed(color = 0xffffff)
                    embed.set_author(name = "{} here is your random dog".format(ctx.message.author.name))
                    embed.set_image(url = response['data'][0]["url"])
                    message = await ctx.send(embed = embed)
                    await asyncio.sleep(15)
                    await message.delete()




    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def urban(self, ctx, *,msg: str):
        word = ' '.join(msg)
        api = "http://api.urbandictionary.com/v0/define"
        response = requests.get(api, params=[("term", word)]).json()

        if len(response["list"]) == 0: return await ctx.send("Could not find that word!")

        embed = discord.Embed(title = ":mag: Search Word", description = word, color = 0xffffff)
        embed.add_field(name = "Top definition:", value = response['list'][0]['definition'])
        embed.add_field(name = "Examples:", value = response['list'][0]["example"])
        embed.set_footer(text = "Tags: " + ', '.join(response['tags']))

        message = await ctx.send(embed = embed)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command(aliases=['inv'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx):
        embed = discord.Embed(color=0xffffff)
        embed.description = ":thumbsup: Here you go [Click here](https://discordapp.com/oauth2/authorize?client_id=368083703051845633&scope=bot&permissions=1610087679)"
        message = await ctx.send(embed=embed)
        await asyncio.sleep(60)
        await message.delete()

    @commands.command(aliases=['av'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def avatar(self, ctx, *, member: discord.Member = None):
        '''Gets someones pfp'''
        member = member or ctx.author
        av = member.avatar_url
        if ".gif" in av:
            av += "&f=.gif"
        em = discord.Embed(url=av, color=0xffffff)
        em.set_author(name=str(member), icon_url=av)
        em.set_image(url=av)
        message = await ctx.send(embed=em)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def poll(self, ctx, *, message :str):
        author = ctx.message.author
        embed = discord.Embed(color=0xffffff, timestamp=datetime.datetime.utcnow())
        embed.set_author(name="Poll", icon_url=ctx.author.avatar_url)
        embed.description = message
        embed.set_footer(text=ctx.author.name)
        x = await ctx.send(embed=embed)
        await x.add_reaction("👍")
        await x.add_reaction("\U0001f937")
        await x.add_reaction("👎")

    @commands.command(pass_context=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def servericon(self, ctx):
        av=discord.Embed(color=0xffffff, timestamp=datetime.datetime.utcnow())
        av.set_author(icon_url=ctx.guild.icon_url, name="{}".format(ctx.guild.name))
        av.set_image(url=ctx.guild.icon_url)
        message = await ctx.send(embed=av)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def hug(self, ctx, *, member : discord.Member=None):
        if member is None:
            message = await ctx.send("{} has been hugged! 🤗".format(ctx.message.author.mention))
            await asyncio.sleep(15)
            await message.delete()
        elif member.id == ctx.message.author.id:
            message = await ctx.send("{} hugged themselves because they are a loner 😐".format(ctx.message.author.mention))
            await asyncio.sleep(15)
            await message.delete()
        else:
            message = await ctx.send("{} was hugged by {} 😍".format(member.mention, ctx.message.author.mention))
            await asyncio.sleep(15)
            await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def now(self, ctx):
        date = datetime.datetime.now().strftime("**Date: **%A, %B %d, %Y\n**Time: **%I:%M %p")
        embed = discord.Embed(color=0xffffff)
        embed.add_field(name="Snowy's System Date & Time", value=date, inline=False)
        message = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command(no_pm = True, aliases = ['ping'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def latency(self, ctx):
        pingms = "{}".format(int(self.bot.latency * 1000))
        pings = "{}".format(int(self.bot.latency * 1))
        message = await ctx.send("Please wait 4")
        await message.edit(content = "Please wait 3")
        await asyncio.sleep(1)
        await message.edit(content = "Please wait 2")
        await asyncio.sleep(1)
        await message.edit(content = "Please wait 1")
        await asyncio.sleep(1)
        await message.edit(content = "Results: latency is **{}**s | **{}**ms".format(pings, pingms))
        await asyncio.sleep(15)
        await message.delete()

    @commands.command(pass_context=True, no_pm=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def servers(self, ctx):
        """The amount of users/servers"""
        users = len(set(self.bot.get_all_members()))
        servers = (len(self.bot.guilds))
        embed=discord.Embed(color=0xffffff)
        embed.add_field(name="Servers/Members", value="**I am currently in {} servers with {} users.**".format(servers, users))
        message = await ctx.send(embed=embed)
        await asyncio.sleep(15)
        await message.delete()




def setup(bot):
    bot.add_cog(Fun(bot))
    print("Loaded the Fun Bot")
