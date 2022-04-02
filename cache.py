from util.net import get_five_day_forecast
from typing import Any

async def get_forecast(latitude: str, longitude: str) -> dict[str, dict[str, Any]] | Exception:
    '''
    Get the forecast of a location based on the coordinates provided.
    The data is acquired from the cache file if it is present and contains the data, or the weather API otherwise
    :param latitude:
    :param longitude:
    :return:
    '''
    pass # TODO: add a radius checking function to see if latlong within range of present latlongs