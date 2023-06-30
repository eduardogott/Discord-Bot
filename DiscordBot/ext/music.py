import discord
from pytube import YouTube, Playlist
from youtube_search import YoutubeSearch as yts
import asyncio  
from discord.ext import commands
import os
from tinydb import TinyDB, Query
import re
import random
from math import ceil

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
settings_table = db.table('music_settings')

def time_input_convert(time_string):
    match = re.match(r'(\d+)\s*(s|m|h|d)', time_string)
    if match:
        time_value, time_unit = match.groups()
        time_value = int(time_value)
        if time_unit == 's':
            return time_value
        elif time_unit == 'm':
            return time_value * 60
        elif time_unit == 'h':
            return time_value * 3600
    return -1
def time_convert(seconds: int = None, type: str = None):
    if type == 'min':
        seconds *= 60
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    return '{}{}h {}m'.format(str(days) + 'd ' if days > 0 else '', 
                              str(hours) if hours > 0 else '',
                              str(minutes) if minutes > 0 else '')

class Decorators:
    def has_permission(self, permission):
        async def predicate(ctx):
            return True
        return commands.check(predicate)
    
    def is_with_bot(self):
        async def predicate(ctx):
            voice_client = ctx.voice_client
            if voice_client and voice_client.is_playing():
                members = voice_client.channel.members
                if ctx.author in members:
                    return True
                
            ctx.send('Você deve estar no mesmo canal do bot para usar este comando e o bot deve estar funcionando!')
            return False

        return commands.check(predicate)

class MemberObject:
    def __init__(self, member_id):
        self.id = member_id
        self.permissions = ['player.play']
        self.musics = {}

queue = []
queue_index = 0
configs = {'play_type': 'loopqueue'}

