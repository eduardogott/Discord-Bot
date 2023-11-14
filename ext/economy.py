'''ECONOMY EXTENSION

Commands included: [] = Optional, {} = Required, () = Choose one of, required
Commands preceded by @ are Manager only

daily - Claims daily bonus
work - Works each two hours to get money
balance [@member] - Display the user's balance
pay {@member} {value} - Transfer money to another member (10% tax)
shop [item name] - Display the shop or info about an item
buy {item name} - Buys an item from the shop
inventory [@member] - Shows a member's inventory
use {item name} - Uses an consumable item
equip {item name} - (Un)equips an equippable item
@eco (give/take/set/reset) {@member} {value} - Changes an member's balance
@giveitem {@member} {item name} - Gives an item to a member
@takeitem {@member} {item name} - Takes an item from a member's inventory
@clearinventory {@member} - Clears a member inventory

Info about how to create new items in the shop shown below
Aliases are listed in ../aliases.md'''

# TODO: Add item use cooldown

import discord
from datetime import datetime, timedelta
from discord.ext import commands, tasks
from tinydb import TinyDB, Query
import random as rd
import asyncio
from ._util_funcs import role_handler, time_convert

CONSECUTIVE_DAILY_BONUS: dict = {
    0:(100,200),
    1:(115,215),
    2:(135,235),
    3:(160,260),
    4:(190,290),
    5:(225,325),
    6:(265,365),
    7:(310,410),
    8:(360,460),
    9:(400,500),
} # Bonus for consecutive daily commands

item_list: dict[str, dict[str, object]] = {'item1':{'name':'item1','shortdesc':'Anim qui quis ullamco ea voluptate occaecat.',
                      'flags':['consumable'],'uses':1,'actions':'giverole:Item1 Supremo'},
             'item2':{'name':'item2','shortdesc':'Veniam laboris amet mollit consectetur id elit veniam.',
                      'flags':['equipable'],'uses':-1,'actions':'giverole:Item2', 'equipped': False},
             'item3':{'name':'item3','shortdesc':'Sint proident est esse officia amet culpa anim Lorem id ex.',
                      'flags':['consumable'],'uses':-1,'actions':'sendmessage:See if it works: it does!'},
             'everyone':{'name':'everyone','shortdesc':'Sends an everyone ping',
                      'flags':['consumable'],'uses':3,'actions':'sendmessage:%everyone% this is a test %member_id%'}} # Items list with short description
                # Names must match "shop_items" name key, negative uses for infinite

'''Key needs to be the same as 'name'
'name': Item name to be displayed at shop and inventory,
'shortdesc': A short description of the item,
'flags':['consumable'/'equipable'],
'uses': No. of uses (-1 for infinite),
'actions': Actions that'll be executed - Valid actions: "giverole:(role_name)"
'''

shop_items: list[dict[str, object]] = [{'name':'item1','shortdesc':'Anim qui quis ullamco ea voluptate occaecat.',
               'longdesc':'''Magna eu culpa consequat nostrud esse. Officia consectetur excepteur amet ut nisi laborum
                aute. Exercitation consectetur officia amet vel it excepteur. Cillum consequat consectetur fugiat eu
                aliqua labore non sunt excepteur qui nisi sint. Veniam qui mollit mollit voluptate duis consectetur.''',
                'price':1000,'flags':'consumable'},
              {'name':'item2','shortdesc':'Veniam laboris amet mollit consectetur id elit veniam.',
               'longdesc':'''Anim ex magna elit cillum qui culpa. Ipsum magna aliqua ipsum laboris magna.
                Laborum exercitation mollit aliqua exercitation. Duis pariatur aliqua esse excepteur sunt amet amet 
                reprehenderit amet. Quis anim Lorem nostrud irure irure eu labore exercitation.''',
                'price':2000,'flags':'equipable'},
              {'name':'item3','shortdesc':'Sint proident est esse officia amet culpa anim Lorem id ex.',
               'longdesc':'''Velit voluptate magna ut amet aliqua. Voluptate labore officia adipisicing excepteur
                laboris sit nulla in sint culpa elit esse aute. Cupidatat consectetur nisi ut laboris nisi.
                Nulla cupidatat sunt est deserunt deserunt occaecat aute est. Non ex ea aute deserunt
                proident ut id magna aliqua veniam ipsum. Ut consequat non ut et proident non excepteur 
                commodo labore consectetur cupidatat ipsum elit anim.''', 
                'price':1500,'flags':'consumable'},
              {'name':'everyone','shortdesc':'Sends an everyone ping',
               'longdesc':'''Sends an message containing an @/everyone ping, has 3 uses''',
               'price':3000,'flags':'consumable'}] # Items as they'll be displayed in the shop
                    # Items "name" must match item_list names

