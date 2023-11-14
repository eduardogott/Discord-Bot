import discord
import datetime
import re
from tinydb import TinyDB, Query
from discord.ext import commands, tasks
import json
from ._util_funcs import time_convert, time_input_convert, role_handler, permissions_handler


PUNISHMENTS_CHANNEL: int = 1107130913948696600 # Discord channel ID in which punishments will be announced
WARNINGS_EXPIRATION: int = 30 # Days in which warnings will expire
AUTO_PUNISHMENTS: dict = {"2": "timeout %member% 7d Reached 2 warnings",
                                    "4": "timeout %member% 30d Reached 4 warnings",
                                    "6": "ban %member% Reached 6 warnings"} # Warning auto-punishments actions
                                    # Valid punishments: 'ban', 'timeout', 'kick'
                                    # Format: [punishment] %member% [length if appliable] [reason] 
                                    # The %member% placeholder is MANDATORY

AUTOMOD_MINIMUM_LENGTH: int = 10 # Minimum message length to be analysed by the automod
AUTOMOD_FLOOD_AMOUNT: int = 3 # Amount of identical messages to be flagged as flood (exclusive ex: if 3, then will be flagged after the 4th message)
AUTOMOD_MAX_MENTIONS: int = 2 # Maximum mentions for the automod not to flag (exclusive ex: will only flag when maxmentions + 1)

