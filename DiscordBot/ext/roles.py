import discord
from discord.ext import commands

#* All working!
class AutoRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        role = discord.utils.get(member.guild.roles, name="Membro")
        await member.add_roles(role)

#! Everything missing!
'''class ReactionRole(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.message_id = None
        self.channel_id = None

    @commands.command(aliases=['registro','registrar'])
    async def register(self, ctx):
        message = await ctx.send('Iniciando registro')'''

async def setup(bot):
    await bot.add_cog(AutoRole(bot))
    #await bot.add_cog(ReactionRole(bot))