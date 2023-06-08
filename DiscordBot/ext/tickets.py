import discord
from discord.ext import commands

#! Everything missing!
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Manager')
    async def ticketsetup(self, ctx):
        embed = discord.Embed(title=':envelope_with_arrow: Abrir ticket!')
        embed.add_field(name='Reaja aqui para abrir um ticket!',value='Clique em :envelope_with_arrow:!')
        message = await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Tickets(bot))