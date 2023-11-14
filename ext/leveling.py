import discord
from datetime import datetime, timedelta
import json
from discord.ext import commands, tasks
from tinydb import TinyDB, Query
from _util_funcs import role_handler

START_EXP: int = 10 # Starting EXP
LEVEL_UP_REQUIREMENTS: int = 1000 # Player level will be EXP // REQUIREMENT
VOICE_CHECK_TIME: int = 300 # Time interval, in seconds, which users will be checked if they're in a voice call
EXP_AWARDED_TEXT: int = 10 # EXP per message
EXP_AWARDED_VOICE: int = 15 # EXP per VOICE_CHECK_TIME seconds in calls
EXP_BONUSES_TEXT: dict[str, int] = {'Sub': 5, 'Booster': 5} # Bonus EXP that'll be awarded to different roles {'Role': BonusEXP}
EXP_BONUSES_VOICE: dict[str, int] = {'Sub': 5, 'Booster': 5} # Bonus EXP that'll be awarded to different roles {'Role': BonusEXP}}

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
levels_table = db.table('levels')

def get_player(member: discord.Member):
    player = levels_table.get(PlayerQuery.id == member.id)
    if player is None:
        _player = Player(member.id)
        levels_table.insert({'id': _player.id, 'level': _player.level, 'xp': _player.xp})

    return levels_table.get(PlayerQuery.id == member.id)

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.level = 1
        self.xp = START_EXP

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

        player = get_player(message.author)

        player['xp'] += EXP_AWARDED_TEXT
        for role, value in EXP_BONUSES_TEXT:
            player['xp'] += value if role in [_role.name for _role in message.author.roles] else 0

        if player['xp'] >= player['level'] * LEVEL_UP_REQUIREMENTS:
            player['level'] += 1
            await message.channel.send(f"{message.author.mention} subiu para o nível '**{player['level']}**!'")
            
            levels_table.update(player, PlayerQuery.id == player['id'])

    @tasks.loop(minutes=5)
    async def check_voice_duration(self):
        for member, start_time in list(self.voice_start_times.items()):
            duration = datetime.now() - start_time

            if duration >= timedelta(seconds=VOICE_CHECK_TIME):
                self.voice_start_times[member] = datetime.now()
                player = get_player(member)
                
                player['xp'] += EXP_AWARDED_VOICE
                for role, value in EXP_BONUSES_VOICE:
                    player['xp'] += value if role in [_role.name for _role in member.roles] else 0

                if player['xp'] >= player['level'] * LEVEL_UP_REQUIREMENTS:
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
    async def level(self, ctx, member: discord.Member | None = None):
        if member is None:
            member = ctx.author

        player = get_player(member)

        await ctx.send(f'{member.display_name} está no nível **{player["level"]}**! (**{player["xp"]} XP**)')
    
    @commands.command()
    async def rank(self, ctx, member: discord.Member | None = None):
        if member is None:
            member = ctx.author

        player = get_player(member)
        
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
        self.req = LEVEL_UP_REQUIREMENTS

    @commands.command(aliases=['setxp'])
    async def setexp(self, ctx, member: discord.Member | None = None, new_exp: int | None = None):
        if role_handler(ctx, 'Manager') is False: return

        if isinstance(member, discord.Member) and isinstance(new_exp, int):
            player = get_player(member)

            if player:
                old_player = player['xp']
                player['xp'] = new_exp
                player['level'] = new_exp // self.req if new_exp >= self.req else 1
                
                levels_table.update(player, PlayerQuery.id == player['id'])
                await ctx.send(f'EXP de {member.display_name} alterado para {player["xp"]} (era {old_player})')
        else:
            await ctx.send('Insira um membro e uma quantidade de EXP! (!setexp \{membro\} \{exp\})')

    @commands.command(aliases=['addxp'])
    async def addexp(self, ctx, member: discord.Member | None = None, add_exp: int | None = None):
        if role_handler(ctx, 'Manager') is False: return

        if isinstance(member, discord.Member) and isinstance(add_exp, int):
            player = get_player(member)
            
            if player:
                old_player = player['xp']

                player['xp'] += add_exp
                player['level'] = player['xp'] // self.req if player['xp'] >= self.req else 1

                levels_table.update(player, PlayerQuery.id == player['id'])
                await ctx.send(f'EXP de {member.display_name} alterado para {player["xp"]} (era {old_player})')

        else:
            await ctx.send('Insira um membro e uma quantidade de EXP! (!addexp \{membro\} \{exp\})')

    @commands.command(aliases=['takexp'])
    async def takeexp(self, ctx, member: discord.Member | None = None, remove_exp: int | None = None):
        if role_handler(ctx, 'Manager') is False: return
        
        if isinstance(member, discord.Member) and isinstance(remove_exp, int):
            player = get_player(member)

            if player['xp'] <= remove_exp:
                await ctx.send('O jogador irá ficar com EXP negativo!')
                return

            old_player = player['xp']        
            player['xp'] -= remove_exp
            player['level'] = player['xp'] // self.req if player['xp'] >= self.req else 1

            levels_table.update(player, PlayerQuery.id == player['id'])
            await ctx.send(f'EXP de {member.display_name} alterado para {player["xp"]} (era {old_player})')
        
        else:
            await ctx.send('Insira um membro e uma quantidade de EXP! (!removeexp \{membro\} \{exp\})')

    @commands.command(alias=['xpreset', 'expreset', 'resetxp'])
    async def resetexp(self, ctx, member: discord.Member | None = None):
        if role_handler(ctx, 'Manager') is False: return

        if member is None:
            await ctx.send('Insira um membro! (!expreset |{membro\})')
            return
        
        player = get_player(member)
        
        old_player = player

        levels_table.remove(PlayerQuery.id == member.id)
        player = get_player(member)
        await ctx.send(f'O nível de {member.display_name}\ (**{old_player["level"]}**, **{old_player["xp"]} XP**) foi resetado!')

async def setup(bot):
    await bot.add_cog(LevelListener(bot))
    await bot.add_cog(LevelCommands(bot))
    await bot.add_cog(LevelAdminCommands(bot))