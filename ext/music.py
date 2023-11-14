'''
#! Setup
channels = remove or add channels in which bot commands will be listened to
voicechannels = remove or add voice channels in which the bot is allowed to enter 
djrole = create the DJ role
reset = reset the settings

#* Playback
play TITLE|URL (--spotify/deezer/youtube/soundcloud) --next
join - straightforward
leave - straightforward
insert/playnow - straightforward

#* TrackState
backwards - go back the music by {x} seconds
forwards - go forward the music by {x} seconds
pause - straightforward
resume - straightforward
volume - changes the current track volume

#* QueueState
reverse - reverses the queue
shuffle - shuffles the queue
sort - sorts the queue by name, lenght or artist
move - moves a track in the queue
swap - swaps two tracks in the queue
previous - go to the previous music in the queue
skip - skips the current music, or starts a vote
voteskip - forces a vote skip
restartqueue - restarts que queue
loop - loops the current music, or disable looping
loopqueue - loops the queue
random - basically the same as shuffle, a random music will be selected from the queue each time
clear - clears the queue
remove - removes a track from the queue
removedupes - removes all duplicate tracks from the queue

#! Informations
nexttrack - info about the next track
nowplaying - info about the current track
lasttrack - info about the last track
queue - straightforward
albuminfo - straightforward
artistinfo - straightforward
lyrics - straightforward
songinfo - straightforward

#! Settings
maxlength - maximum track length
minlength - minimum track length
voteskip toggle - toggles voteskip
voteskip amount - percentage to skip the music
maxplaylistlength - maximum playlist length
maxplaylisttracks - maximum playlist tracks
maxusertracks - maximum tracks by a user
maxuserlength - maximum length by a user
textannounce toggle - toggles announcing in the chat when a music starts
textannounce text - changes the announcer text, with placeholders (%length%, %title%, %artist%, %album%, %requestedby%)
textannounce autodelete - time to delete the message, 0 to disable
defaultvolume - the volume each section the bot enters the voicechannel
blacklist author|music - blacklists an author or music
unblacklist author|music - unblacklists an author or music
removeafterplayed - the music will be removed after played

#! Permissions
permissions role|user|everyone list - list the permissions of a group
permissions role|user|everyone set permission false|true - changes a permission of a group
List of permissions: (you can use * as a wildcard)
queue.clear; queue.remove; queue.shuffle; queue.edit; player.play; player.skip; player.insert; 
player.wind; player.loop; player.random; client.leave; client.volume; blacklist.add;
 blacklist.remove; admin.settings

#! General
donate = straightforward
@leaderboard = most minutes with the bot
leaderboard = most played songs, most minutes with the bot
help - lists all commands
changelog - Lists bot changelog

'''

import discord
from pytube import YouTube, Playlist #type: ignore
from youtube_search import YoutubeSearch as yts #type: ignore
import asyncio
from discord.ext import commands, tasks
import os
from tinydb import TinyDB, Query
import re
import random
from math import ceil
import spotipy #type: ignore        
from spotipy.oauth2 import SpotifyOAuth #type: ignore
import datetime
from _util_funcs import time_input_convert, time_convert

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
settings_table = db.table('music_settings')
players_table = db.table('music_members')

Q = Query()

class Decorators:
    @staticmethod
    def has_permission(permission):
        async def predicate(self, ctx):
            return True
        return commands.check(predicate)
    
    @staticmethod
    def is_with_bot():
        async def predicate(self, ctx):
            voice_client = ctx.voice_client
            if voice_client and voice_client.is_playing():
                members = voice_client.channel.members
                if ctx.author in members:
                    return True
                
            ctx.send('Você deve estar no mesmo canal do bot para usar este comando e o bot deve estar funcionando!')
            return False

        return commands.check(predicate)

def get_player(member):
    player = players_table.get(Q.id == member.id)
    if player is None:
        _player = Player(member.id)
        players_table.insert({'id': _player.id, 'permissions': _player.permissions, 'musics': _player.musics, 'time_with_bot': _player.time_with_bot})
        
    return players_table.get(Q.id == member.id)

class Player:
    def __init__(self, member_id):
        self.id = member_id
        self.permissions = ['player.play']
        self.musics = {}
        self.time_with_bot = 0