class MusicPlayer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pattern = r'^(https:\/\/\.|www\.|open\.)*$'
        self.spotify_playlist = r'^(https://)?open.spotify.com/playlist/*$'
        self.youtube_playlist = r'^(https://)?www.youtube.com/playlist*$'
        self.base_url = "https://youtube.com"

    async def _join(self, ctx):
        if ctx.author.voice is None and ctx.author.voice.channel is None:
            await ctx.send('Você precisa estar em um canal de voz!')
            return
        
        if ctx.voice_client is None:
            voice = await ctx.author.voice.channel.connect(self_deaf=True)

        else:
            voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send('O bot está conectado em outro canal!')
        
        return voice

    async def _play_next(self, ctx, voice, type = None):
        global music, queue_index
        music = queue[queue_index]
        if type == 'restart':
            queue_index = queue_index
        elif configs['play_type'] == 'random':
            queue_index = random.randint(0, len(queue))
        elif configs['play_type'] == 'loopqueue':
            queue_index = (queue_index + 1) if queue_index < len(queue) else 0
        elif configs['play_type'] == 'loop':
            queue_index = queue_index
        else:
            queue_index += 1

        if queue_index > len(queue):
            await ctx.send('Sem músicas na fila!')
            voice.disconnect()
            asyncio.sleep(3)
            for file in os.listdir('.'):
                if os.path.splitext(file)[1] == '.webm':
                    os.remove(file)

        voice.play(discord.FFmpegPCMAudio(music[1]), after=lambda e: self.bot.loop.create_task(self.play_next(ctx, voice)))
        await ctx.send(f'Tocando {music[0].title}')
        voice.is_playing()            

    async def _play(self, ctx, type, *, music):
        if music is None or len(music) <= 3:
            await ctx.send("Nome muito pequeno! Use: !play (musica ou link)", delete_after = 10)
            return

        if ctx.author.voice == None:
            await ctx.send('Você precisa estar em um canal de voz!', delete_after = 10)
            return
        
        voice = self._join(self, ctx)

        if not re.match(self.pattern, music):
            results = yts(music, max_results=5).to_dict()
            yt = YouTube(self.base_url + results[0]['url_suffix'])
            ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
            if type == 'insert':
                queue.insert(queue_index+1, [yt, ys.download(), self.base_url + results[0]['url_suffix']])
                position = queue_index+1
            else:
                queue.append([yt, ys.download(), self.base_url + results[0]['url_suffix']])
                position = len(queue)

            embed=discord.Embed(title='**Música adicionada a fila!**', color=0xff0000)
            embed.set_thumbnail(url=f'{yt.thumbnail_url}')
            embed.add_field(name='Título', value=f'{yt.title}', inline=True)
            embed.add_field(name='Canal', value=f'{yt.author}', inline=True)
            embed.add_field(name='Duração', value=f'{yt.length} segundos', inline=True)
            embed.add_field(name='Views', value=f'{yt.views}', inline=True)
            embed.add_field(name='Posição na fila', value=f'{position}° na fila', inline=True)
            embed.add_field(name='Musicas até tocar', value=f'{position-queue_index}')
            embed.set_footer(text='Digite !queue para ver a fila!')
            await ctx.send(embed=embed)

            if not voice.is_playing():
                await self._play_next(ctx, voice)

    @commands.command()
    async def join(self, ctx):
        voice = await self._join(self, ctx)
        if ctx.author.voice.channel is not None and voice.channel == ctx.author.voice.channel:
            await ctx.send('O bot já está conectado em seu canal!')
        
    @commands.command()
    @Decorators.has_permission('voice.leave')
    @Decorators.is_with_bot()
    async def leave(self, ctx):
        if ctx.voice_client.channel != ctx.author.voice.channel:
            await ctx.send('O bot está conectado em outro canal!')
            return
        
        ctx.voice_client.disconnect()
        await ctx.send('Desconectado!')
    
    @commands.command()
    @Decorators.has_permission('player.play')
    async def play(self, ctx, *, music = None):
        self._play(self, ctx, 'play', music)
    
    @commands.command()
    @Decorators.has_permission('player.insert')
    async def insert(self, ctx, *, music = None):
        self._play(self, ctx, 'insert', music)
    
    @commands.command()
    @Decorators.has_permission('player.play')
    @Decorators.is_with_bot()
    async def replay(self, ctx):
        queue.append(queue[queue_index])
        embed=discord.Embed(title='**Música adicionada a fila!**', color=0xff0000)
        embed.set_thumbnail(url=f'{music[0].thumbnail_url}')
        embed.add_field(name='Título', value=f'{music[0].title}', inline=True)
        embed.add_field(name='Canal', value=f'{music[0].author}', inline=True)
        embed.add_field(name='Duração', value=f'{music[0].length} segundos', inline=True)
        embed.add_field(name='Views', value=f'{music[0].views}', inline=True)
        embed.add_field(name='Posição na fila', value=f'{len(queue)}')
        embed.add_field(name='Musicas até tocar', value=f'{len(queue)-queue_index}')
        embed.add_field(name='Link', value=f'||{music[2]}||')
        embed.set_footer(text='Digite !queue para ver a fila!')
        await ctx.send(embed=embed)

    @commands.command()
    @Decorators.has_permission('player.pause')
    @Decorators.is_with_bot()
    async def pause(self, ctx):
        ctx.voice_client.pause()
        await ctx.send("Pausou!")

    @commands.command()
    @Decorators.has_permission('player.pause')
    @Decorators.is_with_bot()
    async def resume(self, ctx):
        ctx.voice_client.resume()
        await ctx.send('Despausou!')

    @commands.command()
    @Decorators.has_permission('player.wind')
    @Decorators.is_with_bot()
    async def forward(self, ctx, _time = None):
        _time = time_input_convert(_time)
        if _time == -1:
            await ctx.send('Você inseriu um tempo inválido! Insira: [tempo(s/m/h)]')
            return
        
        target_position = ctx.voice_client.source._player._position + _time

        if target_position >= ctx.voice_client.source._duration:
            await ctx.send("Você não pode inserir um tempo maior do que o restante da música!")
            return
        
        ctx.voice_client.source._player.seek(target_position)
        await ctx.send(f'Avançou {time_convert(_time)} segundos!')

    @commands.command()
    @Decorators.has_permission('player.wind')
    @Decorators.is_with_bot()
    async def backwards(self, ctx, _time = None):
        _time = time_input_convert(_time)
        if _time == -1:
            await ctx.send('Você inseriu um tempo inválido! Insira: [tempo(s/m/h)]')
            return
        
        target_position = ctx.voice_client.source._player._position - _time
        if target_position < 0: target_position = 0

        ctx.voice_client.source._player.seek(target_position)
        await ctx.send(f'Voltou {f"{time_convert(_time)} segundos" if target_position != 0 else "ao início"}!')

    @commands.command()
    @Decorators.has_permission('player.wind')
    @Decorators.is_with_bot()
    async def restart(self, ctx):
        ctx.voice_client.source._player.seek(0)
        await ctx.send(f'Reiniciou a música!')

    @commands.command()
    @Decorators.has_permission('client.volume')
    @Decorators.is_with_bot()
    async def volume(self, ctx, volume = None):
        if not isinstance(volume, int) or not 0 > volume > 500:
            await ctx.send('O volume deve ser um número inteiro entre 0 e 200!')
            return
        
        ctx.voice_client.source.volume = volume/100
        await ctx.send(f"Volume definido em {volume}!")
        

