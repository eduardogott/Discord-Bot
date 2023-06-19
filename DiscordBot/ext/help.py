import discord
from discord.ext import commands
from tinydb import TinyDB

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
commands_table = db.table('custom_commands')

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['h', 'ajuda', '?', 'comandos', 'commands'])
    async def help(self, ctx, arg = None):
        if arg in ['eco', 'economy', 'economia']:
            embed = discord.Embed(title='Comandos de economia', color=0x982ab4)
            embed.add_field(name='!daily',value='Recebe o bônus diário')
            embed.add_field(name='!work',value='Trabalha para receber coins')
            embed.add_field(name='!balance',value='Exibe seu saldo em coins')
            embed.add_field(name='!pay',value='Envia coins para outro membro')
            embed.add_field(name='!shop',value='Exibe os ítens da loja')
            embed.add_field(name='!buy',value='Compra algum ítem na loja')
            embed.add_field(name='!inventory',value='Exibe seu inventário')
            embed.add_field(name='!use',value='Usa algum consumível do inventário')
            embed.add_field(name='!equip',value='Equipa/desequipa um ítem do inventário')
            embed.add_field(name='*!eco*',value='Adiciona/remove saldo de um membro')
            embed.add_field(name='*!giveitem*',value='Adiciona ítens a um membro')
            embed.add_field(name='*!takeitem*',value='Remove ítens de um membro')
            embed.add_field(name='*!clearinventory*',value='Limpa o invetário de um membro')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['gw', 'giveaway', 'giveaways', 'sorteio', 'sorteios']:
            embed = discord.Embed(title='Comandos de sorteios', color=0x982ab4)
            embed.add_field(name='*!gcreate*',value='Inicia um sorteio')
            embed.add_field(name='*!gend*',value='Encerra um sorteio prematuramente')
            embed.add_field(name='*!gdelete*',value='Cancela um sorteio')
            embed.add_field(name='*!greroll*',value='Sorteia um ganhador novamente')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['nivel', 'niveis', 'level', 'levels']:
            embed = discord.Embed(title='Comandos de níveis', color=0x982ab4)
            embed.add_field(name='!level',value='Exibe seu nível e XP')
            embed.add_field(name='!rank',value='Exibe sua posição no ranking')
            embed.add_field(name='!leaderboard',value='Exibe o top10 do ranking')
            embed.add_field(name='*!setexp*',value='Define o XP de um usuário')
            embed.add_field(name='*!addexp*',value='Adiciona XP a um usuário')
            embed.add_field(name='*!takeexp*',value='Remove XP de um usuário')
            embed.add_field(name='*!resetexp*',value='Reseta o XP de um usuário')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['mod', 'moderacao', 'moderation']:
            embed = discord.Embed(title='Comandos de moderação', color=0x982ab4)
            embed.add_field(name='*!ticketban*',value='Bane um membro de criar tickets')
            embed.add_field(name='*!unticketban*',value='Desbane um membro de criar tickets')
            embed.add_field(name='*!ban*',value='Bane um membro do servidor')
            embed.add_field(name='*!unban*',value='Desbane um membro do servidor')
            embed.add_field(name='*!kick*',value='Expulsa um membro do servidor')
            embed.add_field(name='*!timeout*',value='Aplica castigo a um membro')
            embed.add_field(name='*!untimeout*',value='Remove o castigo de um membro')
            embed.add_field(name='*!clear*',value='Limpa as mensagens do chat')
            embed.add_field(name='*!slowmode*',value='Adiciona modo lento ao chat')
            embed.add_field(name='*!setnickname*',value='Define o nick de um membro')
            embed.add_field(name='*!lock*',value='Bloqueia o chat do cargo everyone')
            embed.add_field(name='*!unlock*',value='Desbloqueia o chat para o cargo everyone')
            embed.add_field(name='*!history*',value='Exibe todas as punições de um membro')
            embed.add_field(name='*!clearhistory*',value='Limpa as punições de um membro')
            embed.add_field(name='*!warn*',value='Adiciona uma advertência a um membro')
            embed.add_field(name='*!unwarn*',value='Remove uma advertência de um membro')
            embed.add_field(name='*!warnings*',value='Lista as advertências de um membro')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['music', 'musics', 'musica', 'musicas']:
            embed = discord.Embed(title='Comandos de música', color=0x982ab4)
            embed.add_field(name='!play',value='Adiciona uma música a fila')
            embed.add_field(name='!skip',value='Pula a música atual')
            embed.add_field(name='!queue',value='Exibe a fila de músicas')
            embed.add_field(name='!clearqueue',value='Limpa a fila de músicas')
            embed.add_field(name='!remove',value='Remove uma música da fila')
            embed.add_field(name='!pause',value='Pausa a música')
            embed.add_field(name='!resume',value='Resume a música')
            embed.add_field(name='!musica',value='Exibe informações sobre a música atual')
            embed.add_field(name='!replay',value='Adiciona a música atual a fila')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`DJ`*')
            await ctx.send(embed=embed)
            
        elif arg in ['profile', 'profiles', 'perfil', 'perfis']:
            embed = discord.Embed(title='Comandos de perfis', color=0x982ab4)
            embed.add_field(name='!edit',value='Edita seu perfil')
            embed.add_field(name='!perfil',value='Exibe o perfil de algum usuário')
            embed.add_field(name='!rep',value='Adiciona reputação (+rep) a um membro')
            embed.add_field(name='!nextbirthdays',value='Exibe os próximos 10 aniversários')
            embed.add_field(name='*!adminedit*',value='Edita o perfil de outro membro')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['role', 'roles', 'cargo', 'cargos']:
            embed = discord.Embed(title='Comandos de cargos', color=0x982ab4)
            embed.add_field(name='!register',value='Inicia o registro')
            await ctx.send(embed=embed)

        elif arg in ['tc', 'tempchannel', 'tempchannels', 'canaistemporarios', 'canais', 'temporarios']:
            embed = discord.Embed(title='Comandos dos canais temporários', color=0x982ab4)
            embed.add_field(name='!tccreate', value='Cria um canal temporário')
            embed.add_field(name='!tcdelete', value='Apaga seu canal temporário')
            embed.add_field(name='!tcadd', value='Adiciona membros ao seu canal temporário')
            embed.add_field(name='!tcremove', value='Remove membros de seu canal temporário')
            embed.add_field(name='!tctranscript', value='Cria uma transcrição das mensagens de seu canal temporário')
            embed.add_field(name='*!tcadelete*',value='Deleta um canal temporário de outro membro')
            embed.add_field(name='*!tcatranscript*',value='Cria uma transcrição de qualquer canal temporário')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['tickets', 'ticket', 'suporte', 'support']:
            embed = discord.Embed(title='Comandos dos tickets', color=0x982ab4)
            embed.add_field(name='!ticket',value='Inicia a criação do ticket')
            embed.add_field(name='*!tclose*',value='Fecha um ticket')
            embed.add_field(name='*!topen*',value='Reabre um ticket')
            embed.add_field(name='*!tdelete*',value='Apaga um ticket')
            embed.add_field(name='*!tadd*',value='Adiciona um membro ao ticket')
            embed.add_field(name='*!tremove*',value='Remove um membro do ticket')
            embed.add_field(name='*!trename*',value='Renomeia um ticket')
            embed.add_field(name='*!ttranscript*',value='Cria uma transcrição do ticket')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['info', 'informacoes', 'about', 'sobre', 'informations']:
            embed = discord.Embed(title='Comandos de informações', color=0x982ab4)
            embed.add_field(name='!avatar',value='Exibe o avatar de um membro')
            embed.add_field(name='!userbanner',value='Exibe o banner de um membro')
            embed.add_field(name='!userinfo',value='Exibe informações sobre um membro')
            embed.add_field(name='!servericon',value='Exibe o ícone do servidor')
            embed.add_field(name='!serverbanner',value='Exibe o banner do servidor')
            embed.add_field(name='!serverinfo',value='Exibe informações sobre o servidor')
            embed.add_field(name='!sobre',value='Exibe informações sobre o bot')
            await ctx.send(embed=embed)

        elif arg in ['misc', 'miscelanea', 'other', 'outro', 'outros', 'miscelaneous']:
            embed = discord.Embed(title='Comandos miscelâneos', color=0x982ab4)
            embed.add_field(name='!random',value='Gera um número aleatório')
            embed.add_field(name='!dado',value='Gera um número aleatório com o mínimo de 1')
            embed.add_field(name='!jankenpon',value='Joga pedra papel tesoura contra o computador')
            embed.add_field(name='!escolher',value='Escolhe um ítem entre dois ou mais')
            embed.add_field(name='!shorten',value='Encurta uma URL')
            embed.add_field(name='!remindme',value='Cria um lembrete')
            embed.add_field(name='*!poll*',value='Inicia uma votação')
            embed.add_field(name='*!say*',value='Envia uma mensagem usando o bot')
            embed.add_field(name='*!sayeveryone*',value='Envia uma mensagem usando o bot com @/everyone')
            embed.add_field(name='*!sayhere*',value='Envia uma mensagem usando o bot com @/here')
            embed.set_footer(text='Comandos em *itálico* necessitam cargo *`Manager`*')
            await ctx.send(embed=embed)

        elif arg in ['custom', 'customcommands', 'customizado']:
            embed = discord.Embed(title='Comandos customizados', color=0x982ab4)
            embed.add_field(name='*__!customcommand__*',value='Cria um comando customizado')
            embed.add_field(name='*__!ccdelete__*',value='Apaga um comando customizado')
            embed.add_field(name='!cclist',value='Lista os comandos customizados')
            for command in commands_table:
                embed.add_field(name=f'*{command.command}*',value=command.description)
            embed.set_footer(text='Comandos em *__sublinhado__* necessitam o cargo *`Manager`*, e em *itálico* são personalizados!')

        else:
            embed = discord.Embed(title='Lista de menus de ajuda', color=0x982ab4)
            embed.add_field(name='Economia',value='`!help economia`')
            embed.add_field(name='Sorteios',value='`!help sorteios`')
            embed.add_field(name='Níveis',value='`!help niveis`')
            embed.add_field(name='Moderação',value='`!help moderacao`')
            embed.add_field(name='Músicas',value='`!help musicas`')
            embed.add_field(name='Perfis',value='`!help perfis`')
            embed.add_field(name='Cargos',value='`!help cargos`')
            embed.add_field(name='Canais temporários',value='`!help tempchannels`')
            embed.add_field(name='Tickets',value='`!help tickets`')
            embed.add_field(name='Informações',value='`!help informacoes`')
            embed.add_field(name='Miscelânea',value='`!help miscelanea`')
            embed.add_field(name='Comandos criados',value='`!help custom`')
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))