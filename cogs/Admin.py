import discord
from discord.ext import commands
from utils.paginator import Pages
import sys
import inspect
import os
import requests
import aiohttp
import asyncio
import json
import time
import re
import io
import os
import random

class Admin:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, target: discord.Member, reason=None):
        """Kicks a member from your server."""
        await target.kick(reason=reason)
        embed=discord.Embed(color=0xffffff)
        embed.add_field(name="Kicked a User", value="User {}".format(target.mention))
        message = ctx.send(embed=embed)
        await asyncio.sleep(15)
        await message.delete()



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, target: discord.Member, reason=None):
        """Ban a mentioned member from the server with the valid perms."""
        await target.ban(reason=reason)
        embed=discord.Embed(color=0xffffff)
        embed.add_field(name="Banned a User", value="User {}".format(target.mention))
        message = ctx.send(embed=embed)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command(aliases=['soft'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, target: discord.Member, reason=None):
        """Quickly, Bans and Undbans a member from the server."""
        await target.ban(reason=reason)
        await target.unban(reason=reason)
        embed=discord.Embed(color=0xffffff)
        embed.add_field(name="Softbanned a User", value="User {}".format(target.mention))
        message = ctx.send(embed=embed)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.is_owner()
    async def setavatar(self, ctx, link: str):
        """Sets the bot's avatar."""
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as r:
                if r.status == 200:
                    try:
                        await ctx.bot.user.edit(avatar=await r.read())
                    except Exception as e:
                        await ctx.send(e)
                    else:
                        await ctx.send('Avatar set.')
                else:
                    await ctx.send('Unable to download image.')



    @commands.command(aliases=['shutdown'])
    @commands.is_owner()
    async def _shutdown(self, ctx):
        '''Shutdown the bot'''
        reply = await ctx.send("Please react below for **shutdown** 📤, **restart** 🔃 or to *exit* ❌")
        await reply.add_reaction('📤')
        await reply.add_reaction('🔃')
        await reply.add_reaction('❌')

        def pred(reaction, user):
            return user == ctx.author and (str(reaction.emoji) == '📤' or str(reaction.emoji) == '🔃' or str(reaction.emoji) == '❌')

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=15.0, check=pred)
        except asyncio.TimeoutError:
                await reply.delete()
                message = await ctx.send(f"**Returning to online mode. Timed out!**")
                await asyncio.sleep(10)
                await message.delete()
        else:
            if str(reaction.emoji) == '📤':
                await reply.delete()
                message = await ctx.send(f"Shutting down...")
                await asyncio.sleep(10)
                await message.delete()
                os.system("pm2 stop Snowy")

            elif str(reaction.emoji) == '🔃':
                await reply.delete()
                message = await ctx.send("**I will switch my power off and on be right back** :wave:")
                await asyncio.sleep(10)
                await message.delete()
                os.system("pm2 restart Snowy")

            elif str(reaction.emoji) == '❌':
                await reply.delete()
                message = await ctx.send("**I have stopped the shutdown procedure.**")
                await asyncio.sleep(10)
                await message.delete()

def setup(bot):
    bot.add_cog(Admin(bot))
