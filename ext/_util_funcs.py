import re
from discord.ext import commands
from colorama import Fore
from typing import Literal
from datetime import timedelta

language = "english.json" # Write the language EXACTLY as named in ./languages file!

def time_convert(seconds: int | timedelta, input: str = '', return_type: Literal['short', 'long', 'longpt'] = 'short') -> str:
    """Converts seconds to a time string.

        This function returns seconds in a (y, mo, w, d, h, m, s) format
        both short or long, in portuguese or english

        Parameters
        -----------
        seconds: :class:`int`
            The name of the field. Can only be up to 256 characters.
        input: :class:`str`
            Default "sec", can be changed to "min" for minutes input
        return_type: :class:`Literal["short", "long", "longpt"]`
            Return type, "longpt" for portuguese language
    """
    if isinstance(seconds, timedelta):
        seconds = int(seconds.total_seconds()) # Transform datetime in seconds if datetime is provided

    if input in ['min', 'minutes']:
        seconds *= 60 # Multiply minutes by 60 to turn it to seconds

    units = {'year': 31536000, 'month': 2592000, 'week': 604800, 'day': 86400, 'hour': 3600, 'minute': 60, 'second': 1}

    values = {}

    for unit, value in units.items():
        values[unit] = seconds // value # Does floor division for each unit
        seconds %= value # Perform a modulus operation for each unit

    match return_type:
        case 'short':
            return '{}{}{}{}{}{}{}'.format(str(values['year']) + 'y ' if values['year'] else '',
                                        str(values['month']) + 'mo ' if values['month'] else '',
                                        str(values['week']) + 'w ' if values['week'] else '',
                                        str(values['day']) + 'd ' if values['day'] else '',
                                        str(values['hour']) + 'h ' if values['hour'] else '',
                                        str(values['minute']) + 'm ' if values['minute'] else '',
                                        str(values['second']) + 's' if values['second'] else '').rstrip()

        case 'long':
            return '{}{}{}{}{}{}{}'.format(str(values['year']) + 'years ' if values['year'] else '',
                                        str(values['month']) + 'months ' if values['month'] else '',
                                        str(values['week']) + 'weeks ' if values['week'] else '',
                                        str(values['day']) + 'days ' if values['day'] else '',
                                        str(values['hour']) + 'hours ' if values['hour'] else '',
                                        str(values['minute']) + 'minutes ' if values['minute'] else '',
                                        str(values['second']) + 'seconds' if values['second'] else '').rstrip()

        case _:
            return '{}{}{}{}{}{}{}'.format(str(values['year']) + 'anos ' if values['year'] else '',
                                        str(values['month']) + 'meses ' if values['month'] else '',
                                        str(values['week']) + 'semanas ' if values['week'] else '',
                                        str(values['day']) + 'dias ' if values['day'] else '',
                                        str(values['hour']) + 'horas ' if values['hour'] else '',
                                        str(values['minute']) + 'minutos ' if values['minute'] else '',
                                        str(values['second']) + 'segundos' if values['second'] else '').rstrip()

def time_input_convert(time_string: str) -> int:
    """Convert "time_string" to seconds

        This functions takes time in format {int}(s/m/h/d/w/mo/y) and returns it in seconds.

        Parameters
        -----------
        time_string: :class:`str`
            The time string to be converted.
        """
    units = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400, 'w': 604800, 'mo': 2592000, 'y': 31536000}
    match = re.match(r'^(\d+)\s*(s|m|h|d|w|mo|y)$', time_string) # Checks if the time string is valid
   
    if match:
        time_value, time_unit = match.groups()
        time_value = int(time_value)
        return time_value * units[time_unit]
    return -1

