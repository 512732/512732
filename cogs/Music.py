import math
import discord
import audioop
import asyncio
import random
import datetime
import functools
import youtube_dl

from discord.ext import commands
from musicutils import paginator
from musicutils.paginator import Pages
from musicutils import time
from concurrent.futures import ThreadPoolExecutor

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')

class YoutubeEntry:
    def __init__(self, **kwargs):
        self.url = kwargs.get('webpage_url')
        self.download_url = kwargs.get('url')
        self.views = kwargs.get('view_count')
        self.is_live = bool(kwargs.get('is_live'))
        self.likes = kwargs.get('likes')
        self.dislikes = kwargs.get('dislikes')
        self.duration = kwargs.get('duration', 0)
        self.uploader = kwargs.get('uploader')
        self.id = kwargs.get('id')
        if 'twitch' in self.url:
            self.title = kwargs.get('description')
            self.description = None
        else:
            self.title = kwargs.get('title')
            self.description = kwargs.get('description')


class YoutubeSource(discord.FFmpegPCMAudio):
    def __init__(self, message, query):
        self.message = message
        self.query = query
        self.requester = message.author
        self.channel = message.channel
        self.frames = 0
        self.volume = 1.0
        self.opts = {
            'format': 'webm[abr>0]/bestaudio/best',
            'default_search': 'auto',
            'prefer_ffmpeg': True,
            'quiet': True
        }
        self.ytdl = youtube_dl.YoutubeDL(self.opts)
        self.entry = self.get_info()

    def start(self):
        self.entry = self.get_info()
        members = len(self.message.guild.voice_client.channel.members)
        self.required_skips = math.ceil(members/3)
        self.skip_votes = set()
        super().__init__(self.entry.download_url, before_options="-reconnect 1")

    def get_info(self):
        info = self.ytdl.extract_info(self.query, download=False)
        if 'entries' in info:
            info = info['entries'][0]

        entry = YoutubeEntry(**info)
        return entry

    def read(self):
        self.frames += 1
        return audioop.mul(super().read(), 2, self.volume)

    @property
    def length(self):
        return self.entry.duration

    @property
    def progress(self):
        return round(self.frames/50)

    @property
    def remaining(self):
        length = self.length
        progress = self.progress
        return length - progress

    def embed(self):
        embed = discord.Embed(color = 0xffffff)
        embed.title = 'Enqueued {}'.format(self.entry.title)
        embed.url = self.entry.url
        embed.add_field(name='Duration', value=time.human_time(self.entry.duration))
        if self.progress:
            embed.title = 'Currently playing {}'.format(self.entry.title)
            embed.add_field(name='Progress', value=time.human_time(self.progress))
            embed.add_field(name='Requester', value=self.requester, inline=False)
            embed.add_field(name='Skips', value='{}/{}'.format(len(self.skip_votes), self.required_skips))

        return embed