class WarningActions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def process(self, ctx, args, member):
        msg = args.split(' ')

        if msg[0] == 'timeout' or msg[0] == 'mute':
            member = msg[1].replace('%member%', member)
            duration = msg[2]
            reason = msg[3:]
            self.timeout(ctx, member, duration, reason)
            return
        
        if msg[0] == 'ban':
            member = msg[1].replace('%member%', member)
            reason = msg[2:]
            self.ban(ctx, member, reason)
            return
        
        if msg[0] == 'kick':
            member = msg[1].replace('%member%', member)
            reason = msg[2:]
            self.kick(ctx, member, reason)
            return

    async def timeout(self, ctx, member, duration, *, reason):
        length = datetime.datetime.now().astimezone() + datetime.timedelta(seconds=time_input_convert(duration))
        await member.timeout(length, reason = reason)
        await ctx.send(f'{member.mention} foi silenciado! Motivo: {reason}')
        player = punishments_table.get(PlayerQuery.id == member.id)
        player['user_punishments'].append({'type':'timeout','reason':reason,'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'length':length.strftime("%Y-%m-%d %H:%M:%S")})
        punishments_table.update(player, PlayerQuery.id == member.id)
        return
    
    async def ban(self, ctx, member, *, reason):
        await member.ban(reason = reason)
        await ctx.send(f'{member.mention} foi banido! Motivo: {reason}')
        player = punishments_table.get(PlayerQuery.id == member.id)
        player['user_punishments'].append({'type':'ban','reason':reason,'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'removed':False})
        punishments_table.update(player, PlayerQuery.id == member.id)
        return
    
    async def kick(self, ctx, member, *, reason):
        await member.kick(reason = reason)
        await ctx.send(f'{member.mention} foi expulso! Motivo: {reason}')
        player = punishments_table.get(PlayerQuery.id == member.id)
        player['user_punishments'].append({'type':'kick','reason':reason,'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'removed':False})
        punishments_table.update(player, PlayerQuery.id == member.id)
        return

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
punishments_table = db.table('punishments')

def get_player(member):
    player = punishments_table.get(PlayerQuery.id == member.id)
    if player is None:
        _player = Player(member.id)
        punishments_table.insert({'id': _player.id, 'user_punishments': _player.user_punishments, 'warnings': _player.warnings})
        
    return punishments_table.get(PlayerQuery.id == member.id)

class Player():
    def __init__(self, player_id):
        self.id = player_id
        self.user_punishments = []
        self.warnings = []

PlayerQuery = Query()

#? All optimised!
class Punishments(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ticketban(self, ctx, member: discord.Member | None = None, *, reason: str = ''):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Você deve especificar um membro para ser banido dos tickets!', delete_after = 10)
            return
        
        try:
            player = get_player(member)
            
            for punishment in player['user_punishments']:
                if punishment['type'] == 'ticket-ban' and punishment['removed'] is False:
                    await ctx.send('O membro já possui um ticket-ban ativo!')
                    return

            currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
            player['user_punishments'].append({'type':'ticket-ban','reason':reason,'time':currtime,'removed':False,'author':ctx.author.id})
            punishments_table.update(player, PlayerQuery.id == member.id)
            
            await ctx.send(f'Baniu {member.mention} ({member.id}) de criar tickets!')

        except Exception:
            await ctx.send('Não foi possível banir dos tickets!')
    
    @commands.command()
    async def unticketban(self, ctx, member: discord.Member | None = None):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager']) is False: return
        
        if not isinstance(member, discord.Member):
            await ctx.send('Você deve especificar um membro para ser desbanido dos tickets!', delete_after = 10)
            return
        
        try:
            player = get_player(member)
   
            for punishment in player['user_punishments']:
                if punishment['type'] == 'ticket-ban' and punishment['removed'] == False:
                    player['user_punishments'][punishment]['removed'] = True
                    player['user_punishments'][punishment]['removed_by'] = ctx.author.id
                    break
            else:
                await ctx.send('Este membro não está banido de criar tickets!')
                return
            
            punishments_table.update(player, PlayerQuery.id == member.id)
            await ctx.send(f'Desbaniu {member.mention} ({member.id}) de criar tickets!')
        
        except Exception:
            await ctx.send('Não foi possível desbanir dos tickets!')

    @commands.command()
    async def ban(self, ctx, member: discord.Member | None = None, *, reason: str = ''):
        if permissions_handler(ctx, 'ban_members', exempt_roles=['Manager']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Você deve especificar um membro para ser banido!', delete_after = 10)
            return
        
        try:
            await member.ban(reason = reason)

            player = get_player(member)

            currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")    
            player['user_punishments'].append({'type':'ban','reason':reason,'time':currtime,'removed':False,'author':ctx.author.id})
            punishments_table.update(player, PlayerQuery.id == member.id)

            embed=discord.Embed(title=f"{member.display_name} foi banido!", color=0xff0000)
            embed.add_field(name="Banido por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
            embed.add_field(name="Motivo", value=f"{reason}", inline=True)
            embed.set_footer(text=f"ID do usuário: {member.id}")
            channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
            await channel.send(embed=embed)
            await ctx.send(f'Baniu {member.mention} ({member.id})')

        except Exception:
            await ctx.send('Não foi possivel banir!')

    @commands.command()
    async def unban(self, ctx, *, member_id = None):
        if permissions_handler(ctx, 'ban_members', exempt_roles=['Manager']) is False: return
        
        if not isinstance(member, discord.Member):
            await ctx.send('Você deve especificar um membro para ser desbanido (Discord ID)!', delete_after = 10)
            return
        if re.match(r'[0-9]{17,18}', member):
            try:
                member = await self.bot.fetch_user(member_id)
                await ctx.guild.unban(member)
                await ctx.send(f'Desbaniu {member.mention}')
                player = get_player(member)
                player['user_punishments'][-1]['removed'] = True
                player['user_punishments'][-1]['removed_by'] = ctx.author.id
                punishments_table.update(player, PlayerQuery.id == member.id)
                embed=discord.Embed(title=f"{member.display_name} foi desbanido!", color=0x00ff00)
                embed.add_field(name="Desbanido por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
                embed.set_footer(text=f"ID do usuário: {member.id}")
                channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
                await channel.send(embed=embed)
                await ctx.send(f'Desbaniu {member.mention} ({member.id})')
                return
            except Exception:
                await ctx.send(f'Não foi possível desbanir {member_id}!')

    @commands.command()
    async def kick(self, ctx, member: discord.Member | None = None, *, reason: str = ''):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Você deve especificar um membro para ser expulso!', delete_after = 10)
        else:
            try:
                await member.kick(reason = reason)

                player = get_player(member)

                if player:
                    currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    player['user_punishments'].append({'type':'kick','reason':reason,'time':currtime,'author':ctx.author.id})
                    punishments_table.update(player, PlayerQuery.id == member.id)

                    embed=discord.Embed(title=f"{member.display_name} foi expulso!", color=0xffff00)
                    embed.add_field(name="Expulso por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
                    embed.add_field(name="Motivo", value=f"{reason}", inline=True)
                    embed.set_footer(text=f"ID do usuário: {member.id}")
                    channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
                    await channel.send(embed=embed)
                    await ctx.send(f'Expulsou {member.mention} ({member.id})')
            
            except Exception:
                await ctx.send('Não foi possível expulsar!')
        
    @commands.command(aliases=['mute'])
    async def timeout(self, ctx, member: discord.Member | None = None, duration = '30m', *, reason: str = ''):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager', 'Mod']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Insira um membro! (!timeout \{membro\} \{duração\} \{motivo\})')
            return
        
        length = time_input_convert(duration)
        if length == -1:
            await ctx.send('Duração inválida! Digite a duração no formato (s/m/d/h). Ex: 7d para 7 dias.')
            return
        
        length_delta = datetime.datetime.now().astimezone() + datetime.timedelta(seconds = length)
        try:
            await member.timeout(length_delta, reason = reason)
            player = get_player(member)

            currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            length_db = length_delta.strftime("%Y-%m-%d %H:%M:%S")
            player['user_punishments'].append({'type':'timeout','reason':reason,'time':currtime,'length':length_db,'removed':False,'author':ctx.author.id})
            punishments_table.update(player, PlayerQuery.id == member.id)

            embed=discord.Embed(title=f"{member.display_name} foi silenciado!", color=0x0000ff)
            embed.add_field(name="Silenciado por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
            embed.add_field(name="Motivo", value=f"{reason}", inline=True)
            embed.add_field(name="Duração", value=f'{time_convert(length)}')
            embed.set_footer(text=f"ID do usuário: {member.id}")

            channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
            await channel.send(embed=embed)
            await ctx.send(f'Silenciou {member.mention} ({member.id})')
            
        except Exception:
            await ctx.send('Não foi possivel silenciar!')
            
    @commands.command(aliases=['unmute'])
    async def untimeout(self, ctx, member: discord.Member | None = None):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager', 'Mod']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Insira um membro! (!untimeout \{membro\}')
            return
        
        try:
            await member.timeout(datetime.timedelta(seconds = 0))
            player = get_player(member)
            for punishment in player['user_punishments'][::-1]:
                if punishment['type'] == 'timeout' and punishment['removed'] == False:
                    punishment['removed'] = True
                    punishment['removed_by'] = ctx.author.id
                    punishments_table.update(player, PlayerQuery.id == member.id)
                    embed=discord.Embed(title=f"{member.display_name} foi desmutado!", color=0xaaaaff)
                    embed.add_field(name="Desmutado por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
                    embed.set_footer(text=f"ID do usuário: {member.id}")
                    channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
                    await channel.send(embed=embed)
                    await ctx.send(f'Removido silenciamento de {member.mention} ({member.id})!')
                    break

            else:
                await ctx.send(f'{member.display_name} não está silenciado!')

        except commands.MemberNotFound as error:
            await ctx.send(f'Membro ({error.argument}) não encontrado!')

        except Exception:
            await ctx.send(f'{member.mention} não está silenciado!')
            
#? All optimised!
class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command(aliases=['purge','clean','limpar'])
    async def clear(self, ctx, amount: int = 10, user: discord.Member | str | None = None):
        if permissions_handler(ctx, 'manage_messages', exempt_roles=['Manager']) is False: return

        if user in ['self', 'bot', 'client']:
            user == self.bot.user
        
        if user is None:
            try:
                await ctx.channel.purge(limit=amount)
                await ctx.send(f'Apagou {amount} mensagens.', delete_after=5)
            except Exception: 
                await ctx.send('Insira um número válido.', delete_after=5)
            return

        try:
            await ctx.channel.purge(limit=amount, check = lambda m: m.author == user)
        except Exception:
            await ctx.send('Insira um número e um membro válido.', delete_after=10)

    @commands.command(aliases=['delay', 'cooldown'])
    async def slowmode(self, ctx, time: int = 0):
        if permissions_handler(ctx, 'manage_channels', exempt_roles=['Manager']) is False: return

        if not isinstance(time, int) or time > 21600:
            await ctx.send('Digite um tempo em segundos, digite 0 para desativar!')
        else:
            await ctx.channel_edit(slowmode_delay=time)
            await ctx.send(f'Slowmode alterado para {time} segundos!', delete_after = 10)
        
    @commands.command()
    async def setnickname(self, ctx, member: discord.Member | None = None, nick: str | None = None):
        if permissions_handler(ctx, 'manage_nicknames', exempt_roles=['Manager']) is False: return

        if not isinstance(member, discord.Member) or not isinstance(nick, str):
            await ctx.send('Insira um membro e um nick! Ex !nick @Edu#2340 Edu!', delete_after = 10)
            return

        try:
            await member.edit(nick=nick)
            await ctx.send(f'Nickname alterado para {nick}!', delete_after=5)
        except Exception:
            await ctx.send('Não foi possível alterar o nickname!', delete_after=5)
    
    @commands.command(aliases=['historico', 'punicoes', 'punishments'])
    async def history(self, ctx, member: discord.Member | None = None):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager', 'Mod']) is False: return

        if not isinstance(member, discord.Member):
            member = ctx.author
        
        player = get_player(member)
        
        _text = [f'{i}. {"~~" if punishment["removed"] else ""}{punishment["type"]} | ({punishment["time"]}) - \
                {punishment["reason"]} {"~~" if punishment["removed"] else ""}' \
                for i, punishment in enumerate(player['user_punishments'], start=1)]
        
        text = '\n'.join(_text) if _text else 'Sem punições no histórico!'

        embed=discord.Embed(title=f'**Histórico de {member.display_name}!**', description=text)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        embed.set_footer(text=f'ID do usuário: {member.id}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['clearpunishments'])
    async def clearhistory(self, ctx, member: discord.Member | None = None):
        if permissions_handler(ctx, 'administrator', exempt_roles=['Manager']) is False: return
        if not isinstance(member, discord.Member):
            member = ctx.author
        try:
            punishments_table.remove(PlayerQuery.id == member.id)
            await ctx.send(f'Limpou o histórico de {member.mention}')
        except Exception:
            await ctx.send(f'Não foi possível limpar o histórico de {member.mention}')

    @commands.command(aliases=['travar', 'trancar'])
    async def lock(self, ctx):
        if permissions_handler(ctx, 'manage_channels', exempt_roles=['Manager']) is False: return

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = False)
        await ctx.send(f'{ctx.author.mention} trancou o canal!')

    @commands.command(aliases=['destravar', 'destrancar'])
    async def unlock(self, ctx):
        if permissions_handler(ctx, 'manage_channels', exempt_roles=['Manager']) is False: return

        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages = True)
        await ctx.send(f'{ctx.author.mention} destrancou o canal!')

#? All optimised
class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_warnings.start()

    @commands.command()
    async def warn(self, ctx, member: discord.Member | None = None, *, reason: str = ''):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Insira um membro! (`!warn \{membro\} \{motivo\}`)')
            return

        player = get_player(member)

        if player:
            currtime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            exptime = (datetime.datetime.now() + datetime.timedelta(days = WARNINGS_EXPIRATION)).strftime("%Y-%m-%d %H:%M:%S")

            player['warnings'].append({'reason':reason,'time':currtime,'expiration':exptime})
            punishments_table.update(player, PlayerQuery.id == member.id)

            player['user_punishments'].append({'type':'warn','reason':reason,'time':currtime,'removed':False,'author':ctx.author.id})
            punishments_table.update(player, PlayerQuery.id == member.id)

            for key, value in AUTO_PUNISHMENTS:
                if len(player['warnings']) == int(key):
                    await WarningActions(self.bot).process(ctx, value, member)
                    break

            await ctx.send(f'Advertiu {member.mention}!')
            embed=discord.Embed(title=f"{member.display_name} foi advertido!", color=0xff6600)
            embed.add_field(name="Advertido por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
            embed.add_field(name="Motivo", value=f"{reason}", inline=True)
            embed.set_footer(text=f"ID do usuário: {member.id}")
            channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
            await channel.send(embed=embed)
    
    @commands.command()
    async def unwarn(self, ctx, member: discord.Member | None = None):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager']) is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Você deve inserir um membro para remover a advertência! (!unwarn \{membro\})')
            return
        
        try:
            player = get_player(member)
            
            warning = player['warnings'].pop()
            punishments_table.update(player, PlayerQuery.id == member.id)
            
            for punishment in player['user_punishments']:
                if punishment['type'] == 'warn' and punishment['time'] == warning['time']:
                    punishment['removed'] = True
                    punishment['removed_by'] = ctx.author.id
                    punishments_table.update(player, PlayerQuery.id == member.id)
                    embed=discord.Embed(title=f"Removida advertência de {member.display_name}!", color=0xff9900)
                    embed.add_field(name="Removida por", value=f"{ctx.author.display_name} ({ctx.author.id})", inline=False)
                    embed.set_footer(text=f"ID do usuário: {member.id}")
                    channel = self.bot.get_channel(PUNISHMENTS_CHANNEL)
                    await channel.send(embed=embed)
                    break
            
            await ctx.send(f'Removeu uma advertência de {member.mention}')
                
        except IndexError:
            await ctx.send(f'{member.mention} não possui advertências!')

    @commands.command(aliases=['warns', 'warnlist'])
    async def warnings(self, ctx, member: discord.Member | None = None):
        if permissions_handler(ctx, 'kick_members', exempt_roles=['Manager', 'Mod']) is False: return

        if not isinstance(member, discord.Member):
            member = ctx.author
        
        player = get_player(member)

        _text = [f'{i}. ({warning["time"]}) - {warning["reason"]}\n' for i, warning in enumerate(player["warnings"], start=1)]
        text = '\n'.join(_text) if _text else 'Não possui warnings ativos!'

        embed=discord.Embed(title=f'**Warnings de {member.display_name}!**', description=text)
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar)
        embed.set_footer(text=f'ID do usuário: {member.id}')
        await ctx.send(embed=embed)

    @tasks.loop(minutes=5)
    async def check_warnings(self):
        for player in punishments_table:
            for warning in player['warnings'][::-1]:
                time = datetime.strptime(warning['expiration'], '%Y-%m-%d %H:%M:%S')  
                if datetime.datetime.now() > time:
                    player['warnings'].remove(warning)
                    punishments_table.update(player)

#* All working
#! Missing features
class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.content.startswith('!') or len(message.content) < AUTOMOD_MINIMUM_LENGTH:
            return
        
        if 'cargo 2' in [role.name for role in message.author.roles]:
            return
        
        if 'discord.gg' in message.content:
            await message.delete()
            await message.channel.send('Você não pode enviar convites aqui!')
            return
        
        time = datetime.datetime.now() - datetime.timedelta(hours=1)
        messages = len([msg.content async for msg in message.channel.history(limit=None, after=time) if msg.author == message.author and msg.content == message.content])
        if messages > AUTOMOD_FLOOD_AMOUNT:
            await message.channel.send(f'Pare de flood! Você já mandou essa mensagem muitas vezes!')
            return

        if len(message.mentions) > AUTOMOD_MAX_MENTIONS:
            await message.channel.send(f'Você mencionou muitos usuários!')
            return

async def setup(bot):
    await bot.add_cog(Punishments(bot))
    await bot.add_cog(Management(bot))
    await bot.add_cog(Warnings(bot))
    await bot.add_cog(AutoMod(bot))
    await bot.add_cog(WarningActions(bot))