async def role_handler(ctx, *roles: str) -> bool:
    """Checks if the member who used a function has one of the roles

        This function checks if a member who used a function has one of the roles

        Parameters
        -----------
        ctx: :class:`discord.ext.commands.Context`
            The function's (command's) context.
        roles: :class:`Tuple[discord.Role]`
            The roles to check if the member belongs to
        """
    try:
        if not any(role.name == _role for role in ctx.author.roles for _role in roles): # Checks if the member has any of the roles
            if len(roles) == 1:
                await ctx.send(f'Você não tem o cargo necessário {roles[0]}')
                return False
            else:
                await ctx.send(f'Você não tem nenhum dos cargos necessários: ({", ".join(roles)})')
                return False
        return True
    
    except commands.RoleNotFound as e: # If any of the roles does not exists it raises this error
        print(f'Cargo não encontrado: {e.argument}')
        await ctx.send('Erro, contate a equipe!')
        return False

async def permissions_handler(ctx, *perms: str, type: Literal['any', 'all'] = 'any', exempt_roles: list = []) -> bool:
    """Checks if the member who used a function has one/all of the perms

        This function checks if a member who used a function has one or all of the *perms

        Parameters
        -----------
        ctx: :class:`discord.ext.commands.Context`
            The function's (command's) context.
        perms: :class:`Tuple[discord.Permissions.*permission*]`
            The permissions to check if the member has them
        type: :class:`Literal["any", "all"] = "any"`
            Type of check, defaults to "any"
        exempt_roles: :class:`list`
            Exempt roles, if the member has any it returns true 
        """
    try:
        if any(role.name == _role for role in ctx.author.roles for _role in exempt_roles): 
            return True # Returns true if the member has any of the exempt roles
        
    except commands.RoleNotFound as e: # If a role does not exists this is performed
        print(f'Cargo não encontrado: {e.argument}')
        
    if type == 'any':
        if not len([perm for perm in perms if getattr(ctx.author.guild_permissions, perm)]):
            await ctx.send(f'Você não tem nenhuma das seguintes permissões: {", ".join(perms)}')
            return False # Checks if member has any of the permissions
        
    elif type == 'all':
        missing_perms = [perm for perm in perms if not getattr(ctx.author.guild_permissions, perm)]
        if not len(missing_perms): # Checks if member has all of the permissions
            return True 
        
        elif len(missing_perms) == 1:
            await ctx.send(f'Você não tem a seguinte permissão: {missing_perms[0]}')
            return False # Message for a singular missing permission
        
        else:
            await ctx.send(f'Você não tem as seguintes permissões: {", ".join(missing_perms)}')
            return False # Message for more than one missing permission
        
    else:
        print('Tipo inválido de permissão!') # Message for invalid permission given
        await ctx.send('Erro, contate a equipe!')
        return False

'''def dm_only_handler(aliases: list = []):
    def decorator(func):
        @commands.dm_only()
        async def wrapper(self, ctx, *args, **kwargs):
            try:
                await func(self, ctx, *args, **kwargs)
            except commands.PrivateMessageOnly:
                await ctx.send(f'Este comando só pode ser usado em conversas privadas (DM)!')
        return wrapper
    return decorator'''

meses = {1: 'janeiro',
         2: 'fevereiro',
         3: 'março',
         4: 'abril',
         5: 'maio',
         6: 'junho',
         7: 'julho',
         8: 'agosto',
         9: 'setembro',
         10: 'outubro',
         11: 'novembro',
         12: 'dezembro'}

class Log:
    """Used for logging errors, warnings and info without raising anything

        Methods
        -----------
        Log.error(place, message)

        Log.warning(place, message)

        Log.info(place, message)

        Parameters
        -----------
        place: :class:`str`
            Place in code where error occured

        message: :class:`str`
            Info about the error
        """
    def error(place, message):
        print(f'{Fore.RED} ERROR in {place}: {message}{Fore.RESET}')
    def warning(place, message):
        print(f'{Fore.YELLOW} WARNING in {place}: {message}{Fore.RESET}')
    def info(place, message):
        print(f'{Fore.BLUE} INFO in {place}: {message}{Fore.RESET}')