queue: list = []
queue_index: int = 0
configs: dict = {'play_type': 'loopqueue'}

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
        else:
            match configs['play_type']:
                case 'random':
                    queue_index = random.randint(0, len(queue))
                case 'loopqueue':
                    queue_index = (queue_index + 1) if queue_index < len(queue) else 0
                case 'loop':
                    queue_index = queue_index
                case _:
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

        player = get_player(ctx.author)

        if results[0]['url_suffix'] not in player['musics'].keys():
            player['musics']['url_suffix'] = [1, {'title': yt.title, 'author': yt.author}]
        else:
            player['musics']['url_suffix'][0] += 1

        players_table.update(player, Q.id == ctx.author.id)
    
    @commands.command()
    async def join(self, ctx):
        voice = await self._join(self, ctx)
        if ctx.author.voice.channel is not None and voice.channel == ctx.author.voice.channel:
            await ctx.send('O bot já está conectado em seu canal!')
        
    @commands.command()
    @Decorators.has_permission('player.leave')
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

    async def _retrieve_track_info(self, ctx, index, loop = False):
        music = queue[index]
        embed=discord.Embed(title=f'**Tocando agora {"(em loop)" if loop else ""}!**', color=0xff0000)
        embed.set_thumbnail(url=f'{music[0].thumbnail_url}')
        embed.add_field(name='Título', value=f'{music[0].title}', inline=True)
        embed.add_field(name='Canal', value=f'{music[0].author}', inline=True)
        embed.add_field(name='Duração', value=f'{music[0].length} segundos', inline=True)
        embed.add_field(name='Views', value=f'{music[0].views}', inline=True)
        embed.add_field(name='Posição na fila', value=f'{index}')
        embed.add_field(name='Musicas até tocar', value=f'{index if index > 0 else len(queue)+queue_index}')
        embed.add_field(name='Link', value=f'||{music[2]}||')
        embed.set_footer(text='Digite !queue para ver a fila!')
        await ctx.send(embed=embed)

    @commands.command()
    async def nowplaying(self, ctx):
        self._retrieve_track_info(self, ctx, queue_index)
    
    @commands.command()
    async def lasttrack(self, ctx): 
        if configs['play_type'] == 'loop':
            self._retrieve_track_info(self, ctx, queue_index, True)
            return
        
        self._retrieve_track_info(self, ctx, queue_index-1)

    @commands.command()
    async def nexttrack(self, ctx):
        if configs['play_type'] == 'random':
            await ctx.send('Comando `nexttrack` desativado no modo aletório.')

        elif configs['play_type'] == 'loop':
            self._retrieve_track_info(self, ctx, queue_index, True)
        
        else:
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
        match _type:
            case 'artist'|'artista'|'author'|'autor':
                queue = sorted(queue, key=lambda i: i[0].author)
            case 'name'|'nome'|'title'|'titulo':
                queue = sorted(queue, key=lambda i: i[0].title)
            case 'length'|'duracao':
                queue = sorted(queue, key=lambda i: i[0].length)
            case 'views'|'visualizacoes':
                queue = sorted(queue, key=lambda i: i[0].views)
            case _:
                await ctx.send('O tipo de ordenação deve ser `artista, titulo, views ou duracao`!')
                return
        
        await ctx.send(f'Ordenou a lista por {_type}')

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
        await ctx.send(f'Moveu a música {item[0].title} para a {"última" if end_pos == len(queue) else f"{end_pos}°"} posição!')        

    @commands.command()
    @Decorators.has_permission('queue.edit')
    @Decorators.is_with_bot()
    async def swap(self, ctx, item1, item2):
        if not isinstance(item1, int) or not isinstance(item2, int):
            await ctx.send('A posição dos ítens deve ser um número inteiro!')
            return
            
        if item1 > len(queue) or item2 > len(queue) or item1 == item2 or item1 <= 0 or item2 <= 0:
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
            await ctx.send('Voltou para a última música!')
        else:
            await ctx.send('Não há músicas para reproduzir!')

    @commands.command()
    @Decorators.has_permission('queue.forceskip')
    @Decorators.is_with_bot()
    async def forceskip(self, ctx):
        voice_client = ctx.voice_client

        if voice_client and voice_client.is_playing():
            voice_client.stop()
            MusicPlayer._play_next(self, ctx)
            await ctx.send('Pulou a música!')
        else:
            await ctx.send('Não há musicas para serem puladas!')
    
    @commands.command()
    @Decorators.is_with_bot()
    async def skip(self, ctx):
        voice_client = ctx.voice_client

        if voice_client and voice_client.is_playing():
            _members = voice_client.channel.members
            _members.pop(self.bot.user)
        else:
            await ctx.send('Não há musicas para serem puladas!')
        
        self.members |= {member.id:False for member in _members if member not in self.members}
        [self.members.pop(member.id) for member in self.members if member not in _members]
        
        self.members[ctx.author.id] = True

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
            configs['play_type'] = 'default'
            ctx.send('Desativou a repetição da fila!')
        else:
            configs['play_type'] = 'loopqueue'
            ctx.send('Ativou a repetição da fila!')

    @commands.command()
    @Decorators.has_permission('player.random')
    @Decorators.is_with_bot()
    async def random(self, ctx):
        if configs['play_type'] == 'random':
            configs['play_type'] = 'default'
            ctx.send('Desativou a ordem aleatória!')
        else:
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
        await ctx.send(f'Removeu {item[0].title} da fila!')

    @commands.command()
    @Decorators.has_permission('queue.remove')
    @Decorators.is_with_bot()
    async def removedupes(self, ctx):
        unique_queue = []
        seen_urls = set()
        
        for item in queue:
            if item[2] not in seen_urls:
                seen_urls.add(item[2])
                unique_queue.append(item)

        global queue
        queue = unique_queue
        await ctx.send('Removeu todas as músicas duplicadas da fila!')