'''Item info to be displayed at the shop
'name': Item name to be displayed at the shop (must be the same as the item key in items_list)
'shortdesc': Short item description (recommended to be the same as shortdesc in items_list)
'longdesc': Long item description for when using the shop command to get details about it
'price': Price of the item in the shop
'flags': Either of 'consumable' or 'equipable'
'''

db = TinyDB('data.json', sort_keys=True, indent=2, separators=(',', ': '))
economy_table = db.table('economy')

def get_player(member: discord.Member):
    """Gets a player from database or creates one if it doesn't exist
    
    Parameters
    -----------
    member: :class:`discord.Member`
    Discord member for the user to be created
    """
    player = economy_table.get(PlayerQuery.id == member.id)
    if player is None:
        one_day_ago = (datetime.now()-timedelta(days = 1)).strftime("%Y-%m-%d %H:%M:%S")
        new_player_data = {'id': member.id, 'balance': 1, 'last_daily': one_day_ago,
                            'last_work_time': one_day_ago, 'consecutive_daily': 0, 'inventory': {}}
        
        economy_table.insert(new_player_data)
    
        player = economy_table.get(PlayerQuery.id == member.id)

    return Player(player)

class Player:
    def __init__(self, member):
        self.id = member['id']
        self.balance = member['balance']
        self.last_daily = member['last_daily']
        self.last_work_time = member['last_work_time']
        self.consecutive_daily = member['consecutive_daily']
        self.inventory = member['inventory']
    
    def add_money(self, amount):
        if self.balance + amount < 1000000:
            self.balance += amount
        else:
            self.balance = 1000000

        return True
    
    def take_money(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            return True
        
        return False

    def set_money(self, amount):
        if 1000000 >= amount >= 0:
            self.balance = amount
            return True
        
        return False
    
    def is_on_daily_cooldown(self):
        if datetime.now() - datetime.strptime(self.last_daily, "%Y-%m-%d %H:%M:%S") > timedelta(days=1):
            return False
        
        remaining_time = datetime.strptime(self.last_daily, "%Y-%m-%d %H:%M:%S") + timedelta(days=1) - datetime.now()

        return time_convert(remaining_time) # Convert the datetime to 00h 00m 00s representation

    def is_on_work_cooldown(self):
        if datetime.now() - datetime.strptime(self.last_work_time, "%Y-%m-%d %H:%M:%S") > timedelta(hours=2):
            return False
        
        remaining_time = datetime.strptime(self.last_work_time, "%Y-%m-%d %H:%M:%S") + timedelta(hours=2) - datetime.now()

        return time_convert(remaining_time) # Convert the datetime to 00h 00m 00s representation
    
    def update_daily_bonus(self):
        self.last_daily = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.consecutive_daily += 1 if self.consecutive_daily < 9 else 0

    def update_work_cooldown(self):
        self.last_work_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def give_item(self, item):
        self.inventory[item['name']] = item

    def take_item(self, item):
        del self.inventory[item]

    async def consume_item(self, ctx, item):
        inv_item = self.inventory[item]
        if inv_item['actions'].startswith('giverole'):
            role_name = inv_item['actions'].split(':')[1]
            role = discord.utils.get(ctx.guild.roles, name=role_name)

            if role is None:
                role = await ctx.guild.create_role(name=role_name)
            
            await ctx.author.add_roles(role)
            await ctx.send(f'Você recebeu o cargo {role.name}!')
        
        elif inv_item['actions'].startswith('sendmessage'):
            placeholders = {'%member_display_name%': ctx.author.display_name, '%member_name%': ctx.author.name,
                            '%member_id%': ctx.author.id, '%channel_id%': ctx.channel.id, '%everyone%': '@everyone',
                            '%here%': '@here'}
            
            message = inv_item['actions'].split(':', 1)[1]

            for k in placeholders.keys():
                message = message.replace(k, str(placeholders[k]))

            await ctx.send(message)

        if inv_item['uses'] == 1:
            self.take_item(item)

        else:
            self.inventory[item]['uses'] -= 1

    async def equip_item(self, ctx, item):
        inv_item = self.inventory[item]
        if inv_item['actions'].startswith('giverole'):
            role_name = inv_item['actions'].split(':')[1]
            role = discord.utils.get(ctx.guild.roles, name=role_name)

            if role is None:
                role = await ctx.guild.create_role(name=role_name)
            
            if role in ctx.author.roles:
                await ctx.author.remove_roles(role)
                await ctx.send(f'Você desequipou o cargo {role.name}!')
                self.inventory[item]['equipped'] = False
            else:
                await ctx.author.add_roles(role)
                await ctx.send(f'Você equipou o cargo {role.name}!')
                self.inventory[item]['equipped'] = True

    def clear_inventory(self):
        self.inventory = {}

    def update_database(self):
        economy_table.update({'id': self.id, 'balance': self.balance, 'last_daily': self.last_daily,
                              'last_work_time': self.last_work_time, 'consecutive_daily': self.consecutive_daily,
                              'inventory': self.inventory}, PlayerQuery.id == self.id)

PlayerQuery = Query()

#? All optimised
class EconomyCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['diario'])
    async def daily(self, ctx):
        player = get_player(ctx.author)

        cooldown = player.is_on_daily_cooldown()
        if cooldown is False:
            coins = rd.randint(*CONSECUTIVE_DAILY_BONUS[player.consecutive_daily])
            player.add_money(coins)

            player.update_daily_bonus()
            player.update_database()

            await ctx.send(f"Você ganhou {coins} coins!")

        else:
            await ctx.send(f'Seu cooldown acaba em {cooldown}')

    @commands.command(aliases=['trabalhar'])
    async def work(self, ctx):
        player = get_player(ctx.author)

        cooldown = player.is_on_work_cooldown()
        if cooldown is False:
            coins = rd.randint(100, 200)
            player.add_money(coins)

            player.update_work_cooldown()
            player.update_database()

            await ctx.send(f"Você ganhou {coins} coins! Volte em 2 horas para ganhar mais.")

        else:
            await ctx.send(f'Seu cooldown acaba em {cooldown}')

    @commands.command(aliases=['money', 'saldo', 'bal'])
    async def balance(self, ctx, member: discord.Member | None = None):
        if not isinstance(member, discord.Member):
            member = ctx.author

        player = get_player(member)
        await ctx.send(f'{member.display_name} possui {player.balance} coins!')
    
    @commands.command(aliases=['pagar', 'transferir'])
    async def pay(self, ctx, member: discord.Member | None = None, value: int | None = None):
        if not isinstance(member, discord.Member) or not isinstance(value, int):
            await ctx.send('Você precisa enviar um membro e um valor! Ex: !pay @Edu 1000')
            return
    
        from_player = get_player(ctx.author)
        to_player = get_player(member)

        if from_player.balance < value:
            await ctx.send(f'Você não possui dinheiro suficiente (seu saldo: {from_player.balance})!')
            return
        
        from_player.take_money(value)
        to_player.add_money(value*0.9)

        from_player.update_database()
        to_player.update_database()

        await ctx.send(f'Você enviou {value} ({value*0.9} com taxa de 10%) coins para {member.display_name}!')

