import discord
import datetime
import random as rd
import asyncio  
import re
from discord.ext import commands, tasks
from tinydb import TinyDB, Query

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
ongoing_giveaways = db.table('ongoing_giveaways')
ended_giveaways = db.table('ended_giveaways')

class Giveaway():
    def __init__(self, author_id, channel_id, message_id, prize, endtime):
        self.creator_id = author_id
        self.channel_id = channel_id
        self.message_id = message_id
        self.prize = prize
        self.endtime = endtime

GiveawayQuery = Query()

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
        elif time_unit == 'd':
            return time_value * 86400
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

#?All optimised
class GiveawayCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_giveaways.start()

    @commands.command(aliases=['resortear'])
    @commands.has_role('Giveaways')
    async def greroll(self, ctx, id: int = None):
        giveaway = [giveaway for giveaway in ended_giveaways if giveaway["message_id"] == id]
        if giveaway:
            gw = giveaway[0]
            channel = self.bot.get_channel(gw['channel_id'])
            message = await channel.fetch_message(gw['message_id'])
            
            users = await message.reactions[0].users().flatten()
            users.pop(users.index(self.user))
            if len(users):
                winner = rd.choice(users)
                
                await message.reply('Sorteio reiniciado!')
                embed=discord.Embed(title="**SORTEIO REINICIADO! :star2:**", color=0xff0000)
                embed.add_field(name=f"**PARABÉNS {winner.mention}**!", value=f"**Prêmio: {gw['prize']}!**", inline=False)
                embed.set_footer(text="*Abra ticket em até 24 horas para resgatar seu prêmio!*")
                await ctx.send(embed=embed)

                giveaway['rerolled'] = True
                ended_giveaways.update(giveaway, GiveawayQuery.message_id == id)
            else:
                await ctx.send('Membros insuficientes para resortear!', delete_after = 10)
        else:
            await ctx.send('Sorteio não encontrado!', delete_after = 10)
        
    @commands.command(aliases=['delsorteio'])
    @commands.has_role('Giveaways')
    async def gdelete(self, ctx, id: int = None):
        giveaway = [(i, giveaway) for i, giveaway in enumerate(ongoing_giveaways) if giveaway["message_id"] == id]
        if giveaway:
            gwi, gw = giveaway[0]
            ongoing_giveaways.pop(gwi)

            channel = self.bot.get_channel(gw['channel_id'])
            message = await channel.fetch_message(gw['message_id'])
            await message.delete()
            await ctx.send('Sorteio cancelado!', delete_after = 10)

            gw['cancelled'] = True
            ended_giveaways.append(gw)
        else:
            await ctx.send('Sorteio não encontrado ou já encerrado!', delete_after = 10)
        
    @commands.command(aliases=['sortear'])
    @commands.has_role('Giveaways')
    async def gcreate(self, ctx):
        gquestions = {'Em qual canal você quer criar o sorteio?', 'Qual é o prêmio?', 'Quanto tempo o sorteio irá durar?'}
        ganswers = []
        
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel
        
        for question in gquestions:
            await ctx.send(question, delete_after=60)

            try:
                message = await self.wait_for('message', timeout = 60, check = check)
                ganswers.append(message.content)
            except asyncio.TimeoutError:
                await ctx.send('Você não respondeu a tempo! Por favor, responda em até 1 minuto!.')
                return

        try:
            chid = int(ganswers[0][2:-1])
            channel = self.get_channel(chid)
            prize = str(ganswers[1])
        except Exception:
            await ctx.send(f'Você não mencionou o canal corretamente! Por favor, faça assim: {ctx.channel.mention}')
            return
        
        try:
            time = time_input_convert(ganswers[2])
        except Exception:
            await ctx.send('Por favor, defina o tempo com (s/m/h/d)! Exemplo: 30m, 6h.')
            return
        
        await ctx.send(f'O sorteio foi criado em {channel.mention}! Prêmio: {prize}. O sorteio se encerrará em {time_convert(time)}')
        
        endtime = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
        
        embed=discord.Embed(color='0x00ffff', title='**SORTEIO INICIADO!** :star2:', description=f'Reaja com 🎉 para participar!')
        embed.add_field(name=f'**Prêmio:**', value=prize, inline=True)
        embed.add_field(name=f'**Encerra em:**', value=f'{endtime.strftime("%m/%d/%Y, %H:%M")} UTC', inline=True)
        embed.set_footer(text=f'Sorteio iniciado por {ctx.user}!')
        gmessage = await channel.send(embed=embed)
        
        giveaway = Giveaway(ctx.author.id, channel.id, gmessage.id, prize, endtime)
        ongoing_giveaways.insert({'author_id': giveaway.author_id, 'channel_id': giveaway.channel_id, 'message_id':giveaway.message_id, 'prize': giveaway.prize, 'endtime': giveaway.endtime})

        await gmessage.add_reaction('🎉')
        
    @commands.command(aliases=['endsorteio'])
    @commands.has_role('Giveaways')
    async def gend(self, ctx, message_id: int = None):
        if message_id is None:
            await ctx.send('Você deve inserir um ID para encerrar o sorteio!')
            return
        
        gw = ongoing_giveaways.get(GiveawayQuery.message_id == message_id)
        ongoing_giveaways.remove(gw)

        if gw is None:
            await ctx.send('Sorteio não encontrado ou já encerrado!')
            return

        channel = self.bot.get_channel(gw['channel_id'])
        message = await channel.fetch_message(gw['message_id'])

        users = await message.reactions[0].users().flatten()
        users.pop(users.index(self.user))
        winner = rd.choice(users)

        await message.reply('Sorteio encerrado adiantadamente!')
        embed=discord.Embed(title="**SORTEIO ENCERRADO! :star2:**", color=0xff0000)
        embed.add_field(name=f"**PARABÉNS {winner.mention}**!", value=f"**Você ganhou {gw['prize']}!**", inline=False)
        embed.set_footer(text="*Abra ticket em até 24 horas para resgatar seu prêmio!*")
        await channel.send(embed=embed)

        gw['ended_prematurely'] = True
        ended_giveaways.append(gw)

    @tasks.loop(seconds=30)
    async def check_giveaways(self):
        for i, giveaway in enumerate(ongoing_giveaways):
            time = datetime.strptime(giveaway['endtime'], '%Y-%m-%d %H:%M:%S')  
            if datetime.datetime.now() > time:
                gw = ongoing_giveaways.pop(i)
                channel = self.bot.get_channel(gw['channel_id'])
                message = await channel.fetch_message(gw['message_id'])

                users = await message.reactions[0].users().flatten()
                users.pop(users.index(self.user))
                winner = rd.choice(users)

                await message.reply('Sorteio encerrado!')
                embed=discord.Embed(title="**SORTEIO ENCERRADO! :star2:**", color=0xff0000)
                embed.add_field(name=f"**PARABÉNS {winner.mention}**!", value=f"**Você ganhou {gw['prize']}!**", inline=False)
                embed.set_footer(text="*Abra ticket em até 24 horas para resgatar seu prêmio!*")
                await channel.send(embed=embed)

                ended_giveaways.append(gw)

async def setup(bot):
    await bot.add_cog(GiveawayCommands(bot))