class MusicInformations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def _retrieve_track_info(self, ctx, index):
        music = queue[index]
        embed=discord.Embed(title='**Tocando agora!**', color=0xff0000)
        embed.set_thumbnail(url=f'{music[0].thumbnail_url}')
        embed.add_field(name='Título', value=f'{music[0].title}', inline=True)
        embed.add_field(name='Canal', value=f'{music[0].author}', inline=True)
        embed.add_field(name='Duração', value=f'{music[0].length} segundos', inline=True)
        embed.add_field(name='Views', value=f'{music[0].views}', inline=True)
        embed.add_field(name='Posição na fila', value=f'{index}')
        embed.add_field(name='Musicas até tocar', value=f'{index}')
        embed.add_field(name='Link', value=f'||{music[2]}||')
        embed.set_footer(text='Digite !queue para ver a fila!')
        await ctx.send(embed=embed)

    @commands.command()
    async def nowplaying(self, ctx):
        self._retrieve_track_info(self, ctx, queue_index)
    
    @commands.command()
    async def lasttrack(self, ctx):
        self._retrieve_track_info(self, ctx, queue_index-1)
    
    @commands.command()
    async def nexttrack(self, ctx):
        self._retrieve_track_info(self, ctx, queue_index+1)

    @commands.command()
    async def queue(self, ctx):
        if len(self.queue):
            output = [f'{i}. {item[0].title}\n' for i, item in enumerate(self.queue, start=1)]
            embed = discord.Embed(title=':musical_note: Fila de músicas', description=output, color=0xff0000)
            await ctx.send(embed)
        else:
            await ctx.send(f'A fila está vazia!')
    
    @commands.command()
    async def trackinfo(self, ctx, index):
        if not isinstance(index, int):
            await ctx.send('Insira um número válido!')
            return

        if index > len(queue):
            await ctx.send('Você inseriu um número muito alto!')
            return
        
        self._retrieve_track_info(self, ctx, index-1)
    