#? All optimised
class ItemCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['loja'])
    async def shop(self, ctx, item = None):
        if item in [_item['name'] for _item in shop_items]: # If `item` is the name for a shop item
            item = [_item for _item in shop_items if _item["name"] == item][0]
            embed = discord.Embed(title=f'Informações de {item["name"]}', color=0xFFD700)
            embed.add_field(name=f'Descrição', value=f'{item["longdesc"]}', inline=False)
            embed.add_field(name=f'Preço', value=f'{item["price"]} coins', inline=False)
            embed.set_footer(text=f'Para comprar digite !buy {item["name"]}')

        else:
            embed = discord.Embed(title='Lista de ítens',color=0xFFD700)
            for i, item in enumerate(shop_items, start=1):
                embed.add_field(name=f'{i}. {item["name"]} - {item["price"]} coins', value=f'{item["shortdesc"]}', inline=False)

        await ctx.send(embed=embed)
                
    @commands.command(aliases=['comprar', ])
    async def buy(self, ctx, choice = None):
        player = get_player(ctx.author)

        item = next((_item for _item in shop_items if _item["name"] == choice), None) # Gives None if no item with that name is found

        if item is None:
            await ctx.send('Ítem não encontrado!')
            return
        
        if item["price"] > player.balance:
            await ctx.send('Você não possui dinheiro suficiente!')
            return

        if item["name"] in player.inventory:
            await ctx.send('Você já tem esse ítem em seu inventário!')
            return
        
        await ctx.send('Digite `confirmar` para confirmar, ou qualquer coisa para cancelar!')
        
        try:
            message = await self.bot.wait_for('message', timeout=30, check = lambda m: m.author == ctx.author and m.channel == ctx.channel)
            if message.content == 'confirmar':
                player.take_money(item['price'])
                player.give_item(item_list[item["name"]])
                player.update_database()

                await ctx.send(f'Você comprou {item["name"]} por {item["price"]}! Seu saldo agora é {player.balance}')
            else:
                await ctx.send('Compra cancelada!')
            
        except asyncio.TimeoutError:
            await ctx.send('Tempo para confirmação expirado.')        

    @commands.command(aliases=['inv', 'inventario'])
    async def inventory(self, ctx, member: discord.Member | None = None):
        if not isinstance(member, discord.Member):
            member = ctx.author
        
        player = get_player(member)
        if not len(player.inventory):
            await ctx.send('O membro não possui nenhum ítem no inventário.')
            return

        embed = discord.Embed(title=f'Inventário de {member.display_name}', color=0xFFD700)
        for _item in player.inventory:
            item = player.inventory[_item]
            if 'consumable' in item["flags"]:
                usos = item["uses"] if item["uses"] >= 0 else 'Ilimitado'
                embed.add_field(name=f'{item["name"]} (Usos: {usos})', value=f'{item["shortdesc"]}\n(Digite !use {item["name"]} para usar!)')
            else:
                equipped = "Sim" if item["equipped"] else "Não" 
                embed.add_field(name=f'{item["name"]} (Equipado: {equipped})', value=f'{item["shortdesc"]}\n(Digite !equip {item["name"]} para (des)equipar!)')
        
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['usar', 'consumir'])
    async def use(self, ctx, item = None):
        if item is None:
            await ctx.send('Você deve inserir um ítem para usar!')
            return
        
        player = get_player(ctx.author)
        if not player.inventory:
            await ctx.send('Você não possui ítens no inventário!')
            return
        
        if item not in player.inventory:
            await ctx.send(f'Você não possui um ítem chamado {item}! Digite !inventory para ver seus ítens!')
            return
        
        inv_item = player.inventory[item]
        if 'consumable' not in inv_item['flags']:
            await ctx.send(f'{inv_item["name"]} não é consumível! Digite !equip {item}.')
            return
        
        await player.consume_item(ctx, item)        
        player.update_database()

    @commands.command(aliases=['equipar'])
    async def equip(self, ctx, item = None):
        if item is None:
            await ctx.send('Você deve inserir um ítem para usar!')
            return
        
        player = get_player(ctx.author)
        if player.inventory is None:
            await ctx.send('Você não possui ítens no inventário!')
            return
        
        if item not in player.inventory:
            await ctx.send(f'Você não possui um ítem chamado {item}! Digite !inventory para ver seus ítens!')
            return
        
        inv_item = player.inventory[item]
        if 'equipable' not in inv_item['flags']:
            await ctx.send(f'{inv_item["name"]} não é equipável! Digite !use {item}.')
            return
        
        await player.equip_item(ctx, item)
        player.update_database()

