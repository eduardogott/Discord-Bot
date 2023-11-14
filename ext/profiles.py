import discord
from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import re
import datetime
import operator
import heapq
import json
from _util_funcs import meses, role_handler

BIRTHDAYS_CHANNEL: int = 1107132277328191600 # Discord channel ID in which birthdays will be announced 
DEFAULTS = {'Title': 'User profile (!edit titulo)',
            'Birthday': '31-02',
            'Nickname': 'Nickname (!edit apelido)',
            'AboutMe': 'Type `!edit sobremim` to edit this!',
            'Color': '0xa80ca3',
            'Image': 'https://i.imgur.com/aaa.gif',
            'Social': ''} # Default values for items in profile
SIZE_LIMITS = {'Title': [5, 48], 'Nickname': [2, 48], 'AboutMe': [5,128]} # Minimum and maximum size for some entries


db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
profiles_table = db.table('profiles')

def get_player(member):
    player = profiles_table.get(PlayerQuery.id == member.id)
    if player is None:
        _player = Player(member.id)
        profiles_table.insert({'id': _player.id, 'title': _player.title, 'birthday': _player.birthday, 'nickname': _player.nickname, 'aboutme': _player.aboutme, 'color': _player.color, 'image': _player.image, 'reps': _player.reps, 'registered': _player.registered})
    
    return profiles_table.get(PlayerQuery.id == member.id)

class Player():
    def __init__(self, player_id):
        self.id = player_id
        self.title = DEFAULTS['Title']
        self.birthday = DEFAULTS['Birthday']
        self.nickname = DEFAULTS['Nickname']
        self.aboutme = DEFAULTS['AboutMe']
        self.color = DEFAULTS['Color']
        self.image = DEFAULTS['Image']
        self.social = DEFAULTS['Social']
        self.reps = 0
        self.registered = False

PlayerQuery = Query()

#! Implement socials in !edit
class ProfileEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_pattern = r'\b^(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])$\b'
        self.color_pattern = r'^\#[0-9a-f]{6}$'
        self.image_pattern = r'^\bhttps?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.(?:jpg|jpeg|png|gif|bmp)$\b'
        self.social_pattern = r'^(?i)(?:twitter|youtube|reddit|tiktok|instagram|github|facebook|twitch)$'
        self.social_url_pattern = r'^(?i)https?\:\/\/(?:twitter|youtube|reddit|tiktok|instagram|github|facebook|twitch)\.com(\.br)?\/[.]$'

    @commands.command(aliases=['editar', 'editprofile', 'editperfil'])
    async def edit(self, ctx, key: str = '', *, value = None):
        valid_keys = {'titulo': ('O título deve ter entre 5 e 48 caracteres!', (SIZE_LIMITS['Title'][0], SIZE_LIMITS['Title'][1]), 'title'),
                      'aniversario': ('O aniversário deve estar no formato `dd-mm`. Ex: `05-04` é 05 de abril.', self.birthday_pattern, 'birthday'),
                      'apelido': ('O apelido deve ter entre 2 e 48 caracteres!', (SIZE_LIMITS['Nickname'][0], SIZE_LIMITS['Nickname'][1]), 'nickname'),
                      'sobremim': ('O "sobre" deve ter entre 5 e 128 caracteres!', (SIZE_LIMITS['AboutMe'][0], SIZE_LIMITS['AboutMe'][1]), 'aboutme'),
                      'cor': ('Você deve colocar uma cor no formato hex e em minúsculo! (#ffffff)', self.color_pattern, 'color'),
                      'imagem': ('A imagem deve estar no imgur, e com a URL `i.imgur.com/`', (self.social_pattern, self.social_url_pattern), 'image'),
                      'social': ('Insira sua rede social no formato `rede;url`. Ex: `twitter;https://twitter.com/eduardogottert`', (self.social_pattern, self.social_url_pattern), 'social')}
        
        if key in valid_keys:
            error_message, limits, db_entry = valid_keys[key]
            if value is not None:
                player = get_player(ctx.author)

                if key in ['titulo', 'apelido', 'sobremim']:
                    if limits[0] <= len(value) <= limits[1]:
                        player[db_entry] = value
                        profiles_table.update(player, PlayerQuery.id == player['id'])
                    else:
                        await ctx.send(f'{error_message}')

                elif key in ['aniversario', 'cor', 'imagem']:
                    if re.match(limits, value):
                        player[db_entry] = value
                        profiles_table.update(player, PlayerQuery.id == player['id'])
                    else:
                        await ctx.send(f'{error_message}')
                        
            else:
                await ctx.send('Você deve inserir um valor! (Ex: !editar \{titulo\} \{Perfil do Hyper\})')
        else:
            await ctx.send('Opções: `titulo, aniversario, apelido, sobremim, cor, imagem, social`')          

