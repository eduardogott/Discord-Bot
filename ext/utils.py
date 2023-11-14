'''UTIL COMMANDS EXTENSION

Commands included: [] = Optional, {} = Required, () = Choose one of, required, <> = Choose one of, optional
Commands preceded by @ are Manager only

random [min] [max] - Generates a random number, defaults to 1-100, limited to -1000000000-1000000000
dado [size] - Rolls a dice, defaults to 6, max size is 4096
jankenpon (pedra/papel/tesoura) - Plays rock paper scissors vs the bot
escolher {options} - Chooses one of the items in "options", must be more than two items separated by comma
shorten {url} - Shortens a URL using TinyURL's API, cooldown of 60 seconds
remindme {time(s/m/h/d/w/mo/y)} {message} - Creates a reminder to be reminded in an embed after the chosen time
@poll {question} - Creates an embed poll with ✅ and ❌ reactions
ping - Reply the bot's ping (used to test if the bot is online)
avatar [@member] - Shows the member's avatar
userbanner [@member] - Shows the member's banner
serverbanner - Shows the guild's banner
servericon - Shows the guild's icon
userinfo [@member] - Displays informations about an member
serverinfo <cargos> - Displays informations about the guild, or the roles if <guild> is used
@say {message} - Sends a message as the bot (placeholders: %e = @everyone, %h = @here, %a = @command_author)

Aliases are listed in ../aliases.md'''


import discord
import random as rd
from discord.ext import commands, tasks
import requests
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import asyncio
from ._util_funcs import time_convert, time_input_convert, role_handler, meses

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
reminders_table = db.table('reminders')

class Reminder():
    def __init__(self, player_id, now, time, channel_id, text):
        self.id = player_id
        self.creation_date = now
        self.time = time
        self.channel_id = channel_id
        self.reminder = text

ReminderQuery = Query()

#* All working!
class RNGs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.choice_emojis = {'papel':':newspaper:',
                              'pedra':':rock:',
                              'tesoura':':scissors:'}
        
    @commands.command()
    async def random(self, ctx, minimum: int = 1, maximum: int = 100):
        if minimum > maximum:
            minimum, maximum = maximum, minimum # Invert the values if minimum is greater than maximum
        
        maximum = min(maximum, 1000000000) # Remove absurdly high numbers
        minimum = max(minimum, -1000000000) # Remove absurdly low numbers

        x = rd.randint(minimum, maximum)
        await ctx.send(f'Sorteando um número entre {minimum} e {maximum}... O número sorteado é: {x}')

    @commands.command(aliases=['dice'])
    async def dado(self, ctx, maximum: int = 6):
        if maximum < 2:
            await ctx.send('O dado precisa ter no mínimo 2 lados!')
            return
        
        maximum = min(maximum, 4096) # Remove absurdly big dices
        x = rd.randint(1, maximum)
        await ctx.send(f'Rolando um D{maximum}... O resultado é {x}!')
                  
    @commands.command(aliases=['ppt', 'rps', 'rockpaperscissors', 'pedrapapeltesoura', 'jokenpo'])
    async def jankenpon(self, ctx, user_choice: str | None = None):
        if user_choice not in ['pedra', 'papel', 'tesoura']:
            await ctx.send('Você deve escolher `pedra`, `papel` ou `tesoura`!')
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
    async def escolher(self, ctx, *, args = ''):
        args.replace(', ', ',') # Remove trailing spaces after the comma
        args = args.split(',') # Split all items to a list

        if len(args) <= 1:
            await ctx.send('Insira pelo menos 2 ítens para eu escolher, separados por vírgula!')
        else:
            x = rd.choice(args)
            await ctx.send(f'Eu escolho {x}!')

