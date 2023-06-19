
# TODO: LEVEL ROLES
# TODO Weather using wttr.in
# TODO Quizzes and games
# TODO Translate
# TODO config.json for tickets and tempchannels

# FIXME Role names in permissions
# FIXME Add Wikipedia to utils.py 

# TODO Twitch-Discord verification/linking
# TODO Error handling
# TODO Lyrics in music.py
# TODO !punir with default reasons and lengths
# TODO Scheduled messages
# TODO twitch statistics in statistics.py
# TODO Embed sender
# TODO Call recording
# TODO Search pokedex, twitch, youtube, twitter, reddit

# TODO Twitch bot

import discord
from discord.ext import commands
from validator import config_validator

config_validator()

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
        await bot.load_extension('ext.roles')
        await bot.load_extension('ext.economy')

    async def on_ready(self):
        await bot.change_presence(status=discord.Status.online, activity = discord.Game(name=f'Digite !help para ver a lista de comandos!'))
        print(f'Bot ready as {self.user}')
        print(f'Bot loaded in {[guild.name for guild in self.guilds]}')


    async def on_message(self, message):

        await bot.process_commands(message)
    

bot = BotClient()
bot.run('MTEwNzM2MTM4MzEwMTc2Nzc3Mg.GZX_Kw.A1dx4TLR3oqgnAZf5pdcuOLU1UbncsoiPX_4xc')