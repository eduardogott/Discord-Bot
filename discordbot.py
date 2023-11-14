'''
WAITING FOR REWRITE
all_apis.py
announcers.py
apis.py
customcommands.py
dm.py
giveaway.py
help.py
leveling.py
loggers.py
moderation.py
music.py
profiles.py
roles.py
statistics.py
tempchannels.py
tickets.py
utils.py'''

'''
Image Manipulation: Generate memes, resize images, apply filters, or create image-based games.
Fun Games and Trivia: Provide interactive games, trivia quizzes, or word-based challenges.
Weather Updates: Fetch and display current weather conditions or forecasts for specified locations.
Event/Message Scheduling: Allow users to schedule and manage events or reminders within the Discord server.
API Integration: Integrate with external APIs to fetch data from sources like Wikipedia, IMDB, or Twitter.
Starboard: Store and retrieve memorable quotes or messages from the server's chat history.
Translation: Translate messages or entire conversations between different languages.
Customized Embeds: Design and send customized rich embeds with interactive elements.


!youtube
!twitch
!twitter
!insta
!reddit
!spotify/!deezer
!github
!imgur
!tenor
!giphy
!quotify (meme quote)
!memefy (create a meme)
!dicionario (dicio)
!wikipedia (wikipedia)
!crypto (CoinGecko)
!covid



Wttr.in? Wikipedia?
OpenWeatherMap API: Fetch current weather conditions or forecasts for specified locations.
News API: Retrieve news articles from various sources and share them with your server members.
Cat Facts API: Retrieve random cat facts to share with your server members.
Dog CEO's Dog API: Fetch images and information about different dog breeds.
JokeAPI: Retrieve random jokes, puns, or programming-related jokes to lighten the mood.
Quotes REST API: Access a large collection of famous quotes or random quotes on various topics.
Urban Dictionary API: Retrieve definitions and explanations from the Urban Dictionary.
Recipe Puppy API: Fetch recipes based on ingredients or specific cuisines.
Oxford Dictionaries API: Get definitions, synonyms, or translations of words and phrases.
CoinGecko API: Fetch cryptocurrency data such as prices, market trends, or specific coin information.
REST Countries API: Retrieve information about countries, including population, languages, and currencies.
Random Famous Quotes API: Fetch quotes from famous individuals across different categories.
NASA's Astronomy Picture of the Day (APOD) API: Retrieve and display the daily astronomy picture from NASA.

# TODO: LEVEL ROLES
# TODO Quizzes and games
# TODO Translate

# FIXME Role names in permissions
# FIXME Add Wikipedia to utils.py 

# TODO Add error handling to commands: Member/User/Role/ChannelNotFound
# TODO Some private message things

# TODO Twitch-Discord verification/linking
# TODO Lyrics in music.py
# TODO !punir with default reasons and lengths
# TODO Scheduled messages
# TODO twitch statistics in statistics.py
# TODO Embed sender
# TODO Call recording
# TODO Search pokedex, twitch, youtube, twitter, reddit

# TODO Twitch bot
'''
import discord
from discord.ext import commands

intents = discord.Intents.all()
intents.message_content = True
intents.members = True

class BotClient(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!', '.'), case_insensitive = True,
                         strip_after_prefix = True, intents=intents, help_command=None)

    async def setup_hook(self):
        await bot.load_extension('ext.economy')
        #customcommands

    async def on_ready(self):
        await bot.change_presence(status=discord.Status.online, activity = discord.Game(name=f'Digite !help para ver a lista de comandos!'))
        print(f'Bot ready as {self.user}')
        print(f'Bot loaded in {", ".join([guild.name for guild in self.guilds])}')


    async def on_message(self, message):
        await bot.process_commands(message)
    

bot = BotClient()
bot.run('MTEwNzM2MTM4MzEwMTc2Nzc3Mg.Guv9AR.jF5qfs-Pvp8DD1r_My5aXLfy0sIi4eoPbec3-I')