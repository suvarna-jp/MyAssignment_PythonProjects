from SourceFiles.Commons.WeatherForecastAPIAppCommon import DEBUG_MODE, MY_NAME
from SourceFiles.Views import WeatherForecastAPIAppView as wfaView
from SourceFiles.Models import WeatherForecastAPIAppModel as wfaModel
WEATHER_FORECAST_API_APP_RUNNING = True


def handleWeatherAPIResponse(api_response_dict:dict):
    """This function handles the weather forecast to be shown to the user appropriately """
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getWeatherInfo()")

    if(api_response_dict is None):
        if DEBUG_MODE:
            print("[ERROR] :: Unexpected null value for api_response_dict...")
        wfaView.showMessagesToUser(["[ERROR] :: Unexpected error occured. Please contact Admin."])
        executeWeatherForecastApp()


    if(api_response_dict.get('cod') == '200'):
        wfaView.showMessagesToUser(["\n\n**********************************************************************"])

        if ('city' in api_response_dict.keys()):
            city_dict = api_response_dict.get('city')
            if ('id' in city_dict.keys()):
                wfaView.showMessagesToUser([f"City ID :: {city_dict.get('id')}"])
            if ('name' in city_dict.keys()):
                wfaView.showMessagesToUser([f"City Name :: {city_dict.get('name')}"])
            if ('country' in city_dict.keys()):
                wfaView.showMessagesToUser([f"Country :: {city_dict.get('country')}"])
            if ('population' in city_dict.keys()):
                wfaView.showMessagesToUser([f"Population :: {city_dict.get('population')}"])
            if ('sunrise' in city_dict.keys()):
                wfaView.showMessagesToUser([f"Sunrise :: {city_dict.get('sunrise')}"])
            if ('sunset' in city_dict.keys()):
                wfaView.showMessagesToUser([f"Sunset :: {city_dict.get('sunset')}"])
            if ('timezone' in city_dict.keys()):
                wfaView.showMessagesToUser([f"Timezone :: {city_dict.get('timezone')}"])
            if ('coord' in city_dict.keys()):
                coord_dict = city_dict.get('coord')
                if ('lat' in coord_dict.keys()):
                    wfaView.showMessagesToUser([f"Latitude :: {coord_dict.get('lat')}"])
                if ('lon' in coord_dict.keys()):
                    wfaView.showMessagesToUser([f"Longitude :: {coord_dict.get('lon')}"])

        response_list = api_response_dict.get('list')
        for list_dict in response_list:
            wfaView.showMessagesToUser(["\n\n================================================================="])
            if ('id' in list_dict.keys()):
                wfaView.showMessagesToUser([f"City ID :: {list_dict.get('id')}"])
            if ('name' in list_dict.keys()):
                wfaView.showMessagesToUser([f"City Name :: {list_dict.get('name')}"])
            if ('id' in list_dict.keys()):
                wfaView.showMessagesToUser([f"City ID :: {list_dict.get('id')}"])
            if ('name' in list_dict.keys()):
                wfaView.showMessagesToUser([f"City Name :: {list_dict.get('name')}"])
            if ('city' in list_dict.keys()):
                city_dict = list_dict.get('city')
                if ('id' in city_dict.keys()):
                    wfaView.showMessagesToUser([f"Temperature :: {city_dict.get('id')}"])
                if ('name' in city_dict.keys()):
                    wfaView.showMessagesToUser([f"Minimum Temperature :: {city_dict.get('name')}"])
            if ('coord' in list_dict.keys()):
                coord_dict = list_dict.get('coord')
                if ('lat' in coord_dict.keys()):
                    wfaView.showMessagesToUser([f"Latitude :: {coord_dict.get('lat')}"])
                if ('lon' in coord_dict.keys()):
                    wfaView.showMessagesToUser([f"Longitude :: {coord_dict.get('lon')}"])
            wfaView.showMessagesToUser(["================================================================="])
            if ('dt' in list_dict.keys()):
                wfaView.showMessagesToUser([f"Date Code :: {list_dict.get('dt')}"])
            if ('dt_txt' in list_dict.keys()):
                date, time = list_dict.get('dt_txt').split(' ')
                wfaView.showMessagesToUser([f"Date :: {date}"])
                wfaView.showMessagesToUser([f"Time :: {time}"])
                wfaView.showMessagesToUser(["----------------------------------------------------------------"])
            if ('main' in list_dict.keys()):
                main_dict = list_dict.get('main')
                if ('temp' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Temperature :: {main_dict.get('temp')}"])
                if ('temp_min' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Minimum Temperature :: {main_dict.get('temp_min')}"])
                if ('temp_max' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Maximum Temperature :: {main_dict.get('temp_max')}"])
                if ('pressure' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Air Pressure :: {main_dict.get('pressure')}"])
                if ('sea_level' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Sea Level :: {main_dict.get('sea_level')}"])
                if ('grnd_level' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Ground Level :: {main_dict.get('grnd_level')}"])
                if ('humidity' in main_dict.keys()):
                    wfaView.showMessagesToUser([f"Humidity :: {main_dict.get('humidity')}"])
                    wfaView.showMessagesToUser(["----------------------------------------------------------------"])
            if ('weather' in list_dict.keys()):
                weather_list = list_dict.get('weather')
                for weather_dict in weather_list:
                    if ('main' in weather_dict.keys()):
                        wfaView.showMessagesToUser([f"Weather is :: {weather_dict.get('main')}"])
                    if ('description' in weather_dict.keys()):
                        wfaView.showMessagesToUser([f"Weather description :: {weather_dict.get('description')}"])
            if ('clouds' in list_dict.keys()):
                clouds_dict = list_dict.get('clouds')
                if ('all' in clouds_dict.keys()):
                    wfaView.showMessagesToUser([f"Clouds :: {clouds_dict.get('clouds_dict')}"])
            if ('wind' in list_dict.keys()):
                wind_dict = list_dict.get('wind')
                if ('speed' in wind_dict.keys()):
                    wfaView.showMessagesToUser([f"Wind Speed :: {wind_dict.get('speed')}"])
                if ('deg' in wind_dict.keys()):
                    wfaView.showMessagesToUser([f"Wind Degree :: {wind_dict.get('deg')}"])
                    wfaView.showMessagesToUser(["----------------------------------------------------------------\n"])



def executeWeatherForecastApp():
    """This function executes the main functionality to get the weather info based on user's input """
    if DEBUG_MODE:
        print("[DEBUG] :: Inside getWeatherInfo()")

    # Calling the View's getCityInfo  12.9762 77.6033
    city_info = wfaView.getCityInfo()
    if DEBUG_MODE:
        print(f"[DEBUG] :: city_info :: {city_info}")

    if (city_info == None):
        if DEBUG_MODE:
            print("[ERROR] :: Unexpected null value for city_info...")
        wfaView.showMessagesToUser(["[ERROR] :: Unexpected error occured. Please contact Admin."])
        executeWeatherForecastApp()
    elif (type(city_info) == str and city_info == '$EXIT$'):
        wfaView.showMessageBeforeAppExit()
        return
    elif (type(city_info) == dict):
        if DEBUG_MODE:
            print("[DEBUG] :: city_info is a dict.. Calling Model")

        api_response = wfaModel.getWeatherInfo(city_info)
        if DEBUG_MODE:
            print(f"[DEBUG] :: api_response :: {api_response}")

        if(api_response is None or type(api_response) != dict or '$NULL$' in api_response.keys() or '$ERROR$' in api_response.keys()):
            if DEBUG_MODE:
                print("[ERROR] :: Unexpected | api_response is null/not a dict...")
            wfaView.showMessagesToUser(["[ERROR] :: Unexpected error occured. Please contact Admin."])
            executeWeatherForecastApp()
        elif('$EXCEPT$' in api_response.keys()):
            if DEBUG_MODE:
                print(f"[EXCEPT] :: Exception Occured!! Exception :: {api_response.get('$EXCEPT$')}")
            wfaView.showMessagesToUser(["[ERROR] :: Unexpected error occured. Please contact Admin."])
            executeWeatherForecastApp()
        elif('cod' in api_response.keys()):
            if DEBUG_MODE:
                print(f"[DEBUG] :: cod found in api_response.keys() :: {api_response.keys()}")
            handleWeatherAPIResponse(api_response)
        else:
            if DEBUG_MODE:
                print("[DEBUG] :: Unexpected api_response :: {api_response}")
            wfaView.showMessagesToUser(["[ERROR] :: Unexpected error occured. Please contact Admin."])
            executeWeatherForecastApp()

    else:
        if DEBUG_MODE:
            print("[ERROR] :: Unexpected | in else | of city_info check...")
        wfaView.showMessagesToUser(["[ERROR] :: Unexpected error occured. Please contact Admin."])
        executeWeatherForecastApp()

while WEATHER_FORECAST_API_APP_RUNNING:
    wfaView.showMessagesToUser([f"[WELCOME] :: WELCOME! To {MY_NAME} Terminal Weather Forecast App!!",
                                "Dear, User!",
                                "How can I help you..."])
    executeWeatherForecastApp()

if __name__ == '__main__':
    if DEBUG_MODE:
        print('Terminal Weather Forecast App - started from commandline')
    wfaView.showMessagesToUser([f"[WELCOME] :: WELCOME! To {MY_NAME} Terminal Weather Forecast App!!",
                                "Dear, User!",
                                "How can I help you..."])
    executeWeatherForecastApp()
else:
    if DEBUG_MODE:
        print('Terminal Weather Forecast App - Imported as a module')
    wfaView.showMessagesToUser([f"[WELCOME] :: WELCOME! To {MY_NAME} Terminal Weather Forecast App!!",
                                "Dear, User!",
                                "How can I help you..."])
    executeWeatherForecastApp()