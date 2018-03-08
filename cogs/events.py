import discord
from discord.ext import commands

class events():
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, guild):
        print("I have joined {}!".format(guild))
        await guild.owner.send("Hey there! \nThanks for adding me. To use me, my prefix is `s.`, for cmds type `s.help` \n_**Make sure I have the correct permissions to work correctly**_\n• My owner is: YetiGuy!#6280")
        embed = discord.Embed(title="New Server: {}".format(guild), color = 0xffffff)
        embed.add_field(name = "Owner/ID", value ="{} + {}".format(guild.owner, guild.owner.id))
        embed.add_field(name = "Users", value = guild.member_count)
        embed.add_field(name = "ID:", value = guild.id)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon_url)
        if guild.me:
            embed.timestamp = guild.me.joined_at

        Nothing = self.bot.get_channel(394885560289853440)
        await Nothing.send(embed=embed)

    async def on_guild_remove(self, guild):
        print("I have left {}!".format(guild))
        await guild.owner.send("**I left the server**\nSorry if I did anything wrong. You can always add me back with this link: \nhttps://discordapp.com/oauth2/authorize?client_id=368083703051845633&scope=bot&permissions=1110682703")
        embed = discord.Embed(title="Left Server: {}".format(guild), color = 0xffffff)
        embed.add_field(name = "Owner/ID", value ="{} + {}".format(guild.owner, guild.owner.id))
        embed.add_field(name = "Users", value = guild.member_count)
        embed.add_field(name = "ID:", value = guild.id)
        if guild.icon:
            embed.set_thumbnail(url=guild.icon_url)


        Nothing = self.bot.get_channel(394885560289853440)
        await Nothing.send(embed=embed)


def setup(bot):
    bot.add_cog(events(bot))
