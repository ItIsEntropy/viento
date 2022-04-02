import requests
from typing import Any
from decouple import config
from util.exceptions import APILimitError, APIError


# variables needed for the API
API_KEY: str = config('WIND_API_KEY')  # API key for the openweather API


async def get_five_day_forecast(latitude: str, longitude: str) -> dict[str, dict[str, Any]] | Exception:
    """
    Get the 5 day, 3hour forecast for the area specified by latitude and longitude.
    :param longitude: a string representing the area longitude
    :param latitude: a string representing the area latitude
    :return: a dictionary (the JSON response of the API)
    """
    url: str = f'https://api.openweathermap.org/data/2.5/forecast'
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

