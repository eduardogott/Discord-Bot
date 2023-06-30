import discord
from discord.ext import commands
import requests
from all_apis import Countries as _countries
from sys import stdout
import nasapy
import datetime
 
countries = _countries.RestCountryApiV31
stdout.reconfigure(encoding='utf-8')

class CountriesAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    #! Traduzir languages, region e continent em um dict
    @commands.command(aliases=['country', 'countries', 'paises'])
    async def pais(self, ctx, code):
        if code not in countries.VALID_CODES:
            await ctx.send(f'Código inválido, veja os códigos válidos aqui: https://en.wikipedia.org/wiki/ISO_3166-1')
            rc = countries.get_country_by_country_code(code)[0]
            info = {'native_name': '\n'.join([f'{item[0]}: {item[2]} - ({item[1]})' for item in [(item, rc.native_name[item]['common'], rc.native_name[item]['official']) for item in rc.native_name]]),
            'currencies': '\n'.join([f'{item[0]} {item[1]} - ({item[2]})' for item in [(rc.currencies[item]['symbol'], item, rc.currencies[item]['name']) for item in rc.currencies]]),
            'capitals': ', '.join([item for item in rc.capitals]),
            'area': rc.area,
            'pop': rc.population,
            'density': rc.population / rc.area,
            'region': rc.region,
            'subregion': rc.subregion,
            'languages': ', '.join(rc.languages.values()),
            'borders': ', '.join(rc.borders),
            'demonym': {'m': {rc.demonym_male}, 'f': {rc.demonym_female}},
            'timezones': ', '.join(rc.timezones)}

            embed = discord.Embed(title=f'{rc.flag_emoji} Informações de {rc.name_translations["por"]["common"]} ({rc.name_translations["por"]["official"]})', color=0x982ab4)
            embed.add_field(name='Nome(s) nativo(s)', value=f'{info["native_names"]}')
            embed.add_field(name='Moeda(s) local(is)', value=f'{info["currencies"]}')
            embed.add_field(name='Capital(is)', value=f'{info["capitals"]}')
            embed.add_field(name='Área e população', value=f'Área: {info["area"]} km²\nPopulação: {info["pop"]}\nDensidade: {info["density"]} hab/km²')
            embed.add_field(name='Localização',value=f'Região: {info["region"]}\nSub-região: {info["subregion"]}')
            embed.add_field(name='Língua(s)', value=f'{info["languages"]}')
            embed.add_field(name='Fronteira(s)', value=f'{info["borders"]}')
            embed.add_field(name='Gentílico', value=f'Masculino: {info["demonym"]["m"]}\nFeminino: {info["demonym"]["f"]}')
            embed.add_field(name='Fuso(s) horário(s)', value=f'{info["timezones"]}')
            embed.set_thumbnail(url=f'{rc.flag_image_png}')
            embed.set_footer(text='Informações coletadas da API RESTCountries V3.1!')
            await ctx.send(embed=embed)

class NasaAPI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['nasaapod'])
    async def apod(self, ctx):
        n = nasapy.Nasa(key='HcgpXh8GXN36NJ8RchTvJLrKrzCJVjIYyMBGhjwj')
        picture = n.picture_of_the_day(datetime.datetime.today()-datetime.timedelta(days=1), hd=True)
        embed = discord.Embed(title=f'{picture.get("title")}', description=f'{picture.get("explanation")}')
        if picture.get('media_type') == 'image':
            embed.set_image(url=f'{picture.get("hdurl", picture.get("url"))}')
            embed.set_footer(text=f'NASA APOD do dia {picture["date"]}.')
            embed.url = f'{picture.get("hdurl", picture.get("url"))}'
        else:
            youtube_id = picture['url'].split('=')[-1]
            embed.set_image(url=f"https://img.youtube.com/vi/{youtube_id}/0.jpg")
            embed.set_footer(text=f'NASA APOD do dia {picture["date"]}. Clique aqui para assistir!')
            embed.url = picture['url']
        await ctx.send(embed=embed)
    
async def setup(bot):
    await bot.add_cog(CountriesAPI(bot))
    await bot.add_cog(NasaAPI(bot))