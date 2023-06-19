import discord
from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import datetime
import asyncio
import os

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
tempchannels_table = db.table('tempchannels')

class TempChannel:
    def __init__(self, player_id, channel_id, type, creation_date, members):
      self.owner_id = player_id
      self.channel_id = channel_id
      self.type = type
      self.creation_date = creation_date
      self.authorized = members
      self.all_time_members = members
      self.last_member_seen = creation_date

ChannelQuery = Query()

class Decorators():
    def __init__(self):
        self.table = tempchannels_table
    
    def channel_exists():
        async def predicate(self, ctx, ctd = None):
            ChannelQuery = Query()
            if ctd is None:
                ctd = ctx.channel

            channel = self.table.get(ChannelQuery.channel_id == ctd.id)
            if not len(channel):
                await ctx.send('Você não está em um ou não mencionou um canal temporário!')
                return
            
            return True
        
        return commands.check(predicate)
    
    def is_owner():
        async def predicate(self, ctx, ctd = None):
            ChannelQuery = Query()
            if ctd is None:
                ctd = ctx.channel

            channel = self.table.get(ChannelQuery.channel_id == ctd.id)
            
            if channel['owner_id'] != ctx.author.id:
                await ctx.send('Você não é o dono deste canal!')
                return

            return True

        return commands.check(predicate)

    def is_owner_and_exists(self, ctx, ctd=None):
        return self.channel_exists(ctx, ctd) and self.is_owner(ctx, ctd)

class CreateChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_id = 123123123123

    @commands.command(aliases=['tc', 'tcc', 'tccreate', 'tempchannelcreate'])
    async def tempchannel(self, ctx):
        check_creation = lambda m: m.author == ctx.author and m.content in ['texto', 'voz'] and m.channel == ctx.channel
        check_mentions = lambda m: m.author == ctx.author and len(m.mentions) and m.channel == ctx.channel

        await ctx.send('Que tipo de canal você deseja ciar? (texto/voz)')
        try:
            type = await self.wait_for('message', timeout=60, check=check_creation)
            
            channels = tempchannels_table.get(ChannelQuery.owner_id == ctx.author.id and ChannelQuery.type == type)
            if len(channels):
                channel = self.bot.get_channel(channels['channel_id'])
                await ctx.send(f'Você já tem um canal de {type}! ({channel.mention})')
                return
        except asyncio.TimeoutError:
            await ctx.send('Você não escolheu um tipo a tempo!')

        try:
            await ctx.send('Mencione os membros que você quer adicionar ao seu canal (todos na mesma mensagem): ')
            members_answer = await self.wait_for('message', timeout=180, check=check_mentions)
            members = members_answer.mentions
            members.append(ctx.author)
        except:
            await ctx.send('Você não mencionou os membros a tempo!')
        
        category = discord.utils.get(ctx.guild.categories, id=self.temp_id)
        if category is None or not isinstance(category, discord.CategoryChannel):
            category = await ctx.guild.create_category('Temp')
        if type == 'voz':
                channel = await ctx.guild.create_voice_channel(f'Temp voz {ctx.author.display_name} ({ctx.author.id})',category=category)
        else:
            channel = await ctx.guild.create_text_channel(f'Temp texto {ctx.author.display_name} ({ctx.author.id})',category=category)

        channel.set_permissions(ctx.guild.default_role, read_messages = False, view_channel = False)
        [channel.set_permissions(user, read_messages = True, view_channel = True) for user in members]
        
        await ctx.send(f'Canal temporário criado ({channel.mention})!')
        await channel.send('Para ver a lista de comandos para gerenciar o canal, digite !tchelp')

        creation_date = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        tc = TempChannel(ctx.author.id, channel.id, type, creation_date, members)
        tempchannels_table.insert({'owner_id':tc.owner_id, 'channel_id':tc.channel_id, 'type':tc.type, 'creation_date':tc.creation_date, 'members':tc.authorized, 'all_time_members':tc.all_time_members, 'last_member_seen':tc.last_member_seen})

