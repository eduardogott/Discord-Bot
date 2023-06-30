import discord
import random as rd
import wikipedia as wp
from discord.ext import commands, tasks
import ast
import requests
import re
from tinydb import TinyDB, Query
import datetime
import json

with open('config.json') as f:
    file = json.load(f)
    config = file['Configuration']['Utils']

meses = {1: 'janeiro',
         2: 'fevereiro',
         3: 'março',
         4: 'abril',
         5: 'maio',
         6: 'junho',
         7: 'julho',
         8: 'agosto',
         9: 'setembro',
         10: 'outubro',
         11: 'novembro',
         12: 'dezembro'}

def time_convert(seconds, type = None):
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

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
reminders_table = db.table('reminders')

class Reminder():
    def __init__(self, player_id, time, channel_id, text):
        self.id = player_id
        self.time = time
        self.channel_id = channel_id
        self.reminder = text

ReminderQuery = Query()

#* All working!
class RNGs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.choice_emojis = {'papel':':newspaper:','pedra':':rock:','tesoura':':scissors:'}

        wp.set_lang('pt')
        
    @commands.command()
    async def random(self, ctx, minimum: int = None, maximum: int = None):
        if minimum is None or maximum is None:
            await ctx.send('Você precisa informar o mínimo e o máximo! Ex: !random 1 100')
            return 
        if minimum > maximum:
            minimum, maximum = maximum, minimum
        
        maximum = min(maximum, 1000000000)
        minimum = max(minimum, -1000000000)

        await ctx.send(f'Sorteando um número entre {minimum} e {maximum}')
        x = rd.randint(minimum, maximum)
        await ctx.send(f'O número sorteado é: {x}')

    @commands.command(aliases=['dice'])
    async def dado(self, ctx, maximum: int = 6):
        if maximum >= 2:
            maximum = min(maximum, 1000000000)
            x = rd.randint(1, maximum)
            await ctx.send(f'Rolando um D{maximum}... O resultado é {x}!')
        else:
            await ctx.send('O dado precisa ter no mínimo 2 lados!')
        
    @commands.command(aliases=['ppt', 'rps', 'rockpaperscissors', 'pedrapapeltesoura', 'jokenpo'])
    async def jankenpon(self, ctx, user_choice: str = None):
        if user_choice not in {'pedra', 'papel', 'tesoura'}:
            await ctx.send('Você deve escolher `pedra`, `papel` ou `tesoura`!', delete_after = 10)
            return
        
        bot_choice = rd.choice(['pedra', 'papel', 'tesoura'])

        if user_choice == bot_choice:
            result = 'Empatou!'

        elif (user_choice, bot_choice) in {('pedra', 'tesoura'), ('papel', 'pedra'), ('tesoura', 'papel')}:
            result = 'Você venceu!'
        
        else:
            result = 'Eu ganhei!'

        await ctx.send(f'Eu escolho {bot_choice} {self.choice_emojis[bot_choice]}! {result}')
                
    @commands.command(aliases=['choice'])
    async def escolher(self, ctx, *args):
        if len(args) <= 1:
            await ctx.send('Insira pelo menos 2 palavras para mim escolher!')
        else:
            x = rd.choice(args)
            await ctx.send(f'Eu escolho {x}!')

