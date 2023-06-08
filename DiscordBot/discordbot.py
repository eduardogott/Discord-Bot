# COMMAND LIST:
# !greroll !gstart !gdelete
# !ban !kick !unban !clear !timeout !untimeout !slowmode !setnickname !warn !warnings !unwarn !history !clearhistory !lock !unlock
# !random !dado !jankenpon !escolher !calc !say !sayeveryone !sayhere
# !avatar !userbanner !serverbanner !servericon !userinfo !serverinfo !sobre
# !play !forceskip !voteskip !clearqueue !queue !remove !pause !resume !musica
# !level !rank !expreset !leaderboard !setexp !addexp
# !profile !rep !edit !nextbirthdays

#* All commands:
#* ECONOMY: !  

#* All systems

# Anunciador Twitch live, anunciador de vídeo no YouTube
# Sistema de sorteios (Em database de término, premio e vencedor)
# Sistema de níveis, com XP por mensagem e tempo de call (Em database, sem perder dados)
# Sistema de logar mensagens editadas e apagadas, comandos e alterações de nick e avatar
# Sistema de moderação com diversos comandos diferentes
# Sistema de advertências com database e punição automática
# Sistema de música no Discord com fila
# Sistema de perfis em database com +rep e anúncio de aniversário
# Sistema de cargo ao entrar e !registro
# Sistema de exibir as informações do Discord, Twitch e YouTube em forma de canais de voz
# Vários outros comandos úteis, como encurtador de URL e canais temporários

# FIXME Role names in permissions
# FIXME Add Wikipedia to utils.py 

# TODO Error handling
# TODO Temporary channels
# TODO Ticket system
# TODO Lyrics in music.py
# TODO !punir with default reasons and lengths
# TODO Scheduled messages
# TODO twitch statistics in statistics.py
# TODO Embed sender
# TODO Auto-mod other than repeating the same message
# TODO Call recording
# TODO !register command
# TODO Search pokedex, twitch, youtube, twitter, reddit

# TODO Twitch bot

import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, help_command=None)

    async def setup_hook(self):
        await bot.load_extension('ext.moderation')
        await bot.load_extension('ext.utils')
        await bot.load_extension('ext.giveaway')
        await bot.load_extension('ext.loggers')
        await bot.load_extension('ext.music')
        await bot.load_extension('ext.announcers')
        await bot.load_extension('ext.leveling')
        await bot.load_extension('ext.profiles')
        #await bot.load_extension('ext.roles')
        await bot.load_extension('ext.economy')

    async def on_ready(self):
        await bot.change_presence(status=discord.Status.online, activity = discord.Game(name=f'Digite !help para ver a lista de comandos!'))
        print(f'Bot ready as {self.user}')
        print(f'Bot loaded in {[guild.name for guild in self.guilds]}')


    async def on_message(self, message):
        if 'discord.gg' in message.content:
            if 'cargo 2' not in [role.name for role in message.author.roles]:
                await message.delete()

        await bot.process_commands(message)
    

bot = BotClient()
bot.run('MTEwNzM2MTM4MzEwMTc2Nzc3Mg.GZX_Kw.A1dx4TLR3oqgnAZf5pdcuOLU1UbncsoiPX_4xc')