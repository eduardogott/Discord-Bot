import discord
from datetime import datetime, timedelta
import json
from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import random as rd
import asyncio

consecutive_daily_bonus = {
    1:(100,200),
    2:(115,215),
    3:(135,235),
    4:(160,260),
    5:(190,290),
    6:(225,325),
    7:(265,365),
    8:(310,410),
    9:(360,460),
    10:(400,500),
}

item_list = {'item1':{'name':'item1','shortdesc':'Anim qui quis ullamco ea voluptate occaecat.',
                      'flags':['consumable'],'uses':1,'actions':'giverole:Item1 Supremo'},
             'item2':{'name':'item2','shortdesc':'Veniam laboris amet mollit consectetur id elit veniam.',
                      'flags':['equipable'],'uses':-1,'actions':'giverole:Item2'},
             'item3':{'name':'item3','shortdesc':'Sint proident est esse officia amet culpa anim Lorem id ex.',
                      'flags':['consumable'],'uses':-1}}

shop_items = [{'name':'item1','shortdesc':'Anim qui quis ullamco ea voluptate occaecat.',
               'longdesc':'''Magna eu culpa consequat nostrud esse. Officia consectetur excepteur amet ut nisi laborum
                aute. Exercitation consectetur officia amet vel it excepteur. Cillum consequat consectetur fugiat eu
                aliqua labore non sunt excepteur qui nisi sint. Veniam qui mollit mollit voluptate duis consectetur.''',
                'price':1000,'flags':'i'},
              {'name':'item2','shortdesc':'Veniam laboris amet mollit consectetur id elit veniam.',
               'longdesc':'''Anim ex magna elit cillum qui culpa. Ipsum magna aliqua ipsum laboris magna.
                Laborum exercitation mollit aliqua exercitation. Duis pariatur aliqua esse excepteur sunt amet amet 
                reprehenderit amet. Quis anim Lorem nostrud irure irure eu labore exercitation.''',
                'price':2000,'flags':'e'},
              {'name':'item3','shortdesc':'Sint proident est esse officia amet culpa anim Lorem id ex.',
               'longdesc':'''Velit voluptate magna ut amet aliqua. Voluptate labore officia adipisicing excepteur
                laboris sit nulla in sint culpa elit esse aute. Cupidatat consectetur nisi ut laboris nisi.
                Nulla cupidatat sunt est deserunt deserunt occaecat aute est. Non ex ea aute deserunt
                proident ut id magna aliqua veniam ipsum. Ut consequat non ut et proident non excepteur 
                commodo labore consectetur cupidatat ipsum elit anim.''',
                'price':1500,'flags':'c'}]

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
economy_table = db.table('economy')

class Player:
    def __init__(self, player_id):
        self.id = player_id
        self.balance = 1
        self.last_daily = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.last_work_time = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")
        self.consecutive_daily = 0
        self.inventory = []

PlayerQuery = Query()