#? All optimised!
class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.default_reminders_channel = 1107132277328191600
        self.tinyurl_api = 'https://tinyurl.com/api-create.php?url='
        self.check_reminders.start()

    @commands.command(aliases=['short', 'shorturl', 'bitly', 'tinyurl'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def shorten(self, ctx, url: str | None = None):
        if url is None:
            await ctx.send('Você não forneceu uma URL para encurtar!')
            return
        
        try:
            response = requests.get(self.tinyurl_api + url)
            if response.status_code == 200:
                await ctx.send(f'URL encurtada: {response.text}')
            else:
                await ctx.send(f'Não foi possível encurtar a URL `{url}`.')

        except requests.exceptions.RequestException:
            await ctx.send(f'Não foi possível encurtar a URL `{url}`.')

    @commands.command(aliases=['lembrete', 'reminder'])
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def remindme(self, ctx, _time: str = '', *, message: str = ''):
        if not _time:
            await ctx.send('Você não inseriu uma duração válida! (Insira no formato [número](s/m/h/d/w/mo/y))')
            return
        
        time = time_input_convert(_time)
        if time == -1:
            await ctx.send('Duração inválida! (Insira no formato [número](s/m/h/d/w/mo/y))')
            return

        if not message:
            await ctx.send('Você não inseriu um lembrete válido! (Use: !remindme {tempo} {lembrete})')
            return
        
        db_now = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        db_time = (datetime.now() + timedelta(seconds=time)).strftime("%Y-%m-%d %H:%M:%S")
        reminder = Reminder(ctx.author.id, db_now, db_time, ctx.channel.id, message)

        reminders_table.insert({'id':reminder.id,'creation_date':reminder.creation_date,'time':reminder.time,
                                'channel_id':reminder.channel_id,'reminder':reminder.reminder})
        
        await ctx.send('Lembrete criado com sucesso!')
   
    @shorten.error
    async def shorten_error(self, ctx, e):
        if isinstance(e, commands.CommandOnCooldown):
            remaining = round(e.retry_after)
            await ctx.send(f'Este comando está em cooldown! Aguarde {time_convert(remaining)} e tente novamente!')

    @remindme.error
    async def remindme_error(self, ctx, e):
        if isinstance(e, commands.CommandOnCooldown):
            remaining = round(e.retry_after)
            await ctx.send(f'Este comando está em cooldown! Aguarde {time_convert(remaining)} e tente novamente!')

    @commands.command(aliases=['votacao'])
    async def poll(self, ctx, *, question: str = ''):
        if await role_handler(ctx, 'Manager') is False: return

        if not question:
            await ctx.send('Você não inseriu uma pergunta válida! (Use: !poll {pergunta})')
            return

        embed = discord.Embed(title=f'{question}', description='Reaja abaixo com :white_check_mark: SIM ou :x: NÃO')
        embed.set_footer(text=f'Votação criada por {ctx.author.display_name}')
        message = await ctx.send(embed=embed)
        await message.add_reaction('✅')
        await message.add_reaction('❌')

    @tasks.loop(seconds=10)
    async def check_reminders(self):
        for reminder in reminders_table:
            if datetime.strptime(reminder['time'], "%Y-%m-%d %H:%M:%S") < datetime.now():
                try:
                    channel = self.bot.get_channel(reminder['channel_id'])
                except commands.ChannelNotFound:
                    channel = self.bot.get_channel(self.default_reminders_channel)
                
                user = self.bot.get_user(reminder['id'])
                if user is not None:
                    embed = discord.Embed(title=f'Lembrete para {user.display_name}', description=reminder['reminder'], 
                                          color=0x982ab4)
                    
                    embed.set_footer(text=f'Lembrete criado em: {reminder["creation_date"]}')
                    
                    await channel.send(f'{user.mention}', embed=embed)

                reminders_table.remove(ReminderQuery.id == reminder['id'] 
                                       and ReminderQuery.reminder == reminder['reminder'])

#* All working! (Just missing avatar in !sobre)
class Informations(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.creator_id = 710164157235855491

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.bot.latency, 0)}ms')

    @commands.command(aliases=['useravatar'])
    async def avatar(self, ctx, *, member: discord.Member | None  = None):
        if member is None:
            member = ctx.author

        avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
        discriminator = f'#{member.discriminator}' if int(member.discriminator) else ''
        await ctx.send(f'Avatar de {member.display_name}{discriminator}')
        await ctx.send(avatar_url)
            
    @commands.command(aliases=['ubanner'])
    async def userbanner(self, ctx, *, member: discord.Member | None = None):
        if not isinstance(member, discord.Member):
            member = ctx.author

        user = await self.bot.fetch_user(member.id)
        if user.banner:
            banner_url = user.banner
            discriminator = f'#{member.discriminator}' if int(member.discriminator) else ''
            await ctx.send(f'Banner de {member.name}{discriminator}')
            await ctx.send(banner_url)
        else:
            await ctx.send('Este membro não possui um banner!')

    @commands.command(aliases=['sbanner', 'gbanner', 'guildbanner'])
    async def serverbanner(self, ctx):
        if ctx.guild.banner:
            banner_url = ctx.guild.banner.url
            await ctx.send(f'Banner de {ctx.guild.name}')
            await ctx.send(banner_url)
        else:
            await ctx.send('Este servidor não possui um banner!')
               
    @commands.command(aliases=['icon'])
    async def servericon(self, ctx):
            if ctx.guild.icon:
                icon_url = ctx.guild.icon.url
                await ctx.send(f'Ícone de {ctx.guild.name}')
                await ctx.send(icon_url)
            else:
                await ctx.send('Este servidor não possui um ícone!')
            
    @commands.command(aliases=['uinfo', 'memberinfo'])
    async def userinfo(self, ctx, member: discord.Member | None = None):
        if not isinstance(member, discord.Member):
            member = ctx.author

        info = {'display_name': member.display_name,
                'avatar': member.avatar.url if member.avatar else member.default_avatar.url,
                'id': member.id, 
                'name':f'{member.name}',
                'discriminator': f'#{member.discriminator}' if int(member.discriminator) else '',
                'creation': {'d': f'{member.created_at.day:02d}',
                             'm': f'{meses[member.created_at.month]}',
                             'y': f'{member.created_at.year:02d}', 
                             'hh': f'{member.created_at.hour:02d}',
                             'mm':f'{member.created_at.minute:02d}', 
                             'ss': f'{member.created_at.second:02d}'},
                'highest_role': member.top_role.mention}
        
        if isinstance(member.joined_at, datetime):
            info['entry'] = {'d': f'{member.joined_at.day:02d}', 
                             'm': f'{meses[member.joined_at.month]}',
                             'y': f'{member.joined_at.year:02d}', 
                             'hh': f'{member.joined_at.hour:02d}',
                             'mm':f'{member.joined_at.minute:02d}', 
                             'ss': f'{member.joined_at.second:02d}'}
        else:
            info['entry'] = None

        embed=discord.Embed(title=f"Informações sobre {info['display_name']}", color=0x730075)
        embed.set_thumbnail(url=info['avatar'])
        embed.add_field(name=":id: Discord ID", value=f"`{info['id']}`", inline=True)
        embed.add_field(name=":label: Discord Tag", value=f"`{info['name']}{info['discriminator']}`", inline=True)
        embed.add_field(name=":calendar: Data de criação", value=f"`{info['creation']['d']} de {info['creation']['m']} de {info['creation']['y']} às {info['creation']['hh']}:{info['creation']['mm']}:{info['creation']['ss']}`", inline=True)
        embed.add_field(name=":stopwatch: Data de entrada", value=f"`{info['entry']['d']} de {info['entry']['m']} de {info['entry']['y']} às {info['entry']['hh']}:{info['entry']['mm']}:{info['entry']['ss']}`" if info['entry'] else 'Informação indisponível!', inline=True)
        embed.add_field(name=":beginner: Cargo mais alto", value=f"{info['highest_role']}", inline=True)
        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo', 'guildinfo', 'ginfo'])
    async def serverinfo(self, ctx, *, arg: str = ''):
        if arg in ['cargos', 'roles']:
            embed=discord.Embed(title=f"Informações sobre {ctx.guild.name}", color=0x982ab4)
            embed.set_thumbnail(url=f"{ctx.guild.icon.url if ctx.guild.icon else ctx.author.default_avatar.url} ")
            embed.add_field(name=f":beginner: Lista de cargos:", value=f"{', '.join([role.mention for role in reversed(ctx.guild.roles) if role.name != '@everyone' and not role.managed])}")
            await ctx.send(embed=embed)
        else:
            info = {'name': ctx.guild.name,
                    'thumbnail': ctx.guild.icon.url if ctx.guild.icon else ctx.author.default_avatar.url,
                    'id': ctx.guild.id,
                    'owner': {'name': ctx.guild.owner.name, 
                              'disc': f'#{ctx.guild.owner.discriminator}' if int(ctx.guild.owner.discriminator) else '',
                              'id': ctx.guild.owner.id},
                    'creation': {'d': f'{ctx.guild.created_at.day:02d}', 
                                 'm': f'{meses[ctx.guild.created_at.month]}',
                                 'y': f'{ctx.guild.created_at.year:02d}', 
                                 'hh': f'{ctx.guild.created_at.hour:02d}',
                                 'mm':f'{ctx.guild.created_at.minute:02d}', 
                                 'ss': f'{ctx.guild.created_at.second:02d}'},
                    'joined': {'d': f'{ctx.guild.me.joined_at.day:02d}', 
                               'm': f'{meses[ctx.guild.me.joined_at.month]}',
                               'y': f'{ctx.guild.me.joined_at.year:02d}', 
                               'hh': f'{ctx.guild.me.joined_at.hour:02d}',
                               'mm':f'{ctx.guild.me.joined_at.minute:02d}', 
                               'ss': f'{ctx.guild.me.joined_at.second:02d}'},
                    'channels': {'total': len(ctx.guild.channels),
                                 'text': len(ctx.guild.text_channels),
                                 'voice': len(ctx.guild.voice_channels)},
                    'members': {'total': ctx.guild.member_count,
                                'online': sum(member.status == discord.Status.online for member in ctx.guild.members),
                                'offline': ctx.guild.member_count - sum(member.status == discord.Status.online 
                                                                        for member in ctx.guild.members)}}
            
            embed=discord.Embed(title=f"Informações sobre {info['name']}", color=0x982ab4)
            embed.set_thumbnail(url=info['thumbnail'])
            embed.add_field(name=f":id: Server ID", value=f"`{info['id']}`", inline=True)
            embed.add_field(name=f":crown: Dono(a)", value=f"`{info['owner']['name']}{info['owner']['disc']}`\n`({info['owner']['id']})`", inline=True)
            embed.add_field(name=f":calendar: Data de criação", value=f"`{info['creation']['d']} de {info['creation']['m']} de {info['creation']['y']} às {info['creation']['hh']}:{info['creation']['mm']}:{info['creation']['ss']}`", inline=True)
            embed.add_field(name=f":star2: Entrei em", value=f"`{info['joined']['d']} de {info['joined']['m']} de {info['joined']['y']} às {info['joined']['hh']}:{info['joined']['mm']}:{info['joined']['ss']}`", inline=True)
            embed.add_field(name=f":speech_balloon: Canais ({info['channels']['total']})", value=f"**Texto: **{info['channels']['text']}\n**Voz: **{info['channels']['voice']}")
            embed.add_field(name=f":busts_in_silhouette: Membros ({info['members']['total']})", value=f"**Online:** {info['members']['online']}\n**Offline:** {info['members']['offline']}", inline=True)
            embed.set_footer(text=f"Digite `!serverinfo cargos` para ver uma lista de cargos!")
            await ctx.send(embed=embed)

#* All working!
class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def say(self, ctx, *msg):
        placeholders = {'%everyone%': '@everyone', '%e': '@everyone', '%here%': '@here', '%h': '@here',
                        '%author%': ctx.author.mention, '%a': ctx.author.mention}
        if await role_handler(ctx, 'Manager', 'Mod') is False: return

        if not msg:
            await ctx.send('Escreva uma mensagem para mim anunciar!', delete_after = 15)
            return
        
        channel = discord.utils.get(ctx.guild.channels, mention=msg[0]) # Tries to get it by ID

        if channel:
            msg = ' '.join(msg[1:]) # If there were matches above, remove the channel from the message

        else:
            channel = ctx.channel
            msg = ' '.join(msg)

        for item in placeholders:
            msg = msg.replace(item, placeholders[item])

        await channel.send(msg)

async def setup(bot):
    await bot.add_cog(RNGs(bot))
    await bot.add_cog(Utils(bot))
    await bot.add_cog(Informations(bot))
    await bot.add_cog(Say(bot))