import discord
from discord.ext import commands
import asyncio
from tinydb import TinyDB, Query
import json

with open('config.json') as f:
    file = json.load(f)
    default_role = file['Configuration']['Roles']['AutoRole']['DefaultRole']

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
        self.registered = False

PlayerQuery = Query()

#* All working!
class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name=default_role)
        await member.add_roles(role)

#? All optimised!
class Register(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def confirmation_check(self, ctx, reaction, user, message):
        return user == ctx.author and str(reaction.emoji) == '✅' and reaction.message.id == message.id
    
    def gender_check(self, ctx, reaction, user, message):
        return user == ctx.author and str(reaction.emoji) in ['🔵','🔴','🟣'] and reaction.message.id == message.id
    
    def age_check(self, ctx, reaction, user, message):
        return user == ctx.author and str(reaction.emoji) in ['🍺','🔞'] and reaction.message.id == message.id

    @commands.command(aliases=['registro','registrar'])
    async def register(self, ctx):
        player = profiles_table.get(PlayerQuery.id == ctx.author.id)
        if player is None:
            player = Player(ctx.author.id)
            profiles_table.insert({'id': player.id, 'title': player.title, 'birthday': player.birthday, 'nickname': player.nickname, 'aboutme': player.aboutme, 'color': player.color, 'image': player.image, 'reps': player.reps, 'registered': player.registered})
            player = profiles_table.get(PlayerQuery.id == ctx.author.id)

        if player['registered'] is True:
            await ctx.send('Você já se registrou anteriormente! Caso queira alterar algo, abra ticket!')
            return
        
        message = await ctx.send('Iniciando registro\nAVISO: Você só pode se registrar uma vez, caso aconteça algum erro, abra ticket\nReaja com :white_check_mark: para confirmar que leu')
        message.add_reaction('✅')

        try:
            await self.wait_for('reaction', timeout=60, check=self.confirmation_check)
        except:
            await ctx('Você não confirmou seu registro!')
            message.delete()
            return

        player['registered'] = True

        message.edit(content = 'Qual seu gênero?\n:blue_circle: Masculino\n :red_circle: Feminino\n :purple_circle: Outro/NB')
        message.add_reaction('🔵')
        message.add_reaction('🔴')
        message.add_reaction('🟣')

        try:
            reaction = await self.wait_for('reaction', timeout=60, check=self.gender_check)
            if str(reaction.emoji) == '🔵':
                role = discord.utils.get(ctx.guild.roles, name="Masculino")
                ctx.author.add_roles(role)
            elif str(reaction.emoji) == '🔴':
                discord.utils.get(ctx.guild.roles, name="Feminino")
                ctx.author.add_roles(role)
            else:
                discord.utils.get(ctx.guild.roles, name="Outro/NB")
                ctx.author.add_roles(role)
        except asyncio.TimeoutError:
            await ctx.send('Tempo para resposta expirado!')
            message.delete()
            return

        message.clear_reactions()
        message.edit(content = 'Qual sua idade?\n:underage: -18\n :beer: +18')

        message.add_reaction('🔞')
        message.add_reaction('🍺')

        try:
            reaction = await self.wait_for('reaction', timeout=60, check=self.age_check)
            if str(reaction.emoji) == '🔞':
                role = discord.utils.get(ctx.guild.roles, name="-18")
                ctx.author.add_roles(role)
            else:
                role = discord.utils.get(ctx.guild.roles, name='+18')
                ctx.author.add_roles(role)
        except:
            await ctx.send('Tempo para resposta expirado!')
            message.delete()
            return
        
        await ctx.send(f'Registro concluido! {ctx.author.mention}')
        asyncio.sleep(10)
        message.delete()

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
    await bot.add_cog(Register(bot))