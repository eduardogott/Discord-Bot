import discord
from discord.ext import commands
from _util_funcs import dm_only_handler

class DirectMessages(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    