#! Add MaxChannels and other simple things to config.json
class ManageChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_log_channel = 1117017910863466577
        
    @commands.command(aliases=['tempchanneldelete', 'tcd'])
    @Decorators().is_owner_and_exists()
    async def tcdelete(self, ctx, ctd: discord.TextChannel or discord.VoiceChannel = None):
        if ctd is None:
            ctd = ctx.channel

        channel = tempchannels_table.get(ChannelQuery.channel_id == ctd.id)
        await ctx.send('Canal será deletado em 60 segundos, digite `cancelar` para cancelar!')
        try:
            self.wait_for('message', timeout=60, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content == 'cancelar')
        except asyncio.TimeoutError:
            if channel['type'] == 'texto':    
                logchannel = self.bot.get_channel(self.temp_log_channel)

                messages = []
                async for message in ctd.history():
                    messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

                all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['all_time_members']])
                close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['authorized']])
                
                creator = self.bot.get_user(channel["owner_id"])
                header = f'''Canal criado por: {creator.display_name} ({creator.id})
                Canal exluido por: {ctx.author.display_name} ({ctx.author.id})
                Todos os membros do canal: {all_members}
                Membros do canal quando foi fechado: {close_members}\n\n\n'''

                transcript = '\n'.join(messages)
                file = f'transcript_file{channel["channel_id"]}.txt'
                with open(file, 'w') as f:
                    f.write(header)
                    f.write(transcript)

                await logchannel.send(f'Transcrição do canal temporário {ctd.channel.name}\nCriado por {creator.display_name} ({creator.id})!', file=discord.File(file))
                await ctx.send('Canal será apagado em 5 segundos!')
                asyncio.sleep(5)
                ctd.delete()
                os.remove(file)
            else:
                await ctx.send(f'Apagou {ctd.name}!')
                await ctd.delete()
            
            tempchannels_table.delete(ChannelQuery.channel_id == ctd.id)

    @commands.command(aliases=['tca', 'tempchanneladd'])
    @Decorators().is_owner_and_exists()
    async def tcadd(self, ctx, ctd: discord.TextChannel or discord.VoiceChannel = None):
        if ctd is None:
            ctx = ctx.channel
            
        channel = tempchannels_table.get(ChannelQuery.channel_id == ctd.id)
        for member in ctx.message.mentions:
            ctd.set_permissions(member, read_messages = True, view_channel = True)
            if member.id not in channel['all_time_members']:
                channel['authorized'].append(member.id)
            if member.id not in channel['all_time_members']:
                channel['all_time_members'].append(member.id)
        
        tempchannels_table.update(channel, ChannelQuery.channel_id == ctd.id)
        if channel['type'] == 'texto':
            await ctd.send(f'Adicionou {" ".join([member.mention for member in ctx.message.mentions])} ao canal!')
        else:
            await ctx.send(f'Adicionou {" ".join([member.mention for member in ctx.message.mentions])} ao canal {ctd.mention}!')

    @commands.command(aliases=['tcr', 'tempchannelremove'])
    @Decorators().is_owner_and_exists()
    async def tcremove(self, ctx, ctd: discord.TextChannel or discord.VoiceChannel = None):
        if ctd is None:
            ctx = ctx.channel
            
        channel = tempchannels_table.get(ChannelQuery.channel_id == ctd.id)        
        for member in ctx.message.mentions:
            ctd.set_permissions(member, read_messages = False, view_channel = False)
            if member.id in channel['all_time_members']:
                channel['authorized'].remove(member.id)
        
        tempchannels_table.update(channel, ChannelQuery.channel_id == ctd.id)
        if channel['type'] == 'texto':
            await ctd.send(f'Removeu {" ".join([member.mention for member in ctx.message.mentions])} do canal!')
        else:
            await ctx.send(f'Removeu {" ".join([member.display_name for member in ctx.message.mentions])} do canal {ctd.mention}!')

    @commands.command(aliases=['tct', 'tempchanneltranscript'])
    @Decorators().is_owner_and_exists()
    async def tctranscript(self, ctx):
        channel = tempchannels_table.get(ChannelQuery.channel_id == ctx.channel.id)
        if channel['type'] == 'texto':
            messages = []
            async for message in ctx.channel.history():
                messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

            all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['all_time_members']])
            close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['authorized']])
            
            creator = self.bot.get_user(channel["owner_id"])
            header = f'''Canal criado por: {creator.display_name} ({creator.id})
            Todos os membros do canal: {all_members}
            Membros do canal quando foi transcrito: {close_members}\n\n\n'''

            transcript = '\n'.join(messages)
            file = f'transcript_file{channel["channel_id"]}.txt'
            with open(file, 'w') as f:
                f.write(header)
                f.write(transcript)

            await ctx.send(f'Transcrição do canal temporário {ctx.channel.name}\nCriado por {creator.display_name} ({creator.id})!', file=discord.File(file))
            asyncio.sleep(5)
            os.remove(file)

    @commands.command(aliases=['tch', 'tempchannelhelp'])
    async def tchelp(self, ctx):
        embed = discord.Embed(title='Comandos dos canais temporários', color=0x982ab4)
        embed.add_field(name='!tccreate', value='Cria um canal temporário', inline=True)
        embed.add_field(name='!tcdelete', value='Apaga um canal temporário', inline=True)
        embed.add_field(name='!tcadd', value='Adiciona membros a um canal temporário', inline=True)
        embed.add_field(name='!tcremove', value='Remove membros de um canal temporário', inline=True)
        embed.add_field(name='!tctranscript', value='Cria uma transcrição das mensagens do canal temporário', inline=True)
        await ctx.send(embed=embed)

