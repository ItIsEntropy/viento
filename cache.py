from util.net import get_weather_data
from typing import Any, Callable

def cached(func) -> Callable[[Callable], Callable]:
    def cache_or_net(*a,**kw):
        url: str = kw['url']
        # TODO: shorten latlong
        # TODO: key cache dict by dict[url, dict[lat,long, cached data]]
        cached_value = func(*a,**kw)
        # TODO: if cached value is None, make call to net and return that instead and save value it in cache
    return cache_or_net

def get_forecast(latitude: str, longitude: str) -> dict[str, dict[str, Any]] | Exception:
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
