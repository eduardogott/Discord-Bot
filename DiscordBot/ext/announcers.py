import discord
import requests
import json
from discord.ext import commands, tasks

with open('config.json') as f:
    file = json.load(f)
    twitch_config = file['Configuration']['Announcers']['Twitch']
    youtube_config = file['Configuration']['Announcers']['YouTube']

#* All working
class Twitch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_username = twitch_config['Username']
        self.discord_chid = twitch_config['DiscordChannelID']
        self.twitch_api_url = f'https://api.twitch.tv/helix/streams?user_login={self.twitch_username}'
        self.is_stream_live = False
        self.twitch_client_id = '81p0b8zrd3cmnj4n7rg441q5zfn7ss'  
        self.check_stream.start()

    @tasks.loop(seconds=15)
    async def check_stream(self):
        headers = {'Client-ID': self.twitch_client_id}
        response = requests.get(self.twitch_api_url, headers=headers)
        data = json.loads(response.text)
        stream_data = data['data'][0] if 'data' in data and len(data['data']) > 0 else None

        if stream_data is not None and not self.is_stream_live:
            channel = self.bot.get_channel(self.discord_channel_id)
            message = f'Live on! https://twitch.tv/{self.twitch_username} ||@everyone||'
            await channel.send(message)
        
        self.is_stream_live = stream_data is not None

#! Needs the YouTube Channel ID!
'''class YouTube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.youtube_channel_id = youtube_config['YouTubeChannelID']
        self.discord_channel_id = youtube_config['DiscordChannelID']
        self.youtube_api_url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={self.youtube_channel_id}&maxResults=1&order=date&type=video&key=YOUR_YOUTUBE_API_KEY'
        self.last_video_id = None
        self.check_youtube.start()

    @tasks.loop(seconds=15)
    async def check_youtube(self):
        response = requests.get(self.youtube_api_url)
        data = json.loads(response.text)
        video_data = data['items'][0] if 'items' in data and len(data['items']) > 0 else None

        if video_data is not None:
            published_at_str = video_data['snippet']['publishedAt']
            published_at = datetime.datetime.strptime(published_at_str, "%Y-%m-%dT%H:%M:%S.%fZ")
            current_time = datetime.datetime.utcnow()

            if current_time - published_at <= datetime.timedelta(minutes=5):
                channel = self.bot.get_channel(self.discord_channel_id)
                video_id = video_data['id']['videoId']

                if video_id != self.last_video_id:
                    video_url = f'https://www.youtu.be/{video_id}'
                    message = f'New video! {video_url}'
                    await channel.send(message)
                    self.last_video_id = video_id'''

async def setup(bot):
    await bot.add_cog(Twitch(bot))
    #await bot.add_cog(YouTube(bot))