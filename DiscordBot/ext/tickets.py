import discord
from discord.ext import commands
from tinydb import TinyDB, Query
from sys import stdout
import asyncio
import os

stdout.reconfigure(encoding='utf-8')

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
tickets_table = db.table('tickets')
punishments_table = db.table('punishments')

def time_convert(seconds, type = None):
    if type == 'min':
        seconds *= 60
    days = seconds // 86400
    seconds %= 86400
    hours = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    return '{}{}h {}m'.format(str(days) + 'd ' if days > 0 else '', 
                              str(hours) if hours > 0 else '',
                              str(minutes) if minutes > 0 else '')

class Ticket():
    def __init__(self, member_id, channel_id, category):
        self.member_id = member_id
        self.channel_id = channel_id
        self.authorized = [member_id]
        self.all_users_history = [member_id]
        self.category = category
        self.closed = False

TicketQuery = Query()
PlayerQuery = Query()

#! Add MaxTickets to config.json
#! Add self.ticket_reasons to config.json
#! Add cooldown to config.json
class CreateTickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ticket_reasons = {'suggestion':['Enviar uma sugestão','💡','Sugestões','Escreva sua sugestão abaixo: '],
                               'punishment':['Recorrer de uma punição','⛔','Recorrências','Digite abaixo de qual punição você quer recorrer: '],
                               'bugreport':['Reportar um bug','🛠️','Bug Reports','Escreva abaixo um breve resumo do bug e como reproduzi-lo: '],
                               'help_doubts':['Tirar dúvidas','💭','Dúvidas','Escreva abaixo sua dúvida: '],
                               'other':['Outro','❓','Outro']}

    @commands.command(aliases=['createticket', 'openticket', 'tcreate'])
    @commands.cooldown(1, 60*60, commands.BucketType.user)
    async def ticket(self, ctx):
        tickets_by_member = len(tickets_table.get(TicketQuery.member_id == ctx.author.id))
        if tickets_by_member > 2:
            await ctx.send('Você já tem 2 tickets abertos!')
            return
        
        player = punishments_table.get(PlayerQuery.id == ctx.author.id)
        if player and any(punishment['type'] == 'ticket-ban' and not punishment['removed'] for punishment in player['user_punishments']):
            await ctx.send('Você está banido de criar tickets!', delete_after=10)
            return
        
        text = ''.join([f'{self.ticket_reasons[k][1]} - {self.ticket_reasons[k][0]}\n' for k in self.ticket_reasons])
        embed = discord.Embed(title='Abrir um ticket!',description=text)
        embed.set_footer(text=f'Clique no emoji em até 60 segundos! (ID: {ctx.author.id})')
        message = await ctx.send(embed)

        for k in self.ticket_reasons:
            await message.add_reaction(self.ticket_reasons[k][1])

        def check(user, reaction):
            return ( user == ctx.author 
                    and str(reaction.emoji) in [k[1] for k in self.ticket_reasons] 
                    and reaction.message.id == message.id )

        try:
            reaction, _ = await self.wait_for('reaction_add', timeout = 60, check = check)
            selected_category = None
            for k in self.ticket_reasons:
                if str(reaction.emoji) == self.ticket_reasons[k][1]:
                    selected_category = k
                    break
        
        except asyncio.TimeoutError:
            await ctx.send('Tempo para seleção expirado!')
            return

        embed = discord.Embed(title='Criando ticket',description=f'Criando ticket na categoria {selected_category[2]}')
        message.edit(embed=embed)

        channel = await ctx.guild.create_text_channel(f'{selected_category[2].lower()}-{ctx.author.id}', category='Tickets')
        read_false = discord.PermissionOverwrite(read_messages=False)
        read_true = discord.PermissionOverwrite(read_messages=True)
        channel.set_permissions(ctx.guild.default_role, overwrite=read_false)
        channel.set_permissions(ctx.author, overwrite=read_true)

        embed = discord.Embed(title='Ticket criado!', description=f'Clique aqui: {channel.mention}')
        message.edit(embed=embed)

        embed = discord.Embed(title=f'Ticket de {ctx.author.mention}', description='Ticket aberto! Digite abaixo o que você precisa, e a equipe irá responder em até 24 horas!\nCaso seu ticket seja para recorrer de uma punição, pedimos que mencione o membro da equipe que a aplicou!')
        embed.set_footer(f'ID do usuário: {ctx.author.id}')

        ticket = Ticket(ctx.author.id, channel.id, selected_category)
        
        tickets_table.insert({'member_id':ticket.member_id,'channel_id':ticket.channel_id,'authorized':ticket.authorized,'all_users_history':ticket.all_users_history,'category':ticket.category,'closed':ticket.closed})

        channel.send(embed=embed)

        asyncio.sleep(20)
        message.delete()

    @ticket.error
    async def ticket_error(ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            remaining = round(error.retry_after)
            await ctx.send(f'Este comando está em cooldown! Aguarde {time_convert(remaining)} e tente novamente!')

class ManageTickets(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.ticket_logs_channel = 1117017910863466577

    @commands.command()
    @commands.has_role('Manager')
    async def tclose(self, ctx):
        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        if ticket['closed'] is True:
            await ctx.send('Este ticket já está fechado! Abra com !topen ou apague com !tdelete', delete_after = 10)
            return
        
        ticket['closed'] = True
        read_false = discord.PermissionOverwrite(read_messages=False)
        
        [ctx.channel.set_permissions(user, overwrite=read_false) for user in [self.bot.get_user(member) for member in ticket['authorized']]]
        
        await ctx.send('Ticket fechado!')

    @commands.command()
    @commands.has_role('Manager')
    async def topen(self, ctx):
        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        if ticket['closed'] is False:
            await ctx.send('Este ticket não está fechado!', delete_after = 10)
            return
        
        ticket['closed'] = False
        read_true = discord.PermissionOverwrite(read_messages=True)
        
        [ctx.channel.set_permissions(user, overwrite=read_true) for user in [self.bot.get_user(member) for member in ticket['authorized']]]
        
        await ctx.send('Ticket aberto!')
    
    @commands.command()
    @commands.has_role('Manager')
    async def tdelete(self, ctx):
        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        if ticket['closed'] is False:
            await ctx.send('Feche o ticket primeiro com !tclose')
            return

        await ctx.send('Apagando ticket em 60 segundos, digite `cancelar` para cancelar!')
        
        try:
            await self.wait_for('message', timeout = 60, check = lambda m: m.content == 'cancel')
            await ctx.send('Cancelou a exclusão do ticket!')

        except asyncio.TimeoutError:
            logchannel = self.bot.get_channel(self.ticket_logs_channel)

            messages = []
            async for message in ctx.channel.history():
                messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

            all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in ticket['all_users_history']])
            close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in ticket['authorized']])

            header = f'''Categoria do ticket: {ticket['category']}
            Ticket criado por: {ticket['member_id']}
            Ticket exluido por: {ctx.author.display_name} ({ctx.author.id})
            Todos os membros do ticket: {all_members}
            Membros do ticket quando foi fechado: {close_members}\n\n\n'''

            transcript = '\n'.join(messages)
            file = f'transcript_file{ticket["channel_id"]}.txt'
            with open(file, 'w') as f:
                f.write(header)
                f.write(transcript)

            await logchannel.send(f'Transcrição do ticket {ctx.channel.name}!', file=discord.File(file))
            await ctx.send('Ticket será apagado em 5 segundos!')
            asyncio.sleep(5)
            os.remove(file)

            tickets_table.remove(ticket)
            await ctx.channel.delete(reason='Ticket apagado via !tdelete')

    @commands.command()
    @commands.has_role('Manager')
    async def tadd(self, ctx, member: discord.Member = None):
        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        if ticket['closed'] is True:
            await ctx.send('Você não pode adicionar membros a um ticket fechado!')
            return
        
        if member not in ctx.guild.members:
            await ctx.send('Este membro não está no servidor!')
            return
        
        ticket['authorized'].append(member.id)
        read_true = discord.PermissionOverwrite(read_messages=True)
        ctx.channel.set_permissions(member, overwrite=read_true)

        if member.id not in ticket['all_users_history']:
            ticket['all_users_history'].append(member.id)

        await ctx.send(f'Adicionou {member.mention} ao ticket!')
        tickets_table.update(ticket, TicketQuery.channel_id == ctx.channel.id)

    @commands.command()
    @commands.has_role('Manager')
    async def tremove(self, ctx, member: discord.Member = None):
        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        if ticket['closed'] is True:
            await ctx.send('Você não pode remover membros de um ticket fechado!')
            return
        
        if member not in ctx.guild.members:
            await ctx.send('Este membro não está no servidor!')
            return
        
        if member.id not in ticket['authorized']:
            await ctx.send('Este jogador não está no ticket!')
            return
        
        ticket['authorized'].remove(member.id)
        read_false = discord.PermissionOverwrite(read_messages=False)
        ctx.channel.set_permissions(member, overwrite=read_false)
        
        await ctx.send(f'Removeu {member.mention} do ticket!')

    @commands.command()
    @commands.has_role('Manager')
    async def trename(self, ctx, new_name: str = None):
        if new_name is None:
            await ctx.send('Insira um novo nome para o canal!', delete_after = 10)
        
        if len(new_name) > 127:
            await ctx.send('Nome muito grande!', delete_after = 10)

        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        old_name = ctx.channel.name
        ctx.channel.edit(name=new_name)

        await ctx.send(f'Renomeou o canal para {new_name} (era {old_name}).')

    @commands.command()
    @commands.has_role('Manager')
    async def ttranscript(self, ctx):
        ticket = tickets_table.get(TicketQuery.channel_id == ctx.channel.id)
        if ticket is None:
            await ctx.send('Este canal não é um ticket!', delete_after = 10)
            return
        
        messages = []
        async for message in ctx.channel.history():
            messages.insert(0, f'({message.author.id}) | {message.author.display_name}: {message.content}')

        all_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in ticket['all_users_history']])
        close_members = ', '.join([(self.bot.get_user(user).display_name, user) for user in ticket['authorized']])

        header = f'''Categoria do ticket: {ticket['category']}
        Ticket criado por: {ticket['member_id']}
        Ticket exluido por: {ctx.author.display_name} ({ctx.author.id})
        Todos os membros do ticket: {all_members}
        Membros do ticket quando foi fechado: {close_members}\n\n\n'''

        transcript = '\n'.join(messages)
        file = f'transcript_file{ticket["channel_id"]}.txt'
        with open(file, 'w') as f:
            f.write(header)
            f.write(transcript)

        await ctx.send('Transcrição do ticket completada!', file=discord.File(file))
        asyncio.sleep(5)
        os.remove(file)

async def setup(bot):
    await bot.add_cog(CreateTickets(bot))