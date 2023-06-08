import discord
from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import re
import datetime
import operator
import heapq

meses = {'01': 'janeiro',
         '02': 'fevereiro',
         '03': 'março',
         '04': 'abril',
         '05': 'maio',
         '06': 'junho',
         '07': 'julho',
         '08': 'agosto',
         '09': 'setembro',
         '10': 'outubro',
         '11': 'novembro',
         '12': 'dezembro'}

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
profiles_table = db.table('profiles')

class Player():
    def __init__(self, player_id):
        self.id = player_id
        self.title = 'Perfil do usuário (!editar titulo)'
        self.birthday = '31-02'
        self.nickname = 'Apelido (!editar apelido)'
        self.aboutme = 'Digite `!editar sobremim` para editar esta parte!'
        self.color = '0xa80ca3'
        self.image = ''
        self.reps = 0

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
    async def edit(self, ctx, key: str = None, *, value = None):
        valid_keys = {'titulo': ('O título deve ter entre 5 e 48 caracteres!', (5, 48), 'title'),
                      'aniversario': ('O aniversário deve estar no formato `dd-mm`. Ex: `05-04` é 05 de abril.', self.birthday_pattern, 'birthday'),
                      'apelido': ('O apelido deve ter entre 2 e 48 caracteres!', (2, 48), 'nickname'),
                      'sobremim': ('O "sobre" deve ter entre 5 e 128 caracteres!', (5, 128), 'aboutme'),
                      'cor': ('Você deve colocar uma cor no formato hex! (#ffffff)', self.color_pattern, 'color'),
                      'imagem': ('A imagem deve estar no imgur, e com a URL `i.imgur.com/`', (self.social_pattern, self.social_url_pattern), 'image'),
                      'social': ('Insira sua rede social no formato `rede;url`. Ex: `twitter;https://twitter.com/eduardogottert`', (self.social_pattern, self.social_url_pattern), 'social')}
        
        if key in valid_keys:
            error_message, limits, db_entry = valid_keys[key]
            if value is not None:
                player = profiles_table.get(PlayerQuery.id == ctx.author.id)
                if player is None:
                    player = Player(ctx.author.id)
                    profiles_table.insert({'id': player.id, 'title': player.title, 'birthday': player.birthday, 'nickname': player.nickname, 'aboutme': player.aboutme, 'color': player.color, 'image': player.image, 'reps': player.reps})
                    player = profiles_table.get(PlayerQuery.id == ctx.author.id)

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

    @commands.command(aliases=['profile'])
    async def perfil(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        player = profiles_table.get(PlayerQuery.id == ctx.author.id)
        if player is None:
            await ctx.send(f'{member.display_name} não possui um perfil!')
            return

        embed=discord.Embed(title=f'Perfil de {member.display_name}', color=int(player['color'], 16))
        if player['image']:
            embed.set_thumbnail(url=player['image'])

        embed.add_field(name=':beginner: Título', value=player['title'], inline=False)
        embed.add_field(name=':label: Sobre mim', value=player['aboutme'], inline=False)
        embed.add_field(name=':pen_fountain: Apelido', value=player['nickname'], inline=False)

        birthday = player['birthday'].split('-')
        embed.add_field(name=':birthday: Aniversário', value=f'{birthday[0]} de {meses[str(birthday[1])]}', inline=False)
        embed.set_footer(text=f'ID do usuário {member.id}')
        await ctx.send(embed=embed)
    
    @commands.command()
    async def rep(self, ctx, member: discord.Member = None):
        player = profiles_table.get(PlayerQuery.id == ctx.author.id)
        if player is None:
            player = Player(ctx.author.id)
            profiles_table.insert({'id': player.id, 'title': player.title, 'birthday': player.birthday, 'nickname': player.nickname, 'aboutme': player.aboutme, 'color': player.color, 'image': player.image, 'reps': player.reps})
            player = profiles_table.get(PlayerQuery.id == ctx.author.id)
            return
        
        last_rep = player['last_rep'].strptime("%Y-%m-%d %H:%M:%S")
        if last_rep > datetime.datetime.now() - datetime.timedelta(hours=24):
            await ctx.send('Você ainda está em cooldown!')
            return
        
        if member is None:
            await ctx.send('Você deve mencionar um membro! (!rep \{membro\})')
            return
        
        if member == ctx.author:
            await ctx.send('Você não pode dar !rep em si mesmo!')
            return
        
        player = profiles_table.get(PlayerQuery.id == member.id)
        if player is None:
            player = Player(member.id)
            profiles_table.insert({'id': player.id, 'title': player.title, 'birthday': player.birthday, 'nickname': player.nickname, 'aboutme': player.aboutme, 'color': player.color, 'image': player.image, 'reps': player.reps})
            player = profiles_table.get(PlayerQuery.id == member.id)
        
        player['reps'] += 1
        profiles_table.update(player, PlayerQuery.id == member.id)
 
        player_author = profiles_table.get(PlayerQuery.id == ctx.author.id)
        player_author['last_rep'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        profiles_table.update(player_author, PlayerQuery.id == ctx.author.id)
        
        await ctx.send(f'Você deu +rep em {member.mention}! Agora ele(a) tem {player["reps"]} reps!')

#* All working!
class BirthdayAnnouncer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_birthdays.start()
        self.birthdays_channel = 1107132277328191600

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

async def setup(bot):
    await bot.add_cog(ProfileEdit(bot))
    await bot.add_cog(ProfileCommands(bot))
    await bot.add_cog(BirthdayAnnouncer(bot))