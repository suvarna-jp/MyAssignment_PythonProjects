DEBUG_MODE = False
MY_NAME = 'Suvarna\'s'
# $EXIT$
# $NULL$

COUNTRY_CODE_SEARCH_URL = 'https://www.iso.org/obp/ui/#search'
COUNTRY_CODE_SEARCH_URL_2 = 'https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes'

API_KEY = 'c0481e024d0a214b36eadfdd845b26c5'
API_URL = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + API_KEY

# By city name
# Description:
# You can search weather forecast for 5 days with data every 3 hours by city name.
# All weather data can be obtained in JSON and XML formats.
# There is a possibility to receive a central district of the city/town
# with its own parameters (geographic coordinates/id/name) in API response.
# API call:
# api.openweathermap.org/data/2.5/forecast?q={city name},{country code}
# Parameters:
# q city name and country code divided by comma, use ISO 3166 country codes
# Examples of API calls:
# API_URL_CITY_NAME = 'https://api.openweathermap.org/data/2.5/forecast?q=London,us&mode=xml'

# By city ID
# Description:
# You can search weather forecast for 5 days with data every 3 hours by city ID.
# API responds with exact result. All weather data can be obtained in JSON and XML formats.
# API call:
# api.openweathermap.org / data / 2.5 / forecast?id = {city ID}
# Examples of API calls:
# API_URL_CITY_ID = 'https://api.openweathermap.org/data/2.5/forecast?id=524901'

# By geographic coordinates
# Description:
# You can search weather forecast for 5 days with data every 3 hours by geographic coordinates.
# All weather data can be obtained in JSON and XML formats.
# API call:
# api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}
# Examples of API calls:
# API_URL_GEO_CO_ORDINATES = 'https://api.openweathermap.org/data/2.5/forecast?lat=35&lon=139'

# By ZIP code
# Description:
# Please note if country is not specified then the search works for USA as a default.
# API call:
# api.openweathermap.org/data/2.5/forecast?zip={zip code},{country code}
# Examples of API calls:
# API_URL_ZIP_CODE = 'https://api.openweathermap.org/data/2.5/forecast?zip=94040,us'
