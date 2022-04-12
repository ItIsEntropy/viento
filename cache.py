from util.net import get_weather_data
from typing import Any

async def get_forecast(latitude: str, longitude: str, url: str) -> dict[str, dict[str, Any]] | Exception:
    '''
    Get the forecast of a location based on the coordinates provided.
    The data is acquired from the cache file if it is present and contains the data, or the weather API otherwise
    :param latitude: latitude of location to query
    :param longitude: longitude of location to query
    :return: a response or an APIError
    '''
    # TODO get cache file and check for url match
    # TODO: if url matches return data, else get data from the web using API call
    # TODO: save the returned API data with the URL. start a 10 minute timer to delete the data
    pass