#*All working!
class ProfileCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['perfil'])
    async def profile(self, ctx, member: discord.Member | None = None):
        if not isinstance(member, discord.Member):
            member = ctx.author

        player = get_player(member)

        embed=discord.Embed(title=f'Perfil de {member.display_name}', color=int(player['color'], 16))
        if player['image']:
            embed.set_thumbnail(url=player['image'])

        embed.add_field(name=':beginner: Título', value=player['title'], inline=False)
        embed.add_field(name=':label: Sobre mim', value=player['aboutme'], inline=False)
        embed.add_field(name=':pen_fountain: Apelido', value=player['nickname'], inline=False)

        birthday = player['birthday'].split('-')
        embed.add_field(name=':birthday: Aniversário', value=f'{birthday[0]} de {meses[int(birthday[1])]}', inline=False)
        embed.set_footer(text=f'ID do usuário {member.id}')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rep(self, ctx, member: discord.Member | None = None):
        repping_player = get_player(ctx.author)

        last_rep = repping_player['last_rep'].strptime("%Y-%m-%d %H:%M:%S")
        if last_rep > datetime.datetime.now() - datetime.timedelta(hours=24):
            await ctx.send('Você ainda está em cooldown!')
            return
        
        if not isinstance(member, discord.Member):
            await ctx.send('Você deve mencionar um membro! (!rep \{membro\})')
            return
        
        if member == ctx.author:
            await ctx.send('Você não pode dar !rep em si mesmo!')
            return
        
        repped_player = get_player(member)
        
        repped_player['reps'] += 1
        profiles_table.update(repped_player, PlayerQuery.id == member.id)

        repping_player['last_rep'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        profiles_table.update(repping_player, PlayerQuery.id == ctx.author.id)
        
        await ctx.send(f'Você deu +rep em {member.mention}! Agora ele(a) tem {repped_player["reps"]} reps!')

#* All working!
class BirthdayAnnouncer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()

    time = datetime.time(hour=13, minute=00)

    @tasks.loop(time=time)
    async def check_birthdays(self):
        today = datetime.datetime.today().strftime('%d-%m')
        for user in profiles_table:
            if user['birthday'] == today:
                channel = self.bot.get_channel(self.birthdays_channel)
                member = self.bot.fetch_user(user['id'])
                await channel.send(f'Feliz aniversário {member.mention}!')

    @commands.command(aliases=['aniversarios'])
    async def nextbirthdays(self, ctx):
        birthdays = []
        today = datetime.datetime.today()
        for user in profiles_table:
            if user['birthday'] != '31-02':
                birthday_date = datetime.datetime.strptime(user['birthday'], '%d-%m')
                birthdays.append([user['id'], birthday_date])

        for i, birthday in enumerate(birthdays):
            next_birthday = datetime.datetime(today.year, birthday[1].month, birthday[1].day)
            if next_birthday < today:
                next_birthday = datetime.datetime(today.year + 1, birthday[1].month, birthday[1].day)
            birthdays[i][1] = next_birthday

        next_10_birthdays = heapq.nsmallest(10, birthdays, key=lambda x: x[1])
        user_ids = [birthday[0] for birthday in next_10_birthdays]
        members = await self.bot.fetch_users(*user_ids)

        birthday_message = '\n'.join(f'{i}. {member.display_name} - {birthday[1].strftime("%d-%m")}' for i, (member, birthday) in enumerate(zip(members, next_10_birthdays)))
        
        embed = discord.Embed(title='Próximos 10 aniversários', description=birthday_message, color=0xc514b6)
        await ctx.send(embed=embed)

#? All optimised!
class AdminProfileEdit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.birthday_pattern = r'\b^(0[1-9]|[1-2][0-9]|3[0-1])-(0[1-9]|1[0-2])$\b'
        self.color_pattern = r'^\#[0-9a-f]{6}$'
        self.image_pattern = r'^\bhttps?:\/\/i\.imgur\.com\/[a-zA-Z0-9]+\.(?:jpg|jpeg|png|gif|bmp)$\b'
        self.social_pattern = r'^(?i)(?:twitter|youtube|reddit|tiktok|instagram|github|facebook|twitch)$'
        self.social_url_pattern = r'^(?i)https?\:\/\/(?:twitter|youtube|reddit|tiktok|instagram|github|facebook|twitch)\.com(\.br)?\/[.]$'

    @commands.command(aliases=['editar', 'editprofile', 'editperfil'])
    async def adminedit(self, ctx, member: discord.Member | None = None, key: str = '', *, value = None):
        if role_handler(ctx, 'Manager') is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Você deve inserir um membro. Ex: !adminedit @Edu titulo TituloExemplo')
            return
        
        valid_keys = {'titulo': ('O título deve ter entre 5 e 48 caracteres!', (SIZE_LIMITS['Title'][0], SIZE_LIMITS['Title'][1]), 'title'),
                      'aniversario': ('O aniversário deve estar no formato `dd-mm`. Ex: `05-04` é 05 de abril.', self.birthday_pattern, 'birthday'),
                      'apelido': ('O apelido deve ter entre 2 e 48 caracteres!', (SIZE_LIMITS['Nickname'][0], SIZE_LIMITS['Nickname'][1]), 'nickname'),
                      'sobremim': ('O "sobre" deve ter entre 5 e 128 caracteres!', (SIZE_LIMITS['AboutMe'][0], SIZE_LIMITS['AboutMe'][1]), 'aboutme'),
                      'cor': ('Você deve colocar uma cor no formato hex e em minúsculo! (#ffffff)', self.color_pattern, 'color'),
                      'imagem': ('A imagem deve estar no imgur, e com a URL `i.imgur.com/`', (self.social_pattern, self.social_url_pattern), 'image'),
                      'social': ('Insira sua rede social no formato `rede;url`. Ex: `twitter;https://twitter.com/eduardogottert`', (self.social_pattern, self.social_url_pattern), 'social')}
        
        if key in valid_keys:
            error_message, limits, db_entry = valid_keys[key]
            if value is not None:
                player = get_player(member)

                if key in ['titulo', 'apelido', 'sobremim']:
                    if limits[0] <= len(value) <= limits[1]:
                        player[db_entry] = value
                        profiles_table.update(player, PlayerQuery.id == player['id'])
                    else:
                        await ctx.send(f'{error_message}')

                elif key in ['aniversario', 'cor', 'imagem']:
                    if re.match(limits, value):
                        player[db_entry] = value
                        profiles_table.update(player, PlayerQuery.id == player['id'])
                    else:
                        await ctx.send(f'{error_message}')
                        
            else:
                await ctx.send('Você deve inserir um valor! (Ex: !editar \{titulo\} \{Perfil do Hyper\})')
        else:
            await ctx.send('Opções: `titulo, aniversario, apelido, sobremim, cor, imagem, social`')          

async def setup(bot):
    await bot.add_cog(ProfileEdit(bot))
    await bot.add_cog(ProfileCommands(bot))
    await bot.add_cog(BirthdayAnnouncer(bot))