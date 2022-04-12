import requests
from typing import Any
from decouple import config
from util.exceptions import APILimitError, APIError
from util.cache import cached
from util.typing import WeatherData



# variables needed for the API
API_KEY: str = config('WIND_API_KEY')  # API key for the openweather API



@cached
async def get_weather_data(
        latitude: str,
        longitude: str,
        url: str
) -> WeatherData | APIError:
    """
    Get the 5 day, 3hour forecast for the area specified by latitude and longitude.
    :param longitude: a string representing the area longitude
    :param latitude: a string representing the area latitude
    :param call_type: The type of call (forecast data type) to make
    :return: a dictionary (the JSON response of the API) or an Exception
    """
    query_params: dict = {'lat': latitude, 'lon': longitude, 'appid': API_KEY}
    response: requests.Response = requests.get(url=url, params=query_params)
    match response.status_code:  # Check the status of the request
        case 200:  # request successful, return the response data
            return response.json()
        case 429:  # API limit reached, return exception
            raise APILimitError(f'API limit exceeded. Unable to acquire Forecast for lat={latitude}, lon={longitude}')
        case _:  # unknown status code, do future stuff
            if response.ok:
                pass
            else:
                raise APIError('Unknown API Error occured')

