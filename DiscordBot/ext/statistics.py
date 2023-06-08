import discord
from discord.ext import commands, tasks
from youtube_search import YoutubeSearch

#! Missing Twitch followers!
class Statistics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.update_statistics.start()
        self.guild_id = 1107127331119706224
        self.channel_names = ['Membros totais', 'Membros online', 'Cargos', 'Seguidores Twitch', 'Inscritos YouTube']
        self.twitch_id = 666559696
        self.youtube_id = 'UCGD_gX2JQ2-F3yjsKeNM0gA'

    @tasks.loop(seconds=60)
    async def update_statistics(self):
        guild = self.bot.get_guild(self.guild_id)
        online_members = sum(member.status != discord.Status.offline for member in guild.members)
        youtube_subscribers = YoutubeSearch(self.youtube_id, max_results=1).to_dict()[0]['subscribers']

        vars = [guild.member_count, online_members, len(guild.roles)-1, 0, youtube_subscribers]

        category = discord.utils.get(guild.categories, name='Estatísticas')
        for i, channel in enumerate(category.voice_channels):
            channel[i].edit(name=f'{self.channel_names[i]: {vars[i]}}')

async def setup(bot):
    await bot.add_cog(Statistics(bot))