class VoiceQueue:
    def __init__(self, bot, guild):
        self.bot = bot
        self.guild = guild
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            source = await self.songs.get()
            source.start()
            embed = source.embed()
            embed.title = 'Now playing {}'.format(source.entry.title)
            embed.add_field(name='Requester', value=source.requester, inline=False)
            await source.channel.send(embed=embed)
            self.guild.voice_client.play(source, after=lambda x: self.play_next_song.set())
            await self.play_next_song.wait()

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.queues = {}
        self.opts = {
            'quiet': True,
            'ignoreerrors': False
        }
        self.ytdl = youtube_dl.YoutubeDL(self.opts)
        self._ytdl = youtube_dl.YoutubeDL(self.opts)
        self._ytdl.params['ignoreerrors'] = False
        self.executor = ThreadPoolExecutor(max_workers=2)

    def get_queue(self, guild):
        queue = self.queues.get(guild.id)

        if queue is None:
            queue = VoiceQueue(self.bot, guild)
            self.queues[guild.id] = queue

        return queue

    def __unload(self):
        for queue in self.queues.values():
            try:
                queue.audio_player.cancel()
                self.bot.loop.create_task(queue.guild.voice_client.disconnect())
            except:
                pass

    async def on_voice_state_update(self, member, before, after):
        vc = member.guild.voice_client
        if vc is None:
            return

        if not vc.is_playing() and not vc.is_paused():
            return

        channel = vc.channel
        before_channel = before.channel
        after_channel = after.channel

        if channel != before_channel and channel != after_channel:
            return

        members = len(channel.members) - 1

        if members == 0:
            vc.pause()
        else:
            vc.resume()

        vc.source.required_skips = math.ceil(members / 3)

    @commands.command(name='join')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def _join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel."""
        if ctx.author.voice is None:
            return await ctx.send('You need to be in a voice channel.')
        vc = ctx.guild.voice_client
        if vc is not None:
            return await ctx.send('Already in a voice channel.')

        await channel.connect()
        message = await ctx.send('Connected to {}.'.format(channel.name))
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def summon(self, ctx):
        """Summons the bot to join your voice channel."""
        voice = ctx.author.voice
        if voice is None:
            message = await ctx.send('You are not in a voice channel.')
            await asyncio.sleep(15)
            await message.delete(15)
            return

        vc = ctx.guild.voice_client
        if vc is not None:
            await vc.move_to(voice.channel)
        else:
            return await voice.channel.connect()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def quit(self, ctx):
        """Stops playing audio and leaves the voice channel."""
        await vc.disconnect()
        message = await ctx.send('Disconnected.')
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def stop(self, ctx):
        """Stops playing audio and leaves the voice channel.
        This also clears the queue.
        """
        vc = ctx.guild.voice_client
        voice = ctx.author.voice

        if voice:
            if vc is None:
                return await ctx.send('Not in a voice channel.')

        queue = self.get_queue(ctx.guild)
        queue.audio_player.cancel()
        del self.queues[ctx.guild.id]

        await vc.disconnect()
        message = await ctx.send('Disconnected.')
        await asyncio.sleep(15)
        await message.delete()



    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def skip(self, ctx):
        """Vote to skip a song. The song requester can automatically skip.

        Approximately 1/3 of the members in the voice channel
        are required to vote to skip for the song to be skipped.
        """
        if ctx.author.voice is None:
            return await ctx.send('You need to be in a voice channel.')
        vc = ctx.guild.voice_client
        if vc is None:
            return await ctx.send('Not in a voice channel.')

        if not vc.is_playing() and not vc.is_paused():
            return await ctx.send('Not currently playing anything.')

        voter = ctx.author
        if voter == vc.source.requester:
            message = await ctx.send('Requester requested skipping song...')
            vc.stop()
            await asyncio.sleep(15)
            await message.delete()
        elif voter not in vc.source.skip_votes:
            vc.source.skip_votes.add(voter.id)
            votes = len(vc.source.skip_votes)

            if votes >= vc.source.required_skips:
                message = await ctx.send('Skip vote passed, skipping song...')
                vc.stop()
                await asyncio.sleep(15)
                await message.delete()
            else:
                message = await ctx.send('Skip vote added, currently at [}/{}]'.format(votes, vc.source.required_skips))
                await asyncio.sleep(15)
                await message.delete()
        else:
            message = await ctx.send('You have already voted to skip this song.')
            await asyncio.sleep(15)
            await message.delete()


    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def volume(self, ctx, value: int = None):
        """Sets the volume of the currently playing song."""
        vc = ctx.guild.voice_client
        if vc.is_playing() or vc.is_paused():
            if value is not None and checks.role_or_permissions(ctx, lambda r: r.name == 'Admin', manage_guild=True):
                vc.source.volume = min(value / 100, 2.0)
                return await ctx.send('Set the volume to {}.'.format(vc.source.volume))
            message = await ctx.send('Volume is set to {}.'.format(vc.source.volume))
            await asyncio.sleep(15)
            await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, query: str):
        """Plays a song.

        If there is a song currently in the queue, then it is
        queued until the next song is done playing.

        This command automatically searches as well from YouTube.
        The list of supported sites can be found here:
        https://rg3.github.io/youtube-dl/supportedsites.html
        """
        if ctx.author.voice is None:
            return await ctx.send('You need to be in a voice channel.')
        vc = ctx.guild.voice_client
        if vc is None:
            vc = await ctx.invoke(self.summon)
            if vc is None:
                return

        source = YoutubeSource(ctx.message, query)
        embed = source.embed()
        queue = self.get_queue(ctx.guild)
        if not vc.is_playing() and not vc.is_paused():
            time_until = 'Up next!'
        else:
            songs = queue.songs._queue
            length = sum(song.length for song in songs) + vc.source.remaining
            time_until = time.human_time(length)
        embed.add_field(name='Time until playing', value=time_until)
        message = await ctx.send(embed=embed)
        await queue.songs.put(source)
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def playlist(self, ctx, *, link: str):
        """Adds tracks from a playlist to the queue."""
        if ctx.author.voice is None:
            return await ctx.send(f' {ctx.message.author.mention}, You need to be in a voice channel.')
        vc = ctx.guild.voice_client
        if vc is None:
            vc = await ctx.invoke(self.summon)

        func = functools.partial(self._ytdl.extract_info, link, download=False)
        info = await ctx.bot.loop.run_in_executor(self.executor, func)
        if 'entries' not in info:
            return await ctx.send(f'{ctx.message.author.mention}, This is not a playlist')
        bad_entries = 0
        for entry in info['entries']:
            try:
                source = await ctx.bot.loop.run_in_executor(self.executor, YoutubeSource, ctx.message, entry.get('webpage_url'))
                queue = self.get_queue(ctx.guild)
                await queue.songs.put(source)
            except Exception:
                bad_entries += 1
        if bad_entries:
            message = await ctx.send('Added {} songs to the queue. {} songs couldn\'t be added.'.format(len(info["entries"]) - bad_entries,ArithmeticError, bad_entries))
            await asyncio.sleep(15)
            await message.delete()
        else:
            message = await ctx.send('Added {} songs to the queue.'.format(len(info["entries"])))
            await asyncio.sleep(15)
            await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def playing(self, ctx):
        """Shows info about the currently playing song."""
        vc = ctx.guild.voice_client
        if vc is None:
            return await ctx.send('Not in a voice channel.')

        if not vc.is_playing() and not vc.is_paused():
            return await ctx.send('Not currently playing anything.')

        message = await ctx.send(embed=vc.source.embed())
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def wheresmysong(self, ctx):
        """Shows how long until your next song will play."""
        vc = ctx.voice_client
        if vc is None:
            return await ctx.send('Not in a voice channel.')

        if not vc.is_playing() and not vc.is_paused():
            return await ctx.send('Not playing any music right now...')
        songs = self.get_queue(ctx.guild).songs._queue
        if not songs:
            return await ctx.send('Nothing currently in the queue.')
        requesters = set(song.requester for song in songs)
        if ctx.author not in requesters:
            return await ctx.send('You are not in the queue!')
        remaining = vc.source.remaining
        for song in songs:
            if song.requester == ctx.author:
                break
            remaining += song.length

        message = await ctx.send('{} until your next song!'.format(time.human_time(remaining)))
        await asyncio.sleep(15)
        await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def queue(self, ctx):
        """Shows the current queue."""
        vc = ctx.voice_client
        if vc is None:
            embed = discord.Embed(description ="I'm not in a voice channel.", color = 0xffffff)
            return await ctx.send(embed = embed)
        if not vc.is_playing() and not vc.is_paused():
            embed = discord.Embed(description = " Not playing anything", color = 0xffffff)
            return await ctx.send(embed = embed)
        queue = self.get_queue(ctx.guild).songs._queue

        if len(queue) == 0:
            return await ctx.invoke(self.playing)
        songs = ['[{}]({})\nRequested by {}'.format(song.entry.title, song.entry.url, song.requester) for song in queue]
        try:
            p = Pages(ctx, entries=songs, per_page=10)
            p.embed.colour = 0x738bd7
            p.embed.title = 'Currently Playing {} requested by {}'.format(vc.source.entry.title, vc.source.requester)
            p.embed.url = vc.source.entry.url
            await p.paginate()
        except Exception as e:
            message = await ctx.send(e)
            await asyncio.sleep(15)
            await message.delete()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def shuffle(self, ctx):
        """Shuffles the current queue."""
        vc = ctx.voice_client
        if vc is None:
            return await ctx.send('Not in a voice channel.')


        queue = self.get_queue(ctx.guild).songs._queue

        if len(queue) == 0:
            return await ctx.send('No songs in the queue.')
        random.shuffle(queue)
        message = await ctx.send('The queue has been shuffled.')
        await asyncio.sleep(15)
        await message.delete()

def setup(bot):
    bot.add_cog(Music(bot))