#? All optimised!
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tinyurl_api = 'https://tinyurl.com/api-create.php?url='
        self.check_reminders.start()

    @commands.command(aliases=['short', 'shorturl', 'bitly', 'tinyurl'])
    @commands.cooldown(1, config['URLShortenerDelay'], commands.BucketType.user)
    async def shorten(self, ctx, url: str = None):
        if url is None:
            await ctx.send('Você não forneceu uma URL para encurtar!', delete_after = 10)
            return
        
        try:
            response = requests.get(self.tinyurl_api + url)
            if response.ok:
                await ctx.send(f'URL encurtada: {response.text}')
            else:
                await ctx.send(f'Não foi possível encurtar a URL `{url}`.')

        except (requests.exceptions.HTTPError, requests.exceptions.RequestException):
            await ctx.send(f'Não foi possível encurtar a URL `{url}`.')

    @shorten.error
    async def shorten_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining = round(error.retry_after)
            await ctx.send(f'Este comando está em cooldown! Aguarde {time_convert(remaining)} e tente novamente!')

    @commands.command(aliases=['lembrete','reminder'])
    async def remindme(self, ctx, time = None, text = None):
        if time is None or text is None:
            await ctx.send('Você deve inserir um tempo (s/m/h/d) e um lembrete! Ex: !remindme 7d MotivoExemplo')
            return
        
        time = time_input_convert(time)
        if time == -1:
            await ctx.send('Você inseriu um tempo inválido! Deve ser no formato [número](s/m/h/d), ex: 30m, 12h, 7d.')
            return
        
        db_time = (datetime.datetime.now() + datetime.timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
        reminder = Reminder(ctx.author.id, db_time, ctx.channel.id, text)

        reminders_table.insert({'id':reminder.id,'time':reminder.time,'channel_id':reminder.channel_id,'reminder':reminder.reminder})
        await ctx.send('Lembrete criado com sucesso!')

    @commands.command(aliases=['votacao'])
    @commands.has_role('cargo 2')
    async def poll(self, ctx, question = None):
        if question is None:
            await ctx.send('Você deve colocar uma pergunta de sim ou não! Ex: !poll \{Grêmio é maior que Inter?\}')
            return
        
        embed = discord.Embed(title=f'{question}', description='Reaja abaixo com :white_check_mark: SIM ou :no_entry: NÃO')
        embed.set_footer(text=f'Votação criada por {ctx.author.display_name}')
        message = await ctx.send(embed=embed)
        message.add_reaction('✅')
        message.add_reaction('  ')
    
    @tasks.loop(seconds=60)
    async def check_reminders(self):
        for i, reminder in enumerate(reminders_table):
            if reminder['time'].strptime("%Y-%m-%d %H:%M:%S") > datetime.datetime.now():
                reminder = reminders_table.pop(i)
                channel = self.bot.get_channel(reminder['channel_id'])
                user = self.bot.get_user(reminder['id'])
                if user is not None:
                    await channel.send(f'Lembrete para {user.mention}!\n{reminder["reminder"]}')

#* All working! (Just missing avatar in !sobre)
class Informations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.creator_id = 710164157235855491

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency, 0)}ms')

    @commands.command(aliases=['useravatar'])
    async def avatar(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author

        try:
            avatar_url = member.avatar.url
            await ctx.send(f'Avatar de {member.name}#{member.discriminator}')
            await ctx.send(avatar_url)
        except AttributeError:
            await ctx.send(f'Não foi possível exibir o avatar!', delete_after = 10)
            
    @commands.command(aliases=['ubanner'])
    async def userbanner(self, ctx, *, member: discord.Member = None):
        if member is None:
            member = ctx.author
            
        try:
            user = await self.bot.fetch_user(member.id)
            banner_url = user.banner
            await ctx.send(f'Banner de {member.name}#{member.discriminator}')
            await ctx.send(banner_url)
        except AttributeError:
            await ctx.send(f'Não foi possível exibir o banner!', delete_after = 10)

    @commands.command(aliases=['sbanner', 'gbanner', 'guildbanner'])
    async def serverbanner(self, ctx):
        try:
            banner_url = ctx.guild.banner.url
            await ctx.send(f'Banner de {ctx.guild.name}')
            await ctx.send(banner_url)
        except AttributeError:
            await ctx.send(f'Não foi possível exibir o banner desse servidor!', delete_after = 10)
               
    @commands.command(aliases=['icon'])
    async def servericon(self, ctx):
        try:
            icon_url = ctx.guild.icon.url
            await ctx.send(f'Ícone de {ctx.guild.name}')
            await ctx.send(icon_url)
        except AttributeError:
            await ctx.send(f'Não foi possível exibir o ícone desse servidor!', delete_after = 10)
            
    @commands.command(aliases=['uinfo', 'memberinfo'])
    async def userinfo(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        embed=discord.Embed(title=f"Informações sobre {member.nick if member.nick else member.name}", color=0x730075)
        embed.set_thumbnail(url=f"{member.avatar.url if member.avatar else member.default_avatar.url}")
        embed.add_field(name=":id: Discord ID", value=f"`{member.id}`", inline=True)
        embed.add_field(name=":label: Discord Tag", value=f"`{member.name}#{member.discriminator}`", inline=True)
        embed.add_field(name=":calendar: Data de criação", value=f"`{member.created_at.day:02d} de {meses[member.created_at.month]} de {member.created_at.year} às {member.created_at.hour:02d}:{member.created_at.minute:02d}`", inline=True)
        embed.add_field(name=":stopwatch: Data de entrada", value=f"`{member.joined_at.day:02d} de {meses[member.joined_at.month]} de {member.joined_at.year} às {member.joined_at.hour:02d}:{member.joined_at.minute:02d}`", inline=True)
        embed.add_field(name=":beginner: Cargo mais alto", value=f"{member.top_role.mention}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo', 'guildinfo', 'ginfo'])
    async def serverinfo(self, ctx, *, arg = None):
        if arg in ['cargos', 'roles']:
            embed=discord.Embed(title=f"informações sobre {ctx.guild.name}", color=0x982ab4)
            if ctx.guild.icon:
                embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
            embed.add_field(name=f":beginner: Lista de cargos:", value=f"{' '.join([role.mention for role in reversed(ctx.guild.roles) if role.name != '@everyone' and not role.managed])}")
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"Informações sobre {ctx.guild.name}", color=0x982ab4)
            if ctx.guild.icon:
                embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
            embed.add_field(name=f":id: Server ID", value=f"`{ctx.guild.id}`", inline=True)
            embed.add_field(name=f":crown: Dono(a)", value=f"`{ctx.guild.owner.name}#{ctx.guild.owner.discriminator}`\n({ctx.guild.owner.id})", inline=True)
            embed.add_field(name=f":calendar: Data de criação", value=f"`{ctx.guild.created_at.day:02d} de {meses[ctx.guild.created_at.month]} de {ctx.guild.created_at.year} às {ctx.guild.created_at.hour:02d}:{ctx.guild.created_at.minute:02d}`", inline=True)
            embed.add_field(name=f":star2: Entrei em", value=f"`{ctx.guild.me.joined_at.day:02d} de {meses[ctx.guild.me.joined_at.month]} de {ctx.guild.me.joined_at.year} às {ctx.guild.me.joined_at.hour:02d}:{ctx.guild.me.joined_at.minute:02d}`", inline=True)
            embed.add_field(name=f":speech_balloon: Canais ({len(ctx.guild.channels)})", value=f"**Texto: **{len(ctx.guild.text_channels)}\n**Voz: **{len(ctx.guild.voice_channels)}")
            embed.add_field(name=f":busts_in_silhouette: Membros ({ctx.guild.member_count})", value=f"**Online:** {sum(member.status == discord.Status.online for member in ctx.guild.members)}\n**Offline:** {ctx.guild.member_count-sum(member.status == discord.Status.online for member in ctx.guild.members)}", inline=True)
            embed.set_footer(text=f"Digite `!serverinfo cargos` para ver uma lista de cargos!")
            await ctx.send(embed=embed)

    @commands.command(aliases=['about'])
    async def sobre(self, ctx):
        creator_user = self.bot.get_user(self.creator_id)
        embed=discord.Embed(title="Bot da Gaby!")
        #embed.set_thumbnail(url="http")
        embed.add_field(name="Minha Twitch!", value="https://twitch.tv/gaby_ballejo", inline=False)
        embed.add_field(name="Criado por", value=f"https://github.com/eduardogott\nDC: {creator_user.name}#{creator_user.discriminator}", inline=False)
        embed.add_field(name="Latência", value=f"{round(self.bot.latency, 0)}ms")
        embed.add_field(name="Para mais informações", value="Digite `!help`", inline=False)
        await ctx.send(embed=embed)

#* All working!
class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    @commands.has_role('Mod')
    async def say(self, ctx, *, msg: str = None):
        if msg is None:
            await ctx.send('Escreva uma mensagem para mim anunciar!', delete_after = 5)
        else:
            await ctx.send(msg)
    
    @commands.command(aliases=['saye'])
    @commands.has_role('Admin')
    async def sayeveryone(self, ctx, *, msg: str = None):
        if msg is None:
            await ctx.send('Escreva uma mensagem para mim anunciar!', delete_after = 5)
        else:
            await ctx.send(f'{msg} ||@everyone||')
    
    @commands.command(aliases=['sayh'])
    @commands.has_role('Admin')
    async def sayhere(self, ctx, *, msg: str = None):
        if msg is None:
            await ctx.send('Escreva uma mensagem para mim anunciar!', delete_after = 5)
        else:
            await ctx.send(f'{msg} ||@here||')

async def setup(bot):
    await bot.add_cog(RNGs(bot))
    await bot.add_cog(Utils(bot))
    await bot.add_cog(Informations(bot))
    await bot.add_cog(Say(bot))