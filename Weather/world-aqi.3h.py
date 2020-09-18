#!/usr/bin/env LC_ALL=en_US.UTF-8 /usr/local/bin/python3
#
# <bitbar.title>Air Quality Index</bitbar.title>
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>mgjo5899</bitbar.author>
# <bitbar.author.github>mgjo5899</bitbar.author.github>
# <bitbar.desc>You can look up the world AQIs</bitbar.desc>
# <bitbar.image>https://i.imgur.com/CcQyBZZ.png</bitbar.image>
# <bitbar.dependencies>python</bitbar.dependencies>
#
# by mgjo5899

import json

from string import capwords
from urllib.request import urlopen, Request

# You need...
#   1. Google Geocoding API key
#      - https://developers.google.com/maps/documentation/geocoding
#   2. AQICN API token
#      - https://aqicn.org/api/
google_api_key = "YOUR-API-KEY"
aqi_api_token = "YOUR-API-TOKEN"

city = "san+francisco"  # City you want to get AQI, replace space with plus sign (+)


# A function that makes a GET request to the request_url and load the resulting JSON as
#   a Python dictionary
def get_json_result(request_url):
    request = Request(request_url)
    r = urlopen(request).read()

    return json.loads(r)

# Get latitude and longitude of the given city for more accurate results
def geocode_city(city):
    geocoding_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={city}&key={google_api_key}"
    result = get_json_result(geocoding_url)
    location = None

    if result.get("status") == "OK":
        best_result = result.get("results", [None])[0]

        if best_result:
            location = best_result.get("geometry", {}).get("location")

    if location and location.get("lat") and location.get("lng"):
        return location
    else:
        raise Exception(f"Can't geocode the city: {city}")

# Using the latitude and longitude values, query the AQI of the city
def get_aqi_value(geo_location):
    lat = geo_location["lat"]
    lng = geo_location["lng"]
    aqi_request_url = f"https://api.waqi.info/feed/geo:{lat};{lng}/?token={aqi_api_token}"
    result = get_json_result(aqi_request_url)
    aqi_value = None

    if result.get("status") == "ok":
        aqi_value = int(result.get("data", {}).get("aqi"))

    if aqi_value:
        return aqi_value
    else:
        raise Exception(f"Can't find AQI for the Geo-location: {geo_location}")

geo_location = geocode_city(city)
aqi_value = get_aqi_value(geo_location)

city = capwords(city.replace("+", " "))
print(f"AQI in {city}: {aqi_value}")
