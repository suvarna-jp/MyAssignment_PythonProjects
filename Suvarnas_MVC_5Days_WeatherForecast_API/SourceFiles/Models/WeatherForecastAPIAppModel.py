import requests
import sys
from SourceFiles.Commons.WeatherForecastAPIAppCommon import DEBUG_MODE
from SourceFiles.Commons.WeatherForecastAPIAppCommon import API_URL

API_CALL = API_URL


def getWeatherInfo(queryDict: dict):
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getWeatherInfo()")

    global API_CALL

    if (queryDict is None or len(queryDict) <= 0):
        if DEBUG_MODE:
            print(f"[EMPTY] :: queryDict is null or empty :: {queryDict}")
        return {'$NULL$', None}
    elif ('CITY_NAME' in queryDict.keys()):
        API_CALL += '&q=' + queryDict.get('CITY_NAME')
    elif ('CITY_ID' in queryDict.keys()):
        API_CALL += '&id=' + queryDict.get('CITY_ID')
    elif ('LAT_LON' in queryDict.keys()):
        API_CALL += '&lat=' + queryDict.get('LAT') + '&lon=' + queryDict.get('LON')
    elif ('ZIP_CODE' in queryDict.keys()):
        API_CALL += '&zip=' + queryDict.get('ZIP_CODE')
    else:
        if DEBUG_MODE:
            print(f"[ERROR] :: UNEXPECTED! Reached 'else' in queryDict check :: {queryDict}")
        return {'$ERROR$', None}


    if DEBUG_MODE:
        print(f"[DEBUG] :: API_CALL :: {API_CALL}")

    try:
        json_data = requests.get(API_CALL).json()
        if DEBUG_MODE:
            print(f"[DEBUG] :: In Model, JSON Data :: {json_data}")
        return json_data
    except:
        if DEBUG_MODE:
            print(f"[EXCEPT] :: Caught Exception during JSON call :: {sys.exc_info()}")
        return {'$EXCEPT$', sys.exc_info()}


# getWeatherInfo({'CITY_NAME': 'Paris 13e Arrondissement,EU'})

# JSON Data ::  {'cod': '200', 'message': 0.0117, 'cnt': 40,
# 'list': [{'dt': 1569196800, 'main': {'temp': 295.52, 'temp_min': 294.932, 'temp_max': 295.52,
# 'pressure': 1012.02, 'sea_level': 1012.02, 'grnd_level': 1003.8, 'humidity': 55, 'temp_kf': 0.59},
# 'weather': [{'id': 803, 'main': 'Clouds', 'description': 'broken clouds', 'icon': '04n'}],
# 'clouds': {'all': 60}, 'wind': {'speed': 4.09, 'deg': 229.934},
# 'sys': {'pod': 'n'}, 'dt_txt': '2019-09-23 00:00:00'}, {'dt': 1569207600,
# 'main': {'temp': 291.54, 'temp_min': 291.1, 'temp_max': 291.54,
# 'pressure': 1012.34, 'sea_level': 1012.34, 'grnd_level': 1003.98, 'humidity': 67, 'temp_kf': 0.44},
# 'weather': [{'id': 800, 'main': 'Clear', 'description': 'clear sky', 'icon': '01n'}],
# 'clouds': {'all': 1}, 'wind': {'speed': 4.25, 'deg': 255.381}, 'sys': {'pod': 'n'},
# 'dt_txt': '2019-09-23 03:00:00'}, {'dt': 1569218400,
# 'main': {'temp': 289.84, 'temp_min': 289.539, 'temp_max': 289.84,
# 'pressure': 1013.44, 'sea_level': 1013.44, 'grnd_level': 1005.61, 'humidity': 78, 'temp_kf': 0.3}, ........

# JSON Data ::  {'cod': '404', 'message': 'city not found'}