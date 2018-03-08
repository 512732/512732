import discord
from discord.ext import commands
import traceback
import sys
import asyncio

class ErrorHandler:
    def __init__(self, bot):
        self.bot = bot

    async def on_command_error(self, ctx, error):
            if isinstance (error, commands.CommandNotFound):
                embed = discord.Embed(title = "Woops - Not a command!", description = "**" + ctx.author.name + "**, Type: **s.cmds** to see my cmds.", color = 0xFFFFFF)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
                embed.add_field(name="Command Tried to Use: ", value = ctx.message.content)
                Nothing = self.bot.get_channel(394884440389713921)
                await Nothing.send(embed = embed)
                message = await ctx.send(embed = embed)
                await asyncio.sleep(15)
                await message.delete()

            elif isinstance(error, commands.BadArgument):
                embed = discord.Embed(title = "Error - Missing Something!",description = "**"+ ctx.author.name +"**, Try typing that again correctly", color = 0xFFFFFF)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
                embed.add_field(name="Command Tried to Use: ", value = ctx.message.content)
                message = await ctx.send(embed = embed)
                Nothing = self.bot.get_channel(394884440389713921)
                await Nothing.send(embed = embed)
                await asyncio.sleep(15)
                await message.delete()

            elif isinstance(error, commands.CommandOnCooldown):
                embed = discord.Embed(title = "Dont try to spam commands! :no_entry_sign:",description = "**"+ ctx.author.name +"**, Wait for the command to finish cooldown", color = 0xFFFFFF)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
                embed.add_field(name="Command Tried to Use: ", value = ctx.message.content)
                Nothing = self.bot.get_channel(394884440389713921)
                message = await ctx.send(embed = embed)
                await Nothing.send(embed = embed)
                await asyncio.sleep(15)
                await message.delete()

            elif isinstance (error, commands.MissingPermissions):
                embed = discord.Embed(title = "Denied! Your perms..",description = "**"+ ctx.author.name +"**, you're not allowed to do this!", color =  0xFFFFFF)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
                embed.add_field(name="Command Tried to Use: ",value = ctx.message.content)
                Nothing = self.bot.get_channel(394884440389713921)
                message = await ctx.send(embed = embed, delete_after=5)
                await Nothing.send(embed = embed)
                await asyncio.sleep(15)
                await message.delete()

            elif isinstance(error, commands.NotOwner):
                embed = discord.Embed(title = "Heh can't fool me! :no_entry_sign:",description = "**"+ ctx.author.name.mention +"**, Heh ", color = 0xFFFFFF)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
                Nothing = self.bot.get_channel(394884440389713921)
                message = await ctx.send(embed = embed)
                await Nothing.send(embed = embed)
                await asyncio.sleep(15)
                await message.delete()

            elif isinstance (error, commands.BotMissingPermissions):
                embed = discord.Embed(title = "Oh I don't have permissions for that. :warning::",description = "**"+ ctx.author.name.mention +"** Please check that I have the correct perms", color = 0xFFFFFF)
                embed.set_author(name=f"{ctx.author.display_name}", icon_url=f"{ctx.author.avatar_url}")
                Nothing = self.bot.get_channel(394884440389713921)
                message = await ctx.send(embed = embed)
                await Nothing.send(embed = embed)
                await asyncio.sleep(15)
                await message.delete()
            else:
                #  All other Errors not returned come here... And we can just print the default TraceBack.
                    print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
                    traceback.print_exception(type(error),error,error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
