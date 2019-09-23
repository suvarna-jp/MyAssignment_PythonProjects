from SourceFiles.Commons.WeatherForecastAPIAppCommon import DEBUG_MODE, COUNTRY_CODE_SEARCH_URL
from SourceFiles.Validations.WeatherForecastAPIValidations import is_city, is_country_code, is_city_id, is_lat_lon, is_zip_code

def showMessagesToUser(msgsList):
    """This function displays messages to the user
    @:param List - List of String messages"""

    if (msgsList != None and len(msgsList) > 0):
        for msg in msgsList:
            print(msg)


def searchByCityName():
    """This function fetches the city name from user
            @:return {'CITY_NAME' : <cityName>,<countryCode>} dictionary"""

    if DEBUG_MODE:
        print("[DEBUG] :: Inside searchByCityName()")

    cityFlag = True
    countryFlag = True
    city_name = None
    country_code = None

    while cityFlag:
        print("[MESSAGE] :: You can search weather forecast for 5 days with data every 3 hours by city name.")
        city_name = input("\n[INPUT] :: Please enter a City name :: ")

        if(city_name == None or city_name.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            print("[MESSAGE] :: Enter '$EXIT$' to exit back to menu. ")
            continue
        elif (city_name.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_city(city_name) == False):
            print("[INVALID] :: Some special characters are invalid in a City name. "
                  "\nPlease enter a valid city name.")
            continue
        else:
            city_name = city_name.strip()
            cityFlag = False
            break

    while countryFlag:
        print("\n[MESSAGE] :: Use ISO 3166 two-letter country code.")
        print(f"[MESSAGE] :: To know the country code go to {COUNTRY_CODE_SEARCH_URL}")
        country_code = input("\n[INPUT] :: Please enter a two-letter country code :: ")

        if(country_code == None or country_code.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            continue
        elif (country_code.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_country_code(country_code.strip()) == False):
            print("[INVALID] :: Special characters or <space> are invalid in a Country code. "
                  "\nPlease enter a valid Country code.")
            continue
        else:
            country_code = country_code.strip()
            countryFlag = False
            break

    return {"CITY_NAME" : f"{city_name},{country_code}"}


def searchByCityID():
    """This function fetches the city ID from user
            @:return {'CITY_ID' : <cityID>,<countryCode>} dictionary"""

    if DEBUG_MODE:
        print("[DEBUG] :: Inside searchByCityID()")

    cityIDFlag = True
    city_id = None

    while cityIDFlag:
        print("[MESSAGE] :: You can search weather forecast for 5 days with data every 3 hours by City ID.")
        city_id = input("\n[INPUT] :: Please enter a City ID :: ")

        if(city_id == None or city_id.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            print("[MESSAGE] :: Enter '$EXIT$' to exit back to menu. ")
            continue
        elif (city_id.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_city_id(city_id) == False):
            print("[INVALID] :: Some special characters are invalid in a City ID. "
                  "\nPlease enter a valid city ID.")
            continue
        else:
            city_id = city_id.strip()
            cityIDFlag = False
            break

    return {"CITY_ID" : f"{city_id}"}


def searchByGeographicalCoordinates():
    """This function fetches the Geographical Coordinates from user
            @:return {'LAT_LON' : None, 'LAT' : <latitude>, 'LON' : <longitude>} dictionary"""

    if DEBUG_MODE:
        print("[DEBUG] :: Inside searchByGeographicalCoordinates()")

    latFlag = True
    lonFlag = True
    latitude = None
    longitude = None

    while latFlag:
        print("[MESSAGE] :: You can search weather forecast for 5 days with data every 3 hours "
              "by Geographical Coordinates.")
        latitude = input("\n[INPUT] :: Please enter Latitude :: ")

        if(latitude == None or latitude.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            print("[MESSAGE] :: Enter '$EXIT$' to exit back to menu. ")
            continue
        elif (latitude.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_lat_lon(latitude) == False):
            print("[INVALID] :: Some special characters are invalid in a Latitude. "
                  "\nPlease enter a valid Latitude.")
            continue
        else:
            latitude = latitude.strip()
            latFlag = False
            break

    while lonFlag:
        longitude = input("\n[INPUT] :: Please enter Longitude :: ")

        if(longitude == None or longitude.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            continue
        elif (longitude.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_lat_lon(longitude.strip()) == False):
            print("[INVALID] :: Special characters or <space> are invalid in a Country code. "
                  "\nPlease enter a valid Country code.")
            continue
        else:
            longitude = longitude.strip()
            lonFlag = False
            break

    # return {"CITY_NAME" : f"{city_name},{country_code}"}
    return {f'LAT_LON': None, 'LAT': latitude, 'LON': longitude}


def searchByZipCode():
    """This function fetches the Zip code from user
            @:return {'ZIP_CODE' : <zipCode>,<countryCode>} dictionary"""

    if DEBUG_MODE:
        print("[DEBUG] :: Inside searchByZipCode()")

    zipFlag = True
    countryFlag = True
    zip_code = None
    country_code = None

    while zipFlag:
        print("[MESSAGE] :: You can search weather forecast for 5 days with data every 3 hours by Zip code.")
        zip_code = input("\n[INPUT] :: Please enter Zip Code :: ")

        if(zip_code == None or zip_code.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            print("[MESSAGE] :: Enter '$EXIT$' to exit back to menu. ")
            continue
        elif (zip_code.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_zip_code(zip_code) == False):
            print("[INVALID] :: Some special characters are invalid in a City name. "
                  "\nPlease enter a valid city name.")
            continue
        else:
            zip_code = zip_code.strip()
            zipFlag = False
            break

    while countryFlag:
        print("\n[MESSAGE] :: Use ISO 3166 two-letter country code.")
        print(f"[MESSAGE] :: To know the country code go to {COUNTRY_CODE_SEARCH_URL}")
        country_code = input("\n[INPUT] :: Please enter a two-letter country code :: ")

        if(country_code == None or country_code.strip() == ''):
            print("[EMPTY] :: Found Empty input! Please try again...")
            continue
        elif (country_code.strip() == '$EXIT$'):
            print("Redirecting back...")
            return '$EXIT$'
        elif (is_country_code(country_code.strip()) == False):
            print("[INVALID] :: Special characters or <space> are invalid in a Country code. "
                  "\nPlease enter a valid Country code.")
            continue
        else:
            country_code = country_code.strip()
            countryFlag = False
            break

    return {"ZIP_CODE" : f"{zip_code},{country_code}"}


def getCityInfo():
    """This function fetches the city info from user
        @:return city info dictionary"""

    if DEBUG_MODE:
        print("[DEBUG] :: Inside getCityInfo()")

    print("[MESSAGE] :: Based on what parameters would you like to search for the Weather Forecast?\n")

    showMessagesToUser(["[A] :: Search By City Name",
           "[B] :: Search By City ID",
           "[C] :: Search By Geographic coordinates",
           "[D] :: Search By ZIP Code",
           "[E] :: Exit" ])

    user_search = None
    user_option = input("\n[INPUT] :: Please enter your option :: ")
    if DEBUG_MODE:
        print(f"[DEBUG] :: user_option :: {user_option}")

    if (user_option == None or user_option.strip() == ''):
        print("[EMPTY] :: Found Empty input! Please try again...")
        getCityInfo()
    elif (user_option.upper() == 'A'):
        user_search = searchByCityName()
    elif (user_option.upper() == 'B'):
        user_search = searchByCityID()
    elif (user_option.upper() == 'C'):
        user_search = searchByGeographicalCoordinates()
    elif (user_option.upper() == 'D'):
        user_search = searchByZipCode()
    elif (user_option.upper() == 'E'):
        user_input = input("[INPUT] :: Are you sure you want to EXIT? [Y] Yes [N] No :: ")
        if(user_input != None and user_input.strip() != '' and user_input.strip().upper() == 'Y'):
            return '$EXIT$'
    else:
        print("[INVALID] :: You entered an INVALID option! Please try again...")
        getCityInfo()

    if DEBUG_MODE:
        print(f"[DEBUG] :: user_search :: {user_search}")

    if (user_search == None):
        if DEBUG_MODE:
            print("[UNEXPECTED] :: user_search is null in getCityInfo()")
        print("[ERROR] :: Something went wrong! Please try again...or report to Admin")
        getCityInfo()
    elif (user_search == '$EXIT$'):
        if DEBUG_MODE:
            print(f"[DEBUG] :: User chose to $EXIT$")
        getCityInfo()
    else:
        if DEBUG_MODE:
            print(f"[DEBUG] :: returning ... user_search :: {user_search}")
        return user_search


def showMessageBeforeAppExit():
    print("Thank you for using Terminal Weather Forecast App!!")
    print("Please visit back again!!")
