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
bot.run('Hidden for obvious reasons')