#? All optimised
class EconomyAdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eco(self, ctx, arg: str = '', member: discord.Member | None = None, value: int = 0):
        if await role_handler(ctx, 'Manager') is False: return
        
        if not isinstance(member, discord.Member) or not isinstance(value, int):
            await ctx.send('Você precisa enviar um membro e um valor! Ex: !eco (give/take/set/reset) @Edu 1000')
            return
        
        if value <= 0 and arg != 'reset':
            await ctx.send('O valor deve ser maior que 0')
            return

        player = get_player(member)
        
        old_player_balance = player.balance

        if arg == 'give':
            player.add_money(value)
            player.update_database()
            await ctx.send(f'Adicionou {value} coins para {member.display_name}!')
        
        elif arg == 'take':
            ans = player.take_money(value)
            if ans is False:
                await ctx.send(f'O jogador irá ficar com o saldo negativo (saldo atual: {player["balance"]})')
                return
            
            player.update_database()
            await ctx.send(f'Removeu {value} coins de {member.display_name}!')

        elif arg == 'set':
            ans = player.set_money(value)
            if ans is False:
                await ctx.send(f'Insira um valor entre 0 e 1.000.000!')
                return
            
            await ctx.send(f'Definiu o saldo de {member.display_name} para {value} (era {old_player_balance})!')
            player.update_database()
                
        
        elif arg == 'reset':
            player.set_money(1)
            player.update_database()
            await ctx.send(f'Definiu o saldo de {member.display_name} para 0 (era {old_player_balance})!')
        
        else:
            await ctx.send('Argumento inválido, insira !eco (give/take/set/remove) {@membro} {valor}', delete_after = 15)
    
    @commands.command()
    async def giveitem(self, ctx, member: discord.Member | None = None, item = None):
        if await role_handler(ctx, 'Manager') is False: return
        
        if not isinstance(member, discord.Member):
            await ctx.send('Você deve mencionar um membro e um item! Ex: !giveitem @Edu item1')
            return
        
        player = get_player(member)
        if isinstance(item, int) and item <= len(shop_items):
            item = shop_items[item-1]
        
        else:
            item = next((_item for _item in shop_items if _item["name"] == item), None) # Gives None if no item with that name is found

        if item is None:
            await ctx.send('Ítem não encontrado!')
            return

        member_item_names = [item for item in player.inventory]
        if item_list[item["name"]] not in member_item_names:
            player.give_item(item_list[item["name"]])
            player.update_database()
            await ctx.send(f'Você adicionou {item["name"]} ao inventário de {member.display_name}!')

        else:
            await ctx.send(f'{member.display_name} já possui esse ítem!')

    @commands.command()
    async def takeitem(self, ctx, member: discord.Member | None = None, item = None):
        if await role_handler(ctx, 'Manager') is False: return
        
        if not isinstance(member, discord.Member):
            await ctx.send('Você deve mencionar um membro e um item! Ex: !takeitem @Edu item1')
            return

        player = get_player(member)
        if not player.inventory:
            await ctx.send('O inventário do membro está vazio!')
            return                

        if item in player.inventory.keys():
            player.take_item(item)
            player.update_database()
            await ctx.send(f'Removeu {item} do inventário de {member.display_name}!')

        else:
            await ctx.send(f'{member.display_name} não possui esse item!')

    @commands.command()
    async def clearinventory(self, ctx, member: discord.Member | None = None):
        if await role_handler(ctx, 'Manager') is False: return

        if not isinstance(member, discord.Member):
            await ctx.send('Você precisa inserir um membro!')
            return
        
        player = get_player(member)
        if not player.inventory:
            await ctx.send('O membro não possui um inventário!')
            return

        player.clear_inventory()
        player.update_database()
        await ctx.send(f'O inventário de {member.display_name} foi limpo!')

async def setup(bot):
    await bot.add_cog(EconomyCommands(bot))
    await bot.add_cog(ItemCommands(bot))
    await bot.add_cog(EconomyAdminCommands(bot))