#? All optimised
class EconomyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['diario'])
    async def daily(self, ctx):
        player = economy_table.get(PlayerQuery.id == ctx.author.id)
        if player is None:
            player = Player(ctx.author.id)
            economy_table.insert({'id': player.id, 'balance': player.balance, 'last_daily': player.last_daily, 'last_work_time': player.last_work_time, 'consecutive_daily': player.consecutive_daily, 'inventory': player.inventory})
            player = economy_table.get(PlayerQuery.id == ctx.author.id)
        
        if datetime.datetime.now() - datetime.datetime.strptime(player["last_daily"], "%Y-%m-%d %H:%M:%S") > timedelta(days=1):
            player['consecutive_daily'] = min(player['consecutive_daily'], 10)
            coins = rd.randint(*consecutive_daily_bonus[player['consecutive_daily']])
            player['balance'] += coins
            player['consecutive_daily'] += 1
            player['last_daily'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            economy_table.update(player, PlayerQuery.id == ctx.author.id)
            await ctx.send(f"Você ganhou {coins} coins!")
        else:
            await ctx.send(f'Seu cooldown acaba em {((datetime.datetime.strptime(player["last_daily"], "%Y-%m-%d %H:%M:%S"))-datetime.datetime.now()).strftime("%H:%M:%S")}')

    @commands.command(aliases=['trabalhar'])
    async def work(self, ctx):
        player = economy_table.get(PlayerQuery.id == ctx.author.id)
        if player is None:
            player = Player(ctx.author.id)
            economy_table.insert({'id': player.id, 'balance': player.balance, 'last_daily': player.last_daily, 'last_work_time': player.last_work_time, 'consecutive_daily': player.consecutive_daily, 'inventory': player.inventory})
            player = economy_table.get(PlayerQuery.id == ctx.author.id)

        if datetime.datetime.now() - datetime.datetime.strptime(player["last_work_time"], "%Y-%m-%d %H:%M:%S") > timedelta(hours=2):
            coins = rd.randint(100, 200)
            player['balance'] += coins
            player['last_work_time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            economy_table.update(player, PlayerQuery.id == ctx.author.id)
            await ctx.send(f"Você ganhou {coins} coins! Volte em 2 horas para ganhar mais.")
        else:
            await ctx.send(f'Seu cooldown acaba em {((datetime.datetime.strptime(player["last_work_time"], "%Y-%m-%d %H:%M:%S"))-datetime.datetime.now()).strftime("%H:%M:%S")}')

    @commands.command(aliases=['money'])
    async def balance(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author

        player = economy_table.get(PlayerQuery.id == member.id)
        if player is None:
            await ctx.send('Membro não encontrado ou sem dinheiro!')
        else:
            await ctx.send(f'{member.display_name} possui {player["balance"]} coins!')
    
    @commands.command(aliases=['enviar', 'pagar', 'transferir'])
    async def pay(self, ctx, member: discord.Member = None, value = None):
        if not isinstance(member, discord.Member) or not isinstance(value, int):
            await ctx.send('Você precisa enviar um membro e um valor! Ex: !pay @Edu 1000')
            return
    
        from_player = economy_table.get(PlayerQuery.id == ctx.author.id)
        to_player = economy_table.get(PlayerQuery.id == member.id)
        if from_player is None:
            await ctx.send('Você não possui dinheiro!')
            return
        
        if to_player is None:
            player = Player(ctx.author.id)
            economy_table.insert({'id': player.id, 'balance': player.balance, 'last_daily': player.last_daily, 'last_work_time': player.last_work_time, 'consecutive_daily': player.consecutive_daily, 'inventory': player.inventory})
            to_player = economy_table.get(PlayerQuery.id == ctx.author.id)

        if from_player["balance"] < value:
            await ctx.send(f'Você não possui dinheiro suficiente (seu saldo: {from_player["balance"]})!')
            return
        
        from_player["balance"] -= value
        to_player["balance"] += value
        economy_table.update(from_player, PlayerQuery.id == ctx.author.id)
        economy_table.update(to_player, PlayerQuery.id == member.id)
        await ctx.send(f'Você enviou {value} coins para {member.display_name}!')

#? All optimised
class ItemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['loja'])
    async def shop(self, ctx, item = None):
        if item not in [item['name'] for item in shop_items] and (item-1 > len(shop_items) if isinstance(item, int) else True):
            embed = discord.Embed(title='Lista de ítens',color=0xFFD700)
            for i, item in enumerate(shop_items, start=1):
                embed.add_field(name=f'{i}. {item["name"]} - {item["price"]} coins', value=f'{item["shortdesc"]}', inline=False)
            
            await ctx.send(embed=embed)
        else:
            if isinstance(item, int):
                item = shop_items[int-1]
                embed = discord.Embed(title=f'Informações de {item["name"]}', color=0xFFD700)
                embed.add_field(name=f'Descrição', value=f'{item["longdesc"]}', inline=False)
                embed.add_field(name=f'Preço', value=f'{item["price"]} coins', inline=False)
                embed.set_footer(text=f'Para comprar digite !buy {item["name"]}')
            else:
                item = [_item for _item in shop_items if _item["name"] == item][0]
                embed = discord.Embed(title=f'Informações de {item["name"]}', color=0xFFD700)
                embed.add_field(name=f'Descrição', value=f'{item["longdesc"]}', inline=False)
                embed.add_field(name=f'Preço', value=f'{item["price"]} coins', inline=False)
                embed.set_footer(text=f'Para comprar digite !buy {item["name"]}')

    @commands.command(aliases=['comprar'])
    async def buy(self, ctx, item = None):
        player = economy_table.get(PlayerQuery.id == ctx.author.id)
        if player is None:
            player = Player(ctx.author.id)
            economy_table.insert({'id': player.id, 'balance': player.balance, 'last_daily': player.last_daily, 'last_work_time': player.last_work_time, 'consecutive_daily': player.consecutive_daily, 'inventory': player.inventory})
            player = economy_table.get(PlayerQuery.id == ctx.author.id)

        if item in [item['name'] for item in shop_items]:
            item = [_item for _item in shop_items if _item["name"] == item][0]
        elif (item-1 <= len(shop_items) if isinstance(item, int) else False):
            item = shop_items[int-1]
        else:
            await ctx.send('Ítem não encontrado!')

        if item["price"] > player["balance"]:
            await ctx.send('Você não possui dinheiro suficiente!')
        else:
            if item["name"] not in [item["name"] for item in player["inventory"]]:
                await ctx.send('Digite `confirmar` para confirmar, ou qualquer coisa para cancelar!')
                
                try:
                    message = await self.wait_for('message', timeout=30, check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
                    if message.content == 'confirmar':
                        player["balance"] -= item["price"]
                        player["inventory"].append(item_list[item["name"]])
                        economy_table.update(player, PlayerQuery.id == ctx.author.id)
                        await ctx.send(f'Você comprou {item["name"]} por {item["price"]}! Seu saldo agora é {player["balance"]}')
                    else:
                        await ctx.send('Compra cancelada!')
                        return
                except asyncio.TimeoutError:
                    await ctx.send('Tempo para confirmação expirado.')
            else:
                await ctx.send('Você já tem esse ítem em seu inventário!')

    #! Colocar quantidade de usos 
    @commands.command(aliases=['inv', 'inventario'])
    async def inventory(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.author
        
        player = economy_table.get(PlayerQuery.id == member.id)
        if player is None or not len(player["inventory"]):
            await ctx.send('Jogador não possui nenhum ítem no inventário.')
            return

        embed = discord.Embed(title=f'Inventário de {member.display_name}', color=0xFFD700)
        for item in player["inventory"]:
            command = f'!use {item["name"]}' if 'consumable' in item["flags"] else f'!equip {item["name"]}'
            action = 'usar' if 'consumable' in item["flags"] else 'equipar'
            embed.add_field(name=item["name"], value=f'{item["shortdesc"]}\n(Digite {command} para {action}!)')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['usar', 'consumir'])
    async def use(self, ctx, item = None):
        if item is None:
            await ctx.send('Você deve inserir um ítem para usar!')
            return
        
        player = economy_table.get(PlayerQuery.id == ctx.author.id)
        if player is None or player['inventory'] is None:
            await ctx.send('Você não possui ítens no inventário!')
            return
        
        if item not in [item['name'] for item in player['inventory']]:
            await ctx.send(f'Você não possui um ítem chamado {item}! Digite !inventory para ver seus ítens!')
            return
        
        inv_item = player['inventory'][item]
        if 'consumable' not in inv_item['flags']:
            await ctx.send(f'{inv_item["name"]} não é consumível! Digite !equip {item}.')
            return
        
        if inv_item['actions'].startswith('giverole'):
            role = discord.utils.get(ctx.guild.roles, name=inv_item['action'].split(':')[1])
            if role is None:
                await ctx.send(f'Não encontrei o cargo {inv_item["action"].split(":")[1]}! ||@Manager||')
                return
            
            await ctx.author.add_roles(role)
            await ctx.send(f'Você recebeu o cargo {role.name}!')

        if inv_item['uses'] == 1:
            player['inventory'].remove(inv_item)
        else:
            inv_item['uses'] -= 1 if inv_item >= 2 else 0
        
        economy_table.update(player, PlayerQuery.id == ctx.author.id)

    @commands.command(aliases=['equipar'])
    async def equip(self, ctx, item = None):
        if item is None:
            await ctx.send('Você deve inserir um ítem para usar!')
            return
        
        player = economy_table.get(PlayerQuery.id == ctx.author.id)
        if player is None or player['inventory'] is None:
            await ctx.send('Você não possui ítens no inventário!')
            return
        
        if item not in [item['name'] for item in player['inventory']]:
            await ctx.send(f'Você não possui um ítem chamado {item}! Digite !inventory para ver seus ítens!')
            return
        
        inv_item = player['inventory'][item]
        if 'equipable' not in inv_item['flags']:
            await ctx.send(f'{inv_item["name"]} não é equipável! Digite !use {item}.')
            return
        
        if inv_item['actions'].startswith('giverole'):
            role = discord.utils.get(ctx.guild.roles, name=inv_item['action'].split(':')[1])
            if role is None:
                await ctx.send(f'Não encontrei o cargo {inv_item["action"].split(":")[1]}! ||@Manager||')
                return
            
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.send(f'Removido o cargo {role.name}!')
            else:
                await ctx.author.add_roles(role)
                await ctx.send(f'Você recebeu o cargo {role.name}!')
               
        if inv_item['uses'] == 1:
            player['inventory'].remove(inv_item)
        else:
            inv_item['uses'] -= 1 if inv_item >= 2 else 0
        
        economy_table.update(player, PlayerQuery.id == ctx.author.id)

#? All optimised
class EconomyAdminCommands(commands.Cog):  
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role('Manager')
    async def eco(self, ctx, arg: str = None, member: discord.Member = None, value: int = None):
        if not isinstance(member, discord.Member) or not isinstance(value, int):
            await ctx.send('Você precisa enviar um membro e um valor! Ex: !eco (give/take/set/reset) @Edu 1000')
            return
        
        player = economy_table.get(PlayerQuery.id == member.id)
        if player is None:
            player = Player(member.id)
            economy_table.insert({'id': player.id, 'balance': player.balance, 'last_daily': player.last_daily, 'last_work_time': player.last_work_time, 'consecutive_daily': player.consecutive_daily, 'inventory': player.inventory})
            player = economy_table.get(PlayerQuery.id == member.id)
        
        old_player = player

        if arg == 'give':
            player['balance'] += value
            economy_table.update(player, PlayerQuery.id == member.id)
            await ctx.send(f'Adicionou {value} coins para {member.display_name}!')
        
        elif arg == 'take':
            if player['balance'] - value < 0:
                await ctx.send(f'O jogador irá ficar com o saldo negativo (saldo atual: {player["balance"]})')
                return
            
            player['balance'] -= value
            economy_table.update(player, PlayerQuery.id == member.id)
            await ctx.send(f'Removeu {value} coins de {member.display_name}!')

        elif arg == 'set':
            if 1000000 > value >= 0:
                player['balance'] = value
                economy_table.update(player, PlayerQuery.id == member.id)
                await ctx.send(f'Definiu o saldo de {member.display_name} para {value} (era {old_player["balance"]})!')
            else:
                await ctx.send(f'Insira um valor entre 0 e 1.000.000!')
        
        elif arg == 'reset':
            player['balance'] = 0
            economy_table.update(player, PlayerQuery.id == member.id)
            await ctx.send(f'Definiu o saldo de {member.display_name} para 0 (era {old_player["balance"]})!')
        
        else:
            await ctx.send('Argumento inválido, insira !eco (give/take/set/remove) \{@membro\} \{valor\}', delete_after = 15)
    
    #!Corrigir giveitem e takeitem
    @commands.command()
    @commands.has_role('Manager')
    async def giveitem(self, ctx, member: discord.Member = None, item = None):
        if isinstance(member, discord.Member) and ((item-1 <= len(shop_items) if isinstance(item, int) else False) or item in [_item["name"] for _item in shop_items]):
            player = economy_table.get(PlayerQuery.id == member.id)
            if player is None:
                player = Player(member.id)
                economy_table.insert({'id': player.id, 'balance': player.balance, 'last_daily': player.last_daily, 'last_work_time': player.last_work_time, 'consecutive_daily': player.consecutive_daily, 'inventory': player.inventory})
                player = economy_table.get(PlayerQuery.id == member.id)

            if isinstance(item, int):
                item = shop_items[item-1]
            else:
                item = [_item for _item in shop_items if _item["name"] == item][0]

            if item_list[item["name"]] not in [item['name'] for item in player["inventory"]]:
                player["inventory"].append(item_list[item["name"]])
                economy_table.update(player, PlayerQuery.id == member.id)
                await ctx.send(f'Você adicionou {item["name"]} ao inventário de {member.display_name}!')
            else:
                await ctx.send(f'{member.display_name} já possui esse ítem!')
        else:
            await ctx.send('Você deve mencionar um membro e um item! Ex: !giveitem @Edu item1')

    @commands.command()
    @commands.has_role('Manager')
    async def takeitem(self, ctx, member: discord.Member = None, item = None):
        if isinstance(member, discord.Member) and ((item-1 <= len(shop_items) if isinstance(item, int) else False) or item in [_item["name"] for _item in shop_items]):
            if member is None:
                await ctx.send('Você precisa inserir um membro!')
                return

            player = economy_table.get(PlayerQuery.id == member.id)
            if player is None or not len(player["inventory"]):
                await ctx.send('O membro não possui um inventário!')
                return
            
            if isinstance(item, int):
                item = shop_items[item-1]
            else:
                item = [_item for _item in shop_items if _item["name"] == item][0]

            if item_list[item["name"]] in [item['name'] for item in player["inventory"]]:
                player["inventory"].remove(item_list[item["name"]])
                economy_table.update(player, PlayerQuery.id == member.id)
                await ctx.send(f'Você removeu {item["name"]} do inventário de {member.display_name}!')
            else:
                await ctx.send(f'{member.display_name} não possui esse item!')
        else:
            await ctx.send('Você deve mencionar um membro e um item! Ex: !takeitem @Edu item1')

    @commands.command()
    @commands.has_role('Manager')
    async def clearinventory(self, ctx, member: discord.Member = None):
        if member is None:
            await ctx.send('Você precisa inserir um membro!')
            return
        
        player = economy_table.get(PlayerQuery.id == member.id)
        if player is None or not len(player["inventory"]):
            await ctx.send('O membro não possui um inventário!')
            return

        player["inventory"] = []
        economy_table.update(player, PlayerQuery.id == member.id)
        await ctx.send(f'O inventário de {member.display_name} foi limpo!')

async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))
    await bot.add_cog(ItemCommands(bot))
    await bot.add_cog(EconomyAdminCommands(bot))