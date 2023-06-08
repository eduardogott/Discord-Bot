import discord
from pytube import YouTube
from youtube_search import YoutubeSearch as yts
import asyncio  
from discord.ext import commands
import os
    
class VoiceError(Exception): 
    pass

class YTDLError(Exception): 
    pass

#* All working!
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = []
        self.base_url = "https://youtube.com"

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, music = None):
        if music == None or len(music) <= 3:
            await ctx.send("Nome muito pequeno! Use: !play (musica ou link)", delete_after = 10)
        else:
            if ctx.author.voice == None:
                await ctx.send('Você precisa estar em um canal de voz!', delete_after = 10)
            else:
                if ctx.voice_client == None:
                    voice = await ctx.author.voice.channel.connect(self_deaf=True)

                else:
                    voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)

                    
                if ctx.voice_client.channel != ctx.author.voice.channel:
                    await ctx.send('O bot está conectado em outro canal!', delete_after = 10)

                else:
                    results = yts(music, max_results=5).to_dict()
                    yt = YouTube(self.base_url + results[0]['url_suffix'])
                    ys = yt.streams.filter(only_audio=True).order_by('abr').desc().first()

                    self.queue.append([yt, ys.download(), self.base_url + results[0]['url_suffix']])

                    embed=discord.Embed(title='**Música adicionada a fila!**', color=0xff0000)
                    embed.set_thumbnail(url=f'{yt.thumbnail_url}')
                    embed.add_field(name='Título', value=f'{yt.title}', inline=True)
                    embed.add_field(name='Canal', value=f'{yt.author}', inline=True)
                    embed.add_field(name='Duração', value=f'{yt.length} segundos', inline=True)
                    embed.add_field(name='Views', value=f'{yt.views}', inline=True)
                    embed.add_field(name='Posição', value=f'{len(self.queue)}° na fila', inline=True)
                    embed.set_footer(text='Digite !queue para ver a fila!')
                    await ctx.send(embed=embed)

                    if not voice.is_playing():
                        await self.play_next(ctx, voice)
    
    async def play_next(self, ctx, voice):
        if len(self.queue) > 0:
            global music
            music = self.queue.pop(0)
            voice.play(discord.FFmpegPCMAudio(music[1]), after=lambda e: self.bot.loop.create_task(self.play_next(ctx, voice)))
            await ctx.send(f'Tocando {music[0].title}')
            voice.is_playing()
        else:
            await voice.disconnect()
            asyncio.sleep(3)
            for file in os.listdir('.'):
                if os.path.splitext(file)[1] == '.webm':
                    os.remove(file)
            
    @commands.command(aliases=['s'])
    async def skip(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_playing():
            voice.stop()

    @commands.command()
    @commands.has_role('DJ')
    async def clearqueue(self, ctx):
        self.queue = []
        await ctx.send('Limpou a fila!')

    @commands.command(aliases=['q'])
    async def queue(self, ctx):
        if len(self.queue):
            output = [f'{i}. {item[0].title}\n' for i, item in enumerate(self.queue, start=1)]
            embed = discord.Embed(title=':musical_note: Fila de músicas', description=output, color=0xff0000)
            await ctx.send(embed)
        else:
            await ctx.send(f'A fila está vazia!')

    @commands.command()
    @commands.has_role('DJ')
    async def remove(self, ctx, arg):
        try:
            arg = int(arg)
        except:
            await ctx.send('Digite !remove (número)!', delete_after = 10)
        else:
            if arg > len(self.queue):
                await ctx.send('Você digitou um número maior do que a fila (!queue)!', delete_after = 10)
            else:
                removed_song = self.queue.pop(arg)
                await ctx.send(f'Removeu {removed_song[0].title} da fila!')
    
    @commands.command()
    @commands.has_role('DJ')
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.pause()
        await ctx.send('Pausou!')

    @commands.command(aliases=['resumir', 'unpause'])
    @commands.has_role('DJ')
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.resume()
        await ctx.send('Resumiu!')

    @commands.command(aliases=['np', 'nowplaying'])
    async def musica(self, ctx):
        embed=discord.Embed(title='**Tocando agora!**', color=0xff0000)
        embed.set_thumbnail(url=f'{music[0].thumbnail_url}')
        embed.add_field(name='Título', value=f'{music[0].title}', inline=True)
        embed.add_field(name='Canal', value=f'{music[0].author}', inline=True)
        embed.add_field(name='Duração', value=f'{music[0].length} segundos', inline=True)
        embed.add_field(name='Views', value=f'{music[0].views}', inline=True)
        embed.add_field(name='Link', value=f'||{music[2]}||')
        embed.set_footer(text='Digite !queue para ver a fila!')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def replay(self, ctx):
        self.queue.append([music[0], music[1].download()])
        embed=discord.Embed(title='**Música adicionada a fila!**', color=0xff0000)
        embed.set_thumbnail(url=f'{music[0].thumbnail_url}')
        embed.add_field(name='Título', value=f'{music[0].title}', inline=True)
        embed.add_field(name='Canal', value=f'{music[0].author}', inline=True)
        embed.add_field(name='Duração', value=f'{music[0].length} segundos', inline=True)
        embed.add_field(name='Views', value=f'{music[0].views}', inline=True)
        embed.add_field(name='Posição', value=f'{len(self.queue)}° na fila', inline=True)
        embed.set_footer(text='Digite !queue para ver a fila!')
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))