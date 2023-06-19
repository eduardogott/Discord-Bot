import requests
import json
import datetime

class Countries:
    class RestCountryApiV31:
        BASE_URI = "https://restcountries.com/v3.1"
        QUERY_SEPARATOR = ";"
        VALID_CODES = [
        'AD', 'AE', 'AF', 'AG', 'AI', 'AL', 'AM', 'AO', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AW', 'AX', 'AZ', 'BA', 'BB', 'BD',
        'BE', 'BF', 'BG', 'BH', 'BI', 'BJ', 'BL', 'BM', 'BN', 'BO', 'BQ', 'BR', 'BS', 'BT', 'BV', 'BW', 'BY', 'BZ', 'CA',
        'CC', 'CD', 'CF', 'CG', 'CH', 'CI', 'CK', 'CL', 'CM', 'CN', 'CO', 'CR', 'CU', 'CV', 'CW', 'CX', 'CY', 'CZ', 'DE', 
        'DJ', 'DK', 'DM', 'DO', 'DZ', 'EC', 'EE', 'EG', 'EH', 'ER', 'ES', 'ET', 'FI', 'FJ', 'FK', 'FM', 'FO', 'FR', 'GA',
        'GB', 'GD', 'GE', 'GF', 'GG', 'GH', 'GI', 'GL', 'GM', 'GN', 'GP', 'GQ', 'GR', 'GS', 'GT', 'GU', 'GW', 'GY', 'HK',
        'HM', 'HN', 'HR', 'HT', 'HU', 'ID', 'IE', 'IL', 'IM', 'IN', 'IO', 'IQ', 'IR', 'IS', 'IT', 'JE', 'JM', 'JO', 'JP',
        'KE', 'KG', 'KH', 'KI', 'KM', 'KN', 'KP', 'KR', 'KW', 'KY', 'KZ', 'LA', 'LB', 'LC', 'LI', 'LK', 'LR', 'LS', 'LT',
        'LU', 'LV', 'LY', 'MA', 'MC', 'MD', 'ME', 'MF', 'MG', 'MH', 'MK', 'ML', 'MM', 'MN', 'MO', 'MP', 'MQ', 'MR', 'MS',
        'MT', 'MU', 'MV', 'MW', 'MX', 'MY', 'MZ', 'NA', 'NC', 'NE', 'NF', 'NG', 'NI', 'NL', 'NO', 'NP', 'NR', 'NU', 'NZ',
        'OM', 'PA', 'PE', 'PF', 'PG', 'PH', 'PK', 'PL', 'PM', 'PN', 'PR', 'PS', 'PT', 'PW', 'PY', 'QA', 'RE', 'RO', 'RS',
        'RU', 'RW', 'SA', 'SB', 'SC', 'SD', 'SE', 'SG', 'SH', 'SI', 'SJ', 'SK', 'SL', 'SM', 'SN', 'SO', 'SR', 'SS', 'ST',
        'SV', 'SX', 'SY', 'SZ', 'TC', 'TD', 'TF', 'TG', 'TH', 'TJ', 'TK', 'TL', 'TM', 'TN', 'TO', 'TR', 'TT', 'TV', 'TW',
        'TZ', 'UA', 'UG', 'UM', 'US', 'UY', 'UZ', 'VA', 'VC', 'VE', 'VG', 'VI', 'VN', 'VU', 'WF', 'WS', 'YE', 'YT', 'ZA',
        'ZM', 'ZW',  'ABW', 'AFG', 'AGO', 'AIA', 'ALA', 'ALB', 'AND', 'ARE', 'ARG', 'ARM', 'ASM', 'ATA', 'ATF', 'ATG',
        'AUS', 'AUT', 'AZE', 'BDI', 'BEL', 'BEN', 'BES', 'BFA', 'BGD', 'BGR', 'BHR', 'BHS', 'BIH', 'BLM', 'BLR', 'BLZ',
        'BMU', 'BOL', 'BRA', 'BRB', 'BRN', 'BTN', 'BVT', 'BWA', 'CAF', 'CAN', 'CCK', 'CHE', 'CHL', 'CHN', 'CIV', 'CMR',
        'COD', 'COG', 'COK', 'COL', 'COM', 'CPV', 'CRI', 'CUB', 'CUW', 'CXR', 'CYM', 'CYP', 'CZE', 'DEU', 'DJI', 'DMA',
        'DNK', 'DOM', 'DZA', 'ECU', 'EGY', 'ERI', 'ESH', 'ESP', 'EST', 'ETH', 'FIN', 'FJI', 'FLK', 'FRA', 'FRO', 'FSM',
        'GAB', 'GBR', 'GEO', 'GGY', 'GHA', 'GIB', 'GIN', 'GLP', 'GMB', 'GNB', 'GNQ', 'GRC', 'GRD', 'GRL', 'GTM', 'GUF',
        'GUM', 'GUY', 'HKG', 'HMD', 'HND', 'HRV', 'HTI', 'HUN', 'IDN', 'IMN', 'IND', 'IOT', 'IRL', 'IRN', 'IRQ', 'ISL',
        'ISR', 'ITA', 'JAM', 'JEY', 'JOR', 'JPN', 'KAZ', 'KEN', 'KGZ', 'KHM', 'KIR', 'KNA', 'KOR', 'KWT', 'LAO', 'LBN',
        'LBR', 'LBY', 'LCA', 'LIE', 'LKA', 'LSO', 'LTU', 'LUX', 'LVA', 'MAC', 'MAF', 'MAR', 'MCO', 'MDA', 'MDG', 'MDV',
        'MEX', 'MHL', 'MKD', 'MLI', 'MLT', 'MMR', 'MNE', 'MNG', 'MNP', 'MOZ', 'MRT', 'MSR', 'MTQ', 'MUS', 'MWI', 'MYS',
        'MYT', 'NAM', 'NCL', 'NER', 'NFK', 'NGA', 'NIC', 'NIU', 'NLD', 'NOR', 'NPL', 'NRU', 'NZL', 'OMN', 'PAK', 'PAN',
        'PCN', 'PER', 'PHL', 'PLW', 'PNG', 'POL', 'PRI', 'PRK', 'PRT', 'PRY', 'PSE', 'PYF', 'QAT', 'REU', 'ROU', 'RUS',
        'RWA', 'SAU', 'SDN', 'SEN', 'SGP', 'SGS', 'SHN', 'SJM', 'SLB', 'SLE', 'SLV', 'SMR', 'SOM', 'SPM', 'SRB', 'SSD',
        'STP', 'SUR', 'SVK', 'SVN', 'SWE', 'SWZ', 'SXM', 'SYC', 'SYR', 'TCA', 'TCD', 'TGO', 'THA', 'TJK', 'TKL', 'TKM',
        'TLS', 'TON', 'TTO', 'TUN', 'TUR', 'TUV', 'TWN', 'TZA', 'UGA', 'UKR', 'UMI', 'URY', 'USA', 'UZB', 'VAT', 'VCT',
        'VEN', 'VGB', 'VIR', 'VNM', 'VUT', 'WLF', 'WSM', 'YEM', 'ZAF', 'ZMB', 'ZWE']

        @classmethod
        def _get_country_list(cls, resource, term="", filters=None):
            filters_uri_string = ""
            if filters:
                filter_string = cls.QUERY_SEPARATOR.join(filters)
                filters_uri_string = "fields={}".format(filter_string)

            if term and not resource.endswith("="):
                term = "/{}".format(term)

            uri = "{}{}{}".format(cls.BASE_URI, resource, term)
            if filters:
                prefix = "?"
                if "?" in uri:
                    prefix = "&"
                uri += "{}{}".format(prefix, filters_uri_string)

            response = requests.get(uri)
            if response.status_code == 200:
                result_list = []
                data = json.loads(response.text)
                if type(data) == list:
                    for country_data in data:
                        country = Countries.Country(country_data)
                        result_list.append(country)
                else:
                    return Countries.Country(data)
                return result_list
            elif response.status_code == 404:
                raise requests.exceptions.InvalidURL
            else:
                raise requests.exceptions.RequestException

        @classmethod
        def get_all(cls, filters=None):
            """Returns all countries provided by  restcountries.eu.

                :param filters - a list of fields to filter the output of the request to include only the specified fields.
            """
            resource = "/all"
            return cls._get_country_list(resource, filters=filters)

        @classmethod
        def get_countries_by_name(cls, name, filters=None):
            """Returns a list of countries.

            :param name - Name string of a country. E.g. 'France'.
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/name"
            return cls._get_country_list(resource, name, filters=filters)

        @classmethod
        def get_countries_by_language(cls, language, filters=None):
            """Returns a list of countries.

            :param language - Language string of a country. E.g. 'en'.
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/lang"
            return cls._get_country_list(resource, language, filters=filters)

        @classmethod
        def get_countries_by_calling_code(cls, calling_code, filters=None):
            """Returns a list of countries.

            :param calling_code - Calling code string of a country. E.g. '1'.
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/callingcode"
            return cls._get_country_list(resource, calling_code, filters=filters)

        @classmethod
        def get_country_by_country_code(cls, alpha, filters=None):
            """Returns a `Country` object by alpha code.

            :param alpha - Alpha code string of a country. E.g. 'de'.
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: a Country object
            You can look those up at wikipedia: https://en.wikipedia.org/wiki/ISO_3166-1
            """
            resource = "/alpha"
            return cls._get_country_list(resource, alpha, filters=filters)

        @classmethod
        def get_countries_by_country_codes(cls, codes, filters=None):
            """Returns a list of countries.

            :param codes - List of strings which represent the codes of countries. E.g. ['us', 'ke']
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            You can look those up at wikipedia: https://en.wikipedia.org/wiki/ISO_3166-1
            :returns: list of Country objects
            """
            resource = "/alpha?codes="
            codes = cls.QUERY_SEPARATOR.join(codes)
            return cls._get_country_list(resource, codes, filters=filters)

        @classmethod
        def get_countries_by_currency(cls, currency, filters=None):
            """Returns a list of countries.

            :param currency - Currency string of a country. E.g. 'EUR'.
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/currency"
            return cls._get_country_list(resource, currency, filters=filters)

        @classmethod
        def get_countries_by_region(cls, region, filters=None):
            """Returns a list of countries.

            :param region - Region string of a country. E.g. 'Europe'.
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/region"
            return cls._get_country_list(resource, region, filters=filters)

        @classmethod
        def get_countries_by_subregion(cls, subregion, filters=None):
            """Returns a list of countries.

            :param subregion - Subregion string of a country. E.g. 'Western Europe'
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/subregion"
            return cls._get_country_list(resource, subregion, filters=filters)

        @classmethod
        def get_countries_by_capital(cls, capital, filters=None):
            """Returns a list of countries.

            :param capital - Capital string of a country. E.g. 'London'
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/capital"
            return cls._get_country_list(resource, capital, filters=filters)
        
        @classmethod
        def get_countries_by_demonym(cls, demonym, filters=None):
            """Returns a list of countries.

            :param capital - Capital string of a country. E.g. 'London'
            :param filters - a list of fields to filter the output of the request to include only the specified fields.
            :returns: list of Country objects
            """
            resource = "/demonym"
            return cls._get_country_list(resource, demonym, filters=filters)

    class Country:
        def __str__(self):
            return "{}".format(self.name)

        def __init__(self, country_data):
            self.alpha2_code = country_data.get('alpha2Code')
            self.alpha3_code = country_data.get('alpha3Code')
            self.alt_spellings = country_data.get('altSpellings')
            self.area = country_data.get('area')
            self.borders = country_data.get('borders')
            self.calling_codes = country_data.get('callingCodes')
            self.capital = country_data.get('capital')
            self.capital_coordinates = country_data.get('capitalInfo').get('latlng')
            self.car = country_data.get('car')
            self.car_sings = country_data.get('car').get('signs')
            self.driving_side = country_data.get('car').get('side')
            self.ioc_code = country_data.get('cioc')
            self.coat_of_arms = country_data.get('coatOfArms')
            self.continents = country_data.get('continents')
            self.demonyms = country_data.get('demonyms')
            self.demonym_female = country_data.get('demonyms').get('f')
            self.demonym_male = country_data.get('demonyms').get('m')
            self.independency_status = country_data.get('independent')
            self.fifa_code = country_data.get('fifa')
            self.flag_emoji = country_data.get('flag')
            self.flag = country_data.get('flags')
            self.flag_image_png = country_data.get('flags').get('png')
            self.flag_image_svg = country_data.get('flags').get('svg')
            self.flag_alt_explanation = country_data.get('flags').get('alt')
            self.gini = country_data.get('gini')
            self.landlocked = country_data.get('landlocked')
            self.languages = country_data.get('languages')
            self.coordinates = country_data.get('latlng')
            self.map = country_data.get('maps')
            self.name = country_data.get('name')
            self.name_official = country_data.get('name').get('official')
            self.name_common = country_data.get('name').get('common')
            self.native_name = country_data.get('name').get('nativeName')
            self.numeric_code = country_data.get('numericCode')
            self.population = country_data.get('population')
            self.postal_codes = country_data.get('postalCodes')
            self.region = country_data.get('region')
            self.iso_status = country_data.get('status')
            self.start_of_week = country_data.get('startOfWeek')
            self.subregion = country_data.get('subregion')
            self.timezones = country_data.get('timezones')
            self.tld = country_data.get('topLevelDomain')
            self.name_translations = country_data.get('translations')
            self.united_nations_member = country_data.get('unMember')
            self.currencies = country_data.get('currencies')
            self.all = country_data

        def __eq__(self, other):
            assert isinstance(other, Countries.Country)
            return self.numeric_code == other.numeric_code

        def __lt__(self, other):
            assert isinstance(other, Countries.Country)
            return self.numeric_code < other.numeric_code

        def __hash__(self):
            return int(self.numeric_code)

        def __str__(self):
            return "<{} | {}>".format(self.name, self.alpha3_code)

        def __repr__(self):
            return "<{} | {}>".format(self.name, self.alpha3_code)
        
class NASA:
    class NasaApodApi:
        BASE_URI = "https://api.nasa.gov/planetary/apod?"
        QUERY_SEPARATOR = "&"
        KEYS = {'date':datetime.datetime.today().strftime("%Y-%m-%d"), 'start_date': None, 'end_date':datetime.datetime.today().strftime("%Y-%m-%d"), 'count': None, 'thumbs':False, 'api_key': 'DEMO_KEY'}

        @classmethod
        def _get_nasa_apod(cls, date, start_date, end_date, count, thumbs, api_key):
            uri = f"{cls.BASE_URI}&{date}&{start_date}&{end_date}&{count}&{thumbs}&{api_key}"

            response = requests.get(uri)
            if response.status_code == 200:
                result_list = []
                data = json.loads(response.text)
                if type(data) == list:
                    for apod_data in data:
                        apod = NASA.APOD(apod_data)
                        result_list.append(apod)
                else:
                    return NASA.APOD(data)
                return result_list
            elif response.status_code == 404:
                raise requests.exceptions.InvalidURL
            else:
                raise requests.exceptions.RequestException

        @classmethod
        def get_apod(cls, **kwargs):
            """Returns the nasa APOD based on the kwargs given

            :param api_key - api.nasa.gov key for expanded usage and higher rate limits
            :param date - The date of the APOD image to retrieve
            :param start_date - The start of a date range, when requesting date for a range of dates. Cannot be used with date.
            :param end_date - The end of the date range, when used with start_date.
            :param count - If this is specified then count randomly chosen images will be returned. Cannot be used with date or start_date and end_date.
            :param thumbs - Return the URL of video thumbnail. If an APOD is not a video, this parameter is ignored.
            """
            k = cls.KEYS
            date = kwargs.get('date', k['date'])
            start_date = kwargs.get('start_date', k['start_date'])
            end_date = kwargs.get('end_date', k['end_date'])
            count = kwargs.get('count', k['count'])
            thumbs = kwargs.get('thumbs', k['thumbs'])
            api_key = kwargs.get('api_key', k['api_key'])

            return cls._get_nasa_apod(date, start_date, end_date, count, thumbs, api_key)

    class APOD:
        def __str__(self):
            return "{}".format(self.name)

        def __init__(self, data):
            self.is_copyrighted = True if data.get('copyright') else False
            self.copyright = data.get('copyright')
            self.date = data.get('date')
            self.explanation = data.get('explanation')
            self.hd_url = data.get('hdurl')
            self.type = data.get('media_type')
            self.service_version = data.get('service_version')
            self.title = data.get('title')
            self.url = data.get('url')
            self.all = data

        def __str__(self):
            return f"<{self.date} | {self.title}>"

        def __repr__(self):
            return f"<{self.date} | {self.title}>"
        
#class Spotify:
 #   class SpotifyAPI