class TempChannelsAdmin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.temp_log_channel = 1117017910863466577

    @commands.command()
    @commands.has_role('Manager')
    @Decorators().channel_exists()
    async def tcadelete(self, ctx, ctd: discord.TextChannel or discord.VoiceChannel = None):
        if ctd is None:
            ctd = ctx.channel

        channel = tempchannels_table.get(ChannelQuery.channel_id == ctd.id)
        await ctx.send('Canal será deletado em 15 segundos, digite `cancelar` para cancelar!')
        try:
            self.wait_for('message', timeout=15, check=lambda m: m.author == ctx.author and m.channel == ctx.channel and m.content == 'cancelar')
        except asyncio.TimeoutError:
            if channel['type'] == 'texto':    
                logchannel = self.bot.get_channel(self.ticket_logs_channel)

                messages = []
                async for message in ctd.history():
                    messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

                all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['all_time_members']])
                close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['authorized']])
                
                creator = self.bot.get_user(channel["owner_id"])
                header = f'''Canal criado por: {creator.display_name} ({creator.id})
                Canal exluido por: {ctx.author.display_name} ({ctx.author.id})
                Todos os membros do canal: {all_members}
                Membros do canal quando foi fechado: {close_members}\n\n\n'''

                transcript = '\n'.join(messages)
                file = f'transcript_file{channel["channel_id"]}.txt'
                with open(file, 'w') as f:
                    f.write(header)
                    f.write(transcript)

                await logchannel.send(f'Transcrição do canal temporário {ctd.channel.name}\nCriado por {creator.display_name} ({creator.id})!', file=discord.File(file))
                await ctx.send('Canal será apagado em 5 segundos!')
                asyncio.sleep(5)
                ctd.delete()
                os.remove(file)
            else:
                await ctx.send(f'Apagou {ctd.name}!')
                await ctd.delete()

    @commands.command()
    @commands.has_role('Manager')
    @Decorators().channel_exists()
    async def tcatranscript(self, ctx, ctd: discord.TextChannel or discord.VoiceChannel = None):
        if ctd is None:
            ctd = ctx.channel

        channel = tempchannels_table.get(ChannelQuery.channel_id == ctd.id)
        if channel['type'] == 'texto':
            logchannel = self.bot.get_channel(self.temp_logs_channel)
            
            messages = []
            async for message in ctd.channel.history():
                messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

            all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['all_time_members']])
            close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in channel['authorized']])
            
            creator = self.bot.get_user(channel["owner_id"])
            header = f'''Canal criado por: {creator.display_name} ({creator.id})
            Transcrição criada por: {ctx.author.display_name} ({ctx.author.id})
            Todos os membros do canal: {all_members}
            Membros do canal quando foi transcrito: {close_members}\n\n\n'''

            transcript = '\n'.join(messages)
            file = f'transcript_file{channel["channel_id"]}.txt'
            with open(file, 'w') as f:
                f.write(header)
                f.write(transcript)

            await ctx.send(f'Transcrição do canal temporário {ctd.channel.name}\nCriado por {creator.display_name} ({creator.id})!', file=discord.File(file))
            await logchannel.send(f'Transcrição do canal temporário {ctd.channel.name}\nCriado por {creator.display_name} ({creator.id})!', file=discord.File(file))
            asyncio.sleep(5)
            os.remove(file)

