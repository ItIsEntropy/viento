import requests
from typing import Any
from decouple import config
from util.exceptions import APILimitError, APIError

# variables needed for the API
API_KEY: str = config('WIND_API_KEY')  # API key for the openweather API


async def get_weather_data(
        latitude: str,
        longitude: str,
        call_type: str = 'current'
) -> dict[str, dict[str, Any]] | APIError:
    """
    Get the 5 day, 3hour forecast for the area specified by latitude and longitude.
    :param longitude: a string representing the area longitude
    :param latitude: a string representing the area latitude
    :param call_type: The type of call (forecast data type) to make
    :return: a dictionary (the JSON response of the API) or an Exception
    """
    call_types: dict[str, str] = {'current': 'weather', 'forecast': 'forecast'}
    if call_type not in call_types.keys():
        ValueError(f"Unable to make weather forecast type. valid types are:{call_types.keys()}") # invalid forecast type wanted
    url: str = f'https://api.openweathermap.org/data/2.5/{call_types[call_type]}'
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

