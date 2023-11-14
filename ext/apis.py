import discord
from discord.ext import commands
import requests
from .all_apis import Countries as _countries
import nasapy # type: ignore
import datetime
from ._util_funcs import Log 

countries = _countries.RestCountryApiV31

class CountriesAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #! Traduzir languages, region e continent em um dict
    @commands.command(aliases=['country', 'countries', 'paises'])
    async def pais(self, ctx, code: str | None = None):
        if not isinstance(code, str):
            await ctx.send(f'Código inválido, veja os códigos válidos aqui: https://en.wikipedia.org/wiki/ISO_3166-1')
            return
        
        code = code.upper()
        if code in countries.VALID_CODES:
            rc, status_code, request_uri = countries.get_country_by_country_code(code)
            rc = rc[0] if isinstance(rc, list) else rc
        
        else:
            rc, status_code, request_uri = countries.get_countries_by_name(code)
            if rc is None:
                await ctx.send(f'Código/país inválido, veja os códigos válidos aqui: https://en.wikipedia.org/wiki/ISO_3166-1')
                return
            else:
                rc = rc[0] if isinstance(rc, list) else rc

        if status_code == 429:
            await ctx.send('Não foi possível obter informações sobre este país!')
            Log.error('ext/apis.CountriesAPI().pais()', f'RestCountries requests rate limit exceeded! (Status code {status_code})\nRequest URI: {request_uri}')
            return
        
        elif status_code != 200:
            await ctx.send('Não foi possível obter informações sobre este país!')
            Log.error('ext/apis.CountriesAPI().pais()', f'HTTP request to RestCountries not completed! (Status code {status_code})\nRequest URI: {request_uri}')
            return
        
        info = {'native_name': '\n'.join([f'{item[0]}: {item[2]} - ({item[1]})' for item in [(item, rc.native_name[item]['common'], rc.native_name[item]['official']) for item in rc.native_name]]),
        'currencies': '\n'.join([f'{item[0]} {item[1]} - ({item[2]})' for item in [(rc.currencies[item]['symbol'], item, rc.currencies[item]['name']) for item in rc.currencies]]) if len(rc.currencies) >= 1 else '',
        'capitals': ', '.join(rc.capital),
        'area': rc.area,
        'pop': rc.population if rc.population else 0,
        'density': round(rc.population / rc.area, 2),
        'region': rc.region,
        'subregion': rc.subregion,
        'languages': ', '.join(rc.languages.values()),
        'borders': ', '.join([countries.CODES_MAPPING[border] for border in rc.borders]) if isinstance(rc.borders, list) else rc.borders,
        'timezones': ', '.join(rc.timezones)}

        embed = discord.Embed(title=f'{rc.flag_emoji} Informações de {rc.name_translations["por"]["common"]} ({rc.name_translations["por"]["official"]})', color=0x982ab4)
        embed.add_field(name=':label: Nome(s) nativo(s)', value=f'{info["native_name"]}')
        embed.add_field(name=':coin: Moeda(s) local(is)', value=f'{info["currencies"]}')
        embed.add_field(name=':pushpin: Capital(is)', value=f'{info["capitals"]}')
        embed.add_field(name=':map: Área e população', value=f'**Área:** {info["area"]} km²\n**População:** {info["pop"]}\n**Densidade**: {info["density"]} hab/km²')
        embed.add_field(name=':earth_americas: Localização',value=f'**Região:** {info["region"]}\n**Sub-região:** {info["subregion"]}')
        embed.add_field(name=':speaking_head: Língua(s)', value=f'{info["languages"]}')
        embed.add_field(name=':construction: Fronteira(s)', value=f'{info["borders"]}')
        embed.add_field(name=':clock3: Fuso(s) horário(s)', value=f'{info["timezones"]}')
        embed.set_thumbnail(url=f'{rc.flag_image_png}')
        embed.set_footer(text='Informações coletadas da API RESTCountries V3.1')
        await ctx.send(embed=embed)

class NasaAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nasaapod'])
    async def apod(self, ctx):
        n = nasapy.Nasa(key='HcgpXh8GXN36NJ8RchTvJLrKrzCJVjIYyMBGhjwj')
        try:
            picture = n.picture_of_the_day(datetime.datetime.today()-datetime.timedelta(days=1), hd=True)
            embed = discord.Embed(title=f'{picture.get("title")}', description=f'{picture.get("explanation")}')
            if picture.get('media_type') == 'image':
                embed.set_image(url=f'{picture.get("hdurl", picture.get("url"))}')
                embed.set_footer(text=f'Foto Astronômica da NASA do dia {picture["date"]}.')
                embed.url = f'{picture.get("hdurl", picture.get("url"))}'
            else:
                youtube_id = picture['url'].split('=')[-1]
                embed.set_image(url=f"https://img.youtube.com/vi/{youtube_id}/0.jpg")
                embed.set_footer(text=f'NASA APOD do dia {picture["date"]}. Clique aqui para assistir!')
                embed.url = picture['url']
            await ctx.send(embed=embed)
        except requests.exceptions.HTTPError as e:
            await ctx.send('Não foi possível obter a foto astronômica do dia!')
            Log.error('ext/apis.NasaAPI().apod()', f'HTTP request to NASA not completed! (Error {e.args[0]})')
            return
        
async def setup(bot):
    await bot.add_cog(CountriesAPI(bot))
    await bot.add_cog(NasaAPI(bot))