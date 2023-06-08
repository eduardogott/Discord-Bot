import discord
from datetime import datetime, timedelta
import json
from discord.ext import commands, tasks
from tinydb import TinyDB, Query

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
levels_table = db.table('levels')

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.level = 1
        self.xp = 10

PlayerQuery = Query()

#* All working!
class LevelListener(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_start_times = {}
        self.check_voice_duration.start()
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        player = levels_table.get(PlayerQuery.id == message.author.id)
        if player is None:
            player = Player(message.author.id)
            levels_table.insert({'id': player.id, 'level': player.level, 'xp': player.xp})
        else:
            player['xp'] += 10
            player['xp'] += 5 if "Sub" in [role.name for role in message.author.roles] else 0
            player['xp'] += 5 if "Booster" in [role.name for role in message.author.roles] else 0 
            if player['xp'] >= player['level'] * 1000:
                player['level'] += 1
                await message.channel.send(f"{message.author.mention} subiu para o nível '**{player['level']}**!'")
            
            levels_table.update(player, PlayerQuery.id == player['id'])

    @tasks.loop(minutes=5)
    async def check_voice_duration(self):
        for member, start_time in list(self.voice_start_times.items()):
            duration = datetime.now() - start_time

            if duration >= timedelta(minutes=5):
                self.voice_start_times[member] = datetime.now()
                player = levels_table.get(PlayerQuery.id == member.id)
                if player is None:
                    player = Player(member.id)
                    levels_table.insert({'id': player.id, 'level': player.level, 'xp': player.xp})
                else:
                    player['xp'] += 15
                    player['xp'] += 5 if "Sub" in [role.name for role in member.roles] else 0
                    player['xp'] += 5 if "Booster" in [role.name for role in member.roles] else 0 

                    if player['xp'] >= player['level'] * 1000:
                        player['level'] += 1
                        await member.send(f"{member.mention} subiu para o nível '**{player['level']}**!'")

                    levels_table.update(player, PlayerQuery.id == player['id'])

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            self.voice_start_times[member] = datetime.now()

        elif before.channel is not None and after.channel is None:
            if member in self.voice_start_times:
                del self.voice_start_times[member]
    
    @check_voice_duration.before_loop
    async def before_check_voice_duration(self):
        await self.bot.wait_until_ready()

#? All optimised!
class LevelCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def level(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        player = levels_table.get(PlayerQuery.id == member.id)

        if player:
            await ctx.send(f'{member.display_name} está no nível **{player["level"]}**! (**{player["xp"]} XP**)')
        else:
            await ctx.send(f'{member.display_name} não ganhou XP ainda!')
    
    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        player = levels_table.get(PlayerQuery.id == member.id)
        if player is None:
            await ctx.send(f'{member.display_name} não ganhou XP ainda!')
            return
        
        players = levels_table.all()
        sorted_players = sorted(players, key=lambda p: p['xp'], reverse=True)
        rank = sorted_players.index(player) + 1
        await ctx.send(f'Rank de {member.display_name}: {rank}° lugar (**nível {player["level"]}** - **{player["xp"]} XP**)')
        
    @commands.command(aliases=['ranking'])
    async def leaderboard(self, ctx):
        players = levels_table.all()
        sorted_players = sorted(players, key=lambda p: p['xp'], reverse=True)[:10]
        members = [ctx.guild.get_member(member_id) for member_id in [player['id'] for player in sorted_players]]

        leaderboard_text = [f'{i+1}. {member.display_name} - Nível **{player["level"]}** (**{player["xp"]} XP**)' \
                            for i, (player, member) in enumerate(zip(sorted_players), members)]

        embed=discord.Embed(title="**Tabela de XP**", description=f"{leaderboard_text}", color=0x982ab4)
        await ctx.send(embed=embed)

#? All optimised!
class LevelAdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['setxp'])
    @commands.has_permissions(administrator=True)
    async def setexp(self, ctx, member: discord.Member = None, new_exp: int = None):
        if member is not None:
            if new_exp is not None:
                player = levels_table.get(PlayerQuery.id == member.id)

                if player is None:
                    player = Player(member.id)
                    levels_table.insert({'id': player.id, 'level': player.level, 'xp': player.xp})
                
                old_player = player['xp']
                player['xp'] = new_exp
                player['level'] = new_exp // 1000 if new_exp >= 1000 else 1
                
                levels_table.update(player, PlayerQuery.id == player['id'])
                await ctx.send(f'EXP de {member.display_name} alterado para {player["xp"]} (era {old_player})')
    
            else:
                await ctx.send('Insira um novo EXP! (!setexp \{membro\} \{exp\})')
        else:
            await ctx.send('Insira um membro! (!setexp \{membro\} \{exp\})')

    @commands.command(aliases=['addxp'])
    @commands.has_permissions(administrator=True)
    async def addexp(self, ctx, member: discord.Member = None, add_exp: int = None):
        if discord.Member is not None:
            if add_exp is not None:
                player = levels_table.get(PlayerQuery.id == member.id)

                if player is None:
                    player = Player(member.id)
                    levels_table.insert({'id': player.id, 'level': player.level, 'xp': player.xp})
                
                old_player = player['xp']

                player['xp'] += add_exp
                player['level'] = player['xp'] // 1000 if player['xp'] >= 1000 else 1

                levels_table.update(player, PlayerQuery.id == player['id'])
                await ctx.send(f'EXP de {member.display_name} alterado para {player["xp"]} (era {old_player})')
    
            else:
                await ctx.send('Insira EXP para adicionar! (!addexp \{membro\} \{exp\})')
        else:
            await ctx.send('Insira um membro! (!addexp \{membro\} \{exp\})')

    @commands.command(aliases=['removexp, takexp, removeexp'])
    async def takeexp(self, ctx, member: discord.Member = None, remove_exp: int = None):
        if discord.Member is None:
            await ctx.send('Insira um membro! (!takeexp \{membro\} \{exp\})')
            return

        if remove_exp is None:
            await ctx.send('Insira EXP para remover! (!takeexp \{membro\} \{exp\})')
            return
        
        player = levels_table.get(PlayerQuery.id == member.id)
        if player is None:
            await ctx.send(f'{member.display_name} não possui EXP!')
            return

        if player['xp'] <= remove_exp:
            await ctx.send('O jogador irá ficar com EXP negativo!')
            return

        old_player = player['xp']        
        player['xp'] -= remove_exp
        player['level'] = player['xp'] // 1000 if player['xp'] >= 1000 else 1

        levels_table.update(player, PlayerQuery.id == player['id'])
        await ctx.send(f'EXP de {member.display_name} alterado para {player["xp"]} (era {old_player})')

    @commands.command(alias=['xpreset', 'expreset', 'resetxp'])
    @commands.has_permissions(administrator=True)
    async def resetexp(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send('Insira um membro! (!expreset |{membro\})')
            return
        
        player = levels_table.get(PlayerQuery.id == member.id)
        if player is None:
            await ctx.send('O membro mencionado não possui EXP!')
            return
        
        old_player = player

        levels_table.remove(PlayerQuery.id == member.id)
        await ctx.send(f'O nível de {member.display_name}\ (**{old_player["level"]}**, **{old_player["xp"]} XP**) foi resetado!')

async def setup(bot):
    await bot.add_cog(LevelListener(bot))
    await bot.add_cog(LevelCommands(bot))
    await bot.add_cog(LevelAdminCommands(bot))