class MusicQueueState(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.members = {}

    @commands.command()
    @Decorators.has_permission('queue.edit')
    @Decorators.is_with_bot()
    async def reverse(self, ctx):
        queue.reverse()
        await ctx.send('Inverteu a fila!')

    @commands.command()
    @Decorators.has_permission('queue.shuffle')
    @Decorators.is_with_bot()
    async def shuffle(self, ctx):
        random.shuffle(queue)
        await ctx.send('Embaralhou a fila!')

    @commands.command()
    @Decorators.has_permission('queue.edit')
    @Decorators.is_with_bot()
    async def sort(self, ctx, _type = None):
        global queue
        match _type:
            case 'artist':
                queue = sorted(queue, key=lambda i: i[0].author)
            case 'name':
                queue = sorted(queue, key=lambda i: i[0].title)
            case 'length':
                queue = sorted(queue, key=lambda i: i[0].length)
            case 'views':
                queue = sorted(queue, key=lambda i: i[0].views)
            case _:
                await ctx.send('O tipo de ordenação deve ser `artist, name, views ou length`!')

    @commands.command()
    @Decorators.has_permission('queue.edit')
    @Decorators.is_with_bot()
    async def move(self, ctx, start_pos, end_pos):
        if not isinstance(start_pos, int) or not isinstance(end_pos, int):
            await ctx.send('A posição de início e fim deve ser um número inteiro!')
            return
        
        if start_pos > len(queue) or start_pos == end_pos:
            await ctx.send('As posições devem ser diferentes e menores que o tamanho da fila!')
            return

        item = queue.pop(start_pos)
        queue.insert(end_pos, item)
        await ctx.send(f'Moveu a música {item[0].title} para a {"última" if end_pos >= len(queue) else end_pos} posição!')        

    @commands.command()
    @Decorators.has_permission('queue.edit')
    @Decorators.is_with_bot()
    async def swap(self, ctx, item1, item2):
        if not isinstance(item1, int) or not isinstance(item2, int):
            await ctx.send('A posição dos ítens deve ser um número inteiro!')
            return
        
        if item1 > len(queue) or item2 > len(queue) or item1 == item2:
            await ctx.send('As posições devem ser diferentes e menores que o tamanho da fila!')
            return
        
        queue[item1], queue[item2] = queue[item2], queue[item1]

        await ctx.send(f'Inverteu as músicas {queue[item1][0].title} e {queue[item2][0].title} de posição na fila!')

    @commands.command()
    @Decorators.has_permission('queue.skip')
    @Decorators.is_with_bot()
    async def previous(self, ctx):
        global queue_index
        queue_index -= 2
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            MusicPlayer._play_next(self, ctx)

    @commands.command()
    @Decorators.has_permission('queue.skip')
    @Decorators.is_with_bot()
    async def forceskip(self, ctx):
        voice_client = ctx.voice_client

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            MusicPlayer._play_next(self, ctx)
    
    @commands.command()
    @Decorators.is_with_bot()
    async def skip(self, ctx):
        voice_client = ctx.voice_client

        if voice_client and voice_client.is_playing():
            _members = voice_client.channel.members
            _members.pop(self.bot.user)
        
        self.members = {member:False for member in _members if member not in self.members}
        [self.members.pop(member) for member in self.members if member not in _members]
        
        self.members[ctx.author] = True

        if sum(self.members.values()) / len(self.members) > 0.5:
            await ctx.send('Pulou a música!')
            voice_client.stop()
            MusicPlayer._play_next(self, ctx)
        else:
            await ctx.send(f'Votou para pular a música! ({sum(self.members.values())}/{ceil(len(self.members)/2)} votos necessários)')
            
    @commands.command()
    @Decorators.has_permission('queue.restart')
    @Decorators.is_with_bot()
    async def restartqueue(self, ctx):
        global queue_index
        queue_index = 0
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()
            MusicPlayer._play_next(self, ctx)
    
    @commands.command()
    @Decorators.has_permission('player.loop')
    @Decorators.is_with_bot()
    async def loop(self, ctx):
        if configs['play_type'] == 'loop':
            global configs
            configs['play_type'] = 'default'
            ctx.send('Desativou a repetição!')
        else:
            global configs
            configs['play_type'] = 'loop'
            ctx.send('Ativou a repetição!')

    @commands.command()
    @Decorators.has_permission('player.loop')
    @Decorators.is_with_bot()
    async def loopqueue(self, ctx):
        if configs['play_type'] == 'loopqueue':
            global configs
            configs['play_type'] = 'default'
            ctx.send('Desativou a repetição da fila!')
        else:
            global configs
            configs['play_type'] = 'loopqueue'
            ctx.send('Ativou a repetição da fila!')

    @commands.command()
    @Decorators.has_permission('player.random')
    @Decorators.is_with_bot()
    async def random(self, ctx):
        if configs['play_type'] == 'random':
            global configs
            configs['play_type'] = 'default'
            ctx.send('Desativou a ordem aleatória!')
        else:
            global configs
            configs['play_type'] = 'random'
            ctx.send('Ativou a ordem aleatória!')

    @commands.command()
    @Decorators.has_permission('queue.clear')
    @Decorators.is_with_bot()
    async def clear(self, ctx):
        global queue
        queue = []
        await ctx.send('Limpou a fila de músicas!')

    @commands.command()
    @Decorators.has_permission('queue.remove')
    @Decorators.is_with_bot()
    async def remove(self, ctx, index = None):
        if index is None or not isinstance(index, int) or index >= len(queue):
            await ctx.send('Insira um número válido, menor que o tamanho da fila!')
            return
        
        item = queue.pop(index)
        await ctx.send(f'Removeu {item[0].title}!')

    @commands.command()
    @Decorators.has_permission('queue.remove')
    @Decorators.is_with_bot()
    async def removedupes(self, ctx):
        global queue
        queue = list(set(queue))
        await ctx.send('Removeu todas as músicas duplicadas da fila!')

async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))