class Leaderboards(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot_time_start = {}
        self.time_with_bot.start()

    @tasks.loop(minutes=1)
    async def time_with_bot(self):
        for member, start_time in list(self.bot_time_start.items()):
            duration = datetime.now() - start_time

            if duration >= datetime.timedelta(minutes=1):
                self.bot_time_start[member] = datetime.now()
                player = get_player(member)
                player['time_with_bot'] += 1

                players_table.update(player, Q.id == player['id'])

    @commands.command()
    async def musicleaderboard(self, ctx):
        members = {members[member['id']]: [self.bot.get_user(member), member[member['time_with_bot']]] for member in players_table}
        members = sorted(members, lambda m: members[m][1], reversed = True)[:10]
        message = '\n'.join([f'{i}. {members[member][0].display_name}: {members[member][1]} minutos' for i, member in enumerate(members)])
        embed = discord.Embed(title='Ranking de tempo com o bot', description=message)
        await ctx.send(embed=embed)

    @commands.command()
    async def mostplayedmusics(self, ctx):
        musics_list = {}
        for member in players_table:
            for music in member['musics']:
                if music not in musics_list:
                    musics_list[music] = [music[0], {'title': music[1]['title'], 'author': music[1]['author']}]
                else:
                    musics_list[music][0] += music[0]
        
        musics = sorted(musics, key = lambda m: musics[m][0], reversed = True)[:10] # Sorts the top 10 musics
        message = '\n'.join([f'{i}. {musics[music][1]["title"]} - {musics[music][0]} vezes'] for i, music in enumerate(musics))
        embed = discord.Embed(title='Músicas mais tocadas', description=message)
        await ctx.send(embed=embed)

    @commands.command()
    async def musicprofile(self, ctx, member: discord.Member | None = None):
        if not isinstance(member, discord.Member):
            member = ctx.author

        player = get_player(member)
        
        total_musics = 0
        for music in player['musics']:
            total_musics += music[0]

        total_time = time_convert(player['time_with_bot'], 'min')
        top_musics = sorted(player['musics'], key = lambda m: m[0], reverse = True)[:10]
        message = '\n'.join([f'{i}. {top_musics[music][1]["title"]} - {top_musics[music[0]]} vezes' for i, music in enumerate(top_musics)])
        
        embed = discord.Embed(title=f'Perfil de {member.display_name}', description=f'Músicas mais tocadas:\n{message}')
        embed.add_field(name='Total de músicas', value=f'{total_musics}')
        embed.add_field(name='Músicas diferentes', value=f'{total_time}')
        embed.add_field(name='Total de tempo', value=f'{player["time_with_bot"]} minutos')
        embed.set_footer(text='Para ver o perfil completo, digite !perfil {membro}!')
        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(MusicPlayer(bot))