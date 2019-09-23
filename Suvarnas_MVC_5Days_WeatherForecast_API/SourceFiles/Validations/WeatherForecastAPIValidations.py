import re

#----------City Name Validation--------------#
CITY_RE = re.compile(
    r"^[a-zA-Z\u0080-\u024F]+(?:. |-| |')*"  # a word
    r"([1-9a-zA-Z\u0080-\u024F]+(?:. |-| |'))*"
    r"[a-zA-Z\u0080-\u024F]*$"
)

# ("1", False),
# ("Toronto", True),
# ("Saint-Père-en-Retz", True),
# ("Saint Père en Retz", True),
# ("Saint-Père en Retz", True),
# ("Paris 13e Arrondissement", True),
# ("Paris  13e  Arrondissement ", True),
# ("Bouc-Étourdi", True),
# ("Arnac-la-Poste", True),
# ("Bourré", True),
# ("Å", True),
# ("San Francisco", True)
def is_city(value: str) -> bool:
    valid = CITY_RE.match(value) is not None
    return valid

#-------End of City Name Validation----------#

#-----------Two-Letter Country Code Validation-------------#
COUNTRY_CODE_RE = re.compile(
    r"^[a-zA-Z][a-zA-Z]$"
)

# ("IN", True),
# ("us", True),
# ("U$", False),
# ("U S ", False)
def is_country_code(value: str) -> bool:
    valid = COUNTRY_CODE_RE.match(value) is not None
    return valid

#-------End of Two-Letter Country Code Validation----------#


#-----------City ID Validation-------------#
CITY_ID_RE = re.compile(
    r'^[0-9][0-9]'
)

# ("IN", True),
# ("us", True),
# ("U$", False),
# ("U S ", False)
def is_city_id(value: str) -> bool:
    valid = CITY_ID_RE.match(value) is not None
    return valid

#-------City ID Validation----------#


#-----------Latitude Longitude Validation-------------#
LAT_LON_RE = re.compile(
    r'^[0-9][0-9\.]'
)

# ("IN", True),
# ("us", True),
# ("U$", False),
# ("U S ", False)
def is_lat_lon(value: str) -> bool:
    valid = LAT_LON_RE.match(value) is not None
    return valid

#-------Latitude Longitude Validation----------#


#-----------Two-Letter Country Code Validation-------------#
ZIP_CODE_RE = re.compile(
    r"(?<!\n)[\d]{5,6}[\-]?[\d]*"
)

# ("IN", True),
# ("us", True),
# ("U$", False),
# ("U S ", False)
def is_zip_code(value: str) -> bool:
    valid = ZIP_CODE_RE.match(value) is not None
    return valid

#-------End of Two-Letter Country Code Validation----------#