class CheckChannels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.main_channel = 123123123123
        self.temp_log_channel = 1117017910863466577
        self.check_channels.start()

    @tasks.loop(seconds=60)
    async def check_channels(self):
        for ch in tempchannels_table:
            channel = self.get_channel(channel['channel_id'])
            if ch['type'] == 'texto':
                last_message = [message async for message in channel.history(limit=1)][0]
                last_message_time = last_message.created_at
                ch['last_member_seen'] = last_message_time.strftime("%m/%d/%Y, %H:%M:%S")
                tempchannels_table.update(ch)
            else:
                if len(channel.members):
                    ch['last_member_seen'] = datetime.datetime.now()
                    tempchannels_table.update(ch)

        if ch['last_member_seen'].strptime("%m/%d/%Y, %H:%M:%S") < datetime.datetime.now() - datetime.timedelta(days=7):
            if ch['type'] == 'texto':
                logchannel = self.bot.get_channel(self.temp_log_channel)

                messages = []
                async for message in channel.history():
                    messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

                all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in ch['all_time_members']])
                close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in ch['authorized']])
                
                creator = self.bot.get_user(ch["owner_id"])
                header = f'''Canal criado por: {creator.display_name} ({creator.id})
                Canal exluido por: INATIVIDADE
                Todos os membros do canal: {all_members}
                Membros do canal quando foi fechado: {close_members}\n\n\n'''

                transcript = '\n'.join(messages)
                file = f'transcript_file{ch["channel_id"]}.txt'
                with open(file, 'w') as f:
                    f.write(header)
                    f.write(transcript)

                await logchannel.send(f'Transcrição do canal temporário {channel.name}\nCriado por {creator.display_name} ({creator.id})!', file=discord.File(file))
                asyncio.sleep(5)
                channel.delete()
                os.remove(file)
            else:
                main = self.get_channel(self.main_channel)
                await main.send(f'{channel.name} foi apagado por inatividade! ||({creator.mention})||')
                await channel.delete()

            tempchannels_table.delete(ChannelQuery.channel_id == channel.id)

        if ch['last_member_seen'].strptime("%m/%d/%Y, %H:%M:%S") < datetime.datetime.now() - datetime.timedelta(days=5):
            if ch['type'] == 'texto':
                await channel.send('Este canal será deletado em **2 dias** por inatividade!')
            else:
                main = self.get_channel(self.main_channel)
                await main.send(f'O canal {channel.mention} será deletado em **2 dias** por inatividade!')

async def setup(bot):
    await bot.add_cog(CreateChannels(bot))
    await bot.add_cog(ManageChannels(bot))
    await bot.add_cog(TempChannelsAdmin(bot))
    await bot.add_cog(CheckChannels(bot))