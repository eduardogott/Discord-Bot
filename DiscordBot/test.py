from apis.countries import RestCountryApiV31 as rapi

rc = rapi.get_countries_by_country_codes(['LK'])[0]
print(rc.all)