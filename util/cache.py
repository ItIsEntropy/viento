from util.net import get_weather_data
from util.typing import LocationData, DataCache, WeatherData
from typing import Any, Callable
from util.io import get_file_locker
from pathlib import Path
import time
import decimal
import os
import json
import asyncio



# create a thread that sleeps per minute, 
# then wakes up and checks timestamps of all cached dicts and deletes older than 10 minute dicts

async def get_weather(latitude: str, longitude: str, url: str) -> DataCache | None | Exception:
    '''
    Get the forecast of a location based on the coordinates provided.
    The data is acquired from the cache file if it is present and contains the data, or the weather API otherwise
    :param latitude: latitude of location to query
    :param longitude: longitude of location to query
    :return: a response or an APIError
    '''
    # get locker plugin
    locker: Any = await get_file_locker()
    cache_path: Path = Path(os.getcwd()).joinpath('response_cache.json')
    # open cache file and lock it
    async with locker(cache_path) as cache_file:
        cache: DataCache = json.load(cache_file) # read json data of the file
        try:
            data: LocationData = cache[f'{url},{latitude},{longitude}']
            data_age: float = time.time() - data['time']
            if data_age > 600.0: 
                # data's time stamp is more than 10 minutes old, invalidate it by returning None
                return None
            return data # return the valid data
        except KeyError: # data does not exist, return None
            return None

async def cache_data(data:WeatherData, url:str, lat:str, lon:str) -> None:
    # TODO: cache the passed data into the file using a lock
    # get locker plugin
    locker: Any = await get_file_locker()
    cache_path: Path = Path(os.getcwd()).joinpath('response_cache.json')
    loc_data: LocationData = {'data': data, 'time': time.time()}
    # TODO: figure out how to none distructively update the dict with new data
    # open cache file and lock it
    async with locker(cache_path) as cache_file:
        cache: DataCache = json.load(cache_file) # read json data of the file
        cache[f'{url},{lat},{lon}'] = loc_data # store our new data into the data cache
        json.dump(obj=cache, fp=cache_file)
    raise NotImplementedError('Flesh this out')
    


def cached(func) -> Callable[[Callable], Callable]: #TODO: rename after strategy in use. add docstring
    # A decorator to tag network calls with a caching strategy
    if asyncio.iscoroutinefunction(func=func): # await coroutines and do other async operations
        pass
    else: # Normal funcs continue as usual without async code.
        pass
    # TODO: move code to above logic so we generify the decorator
    async def cache_or_net(*a,**kw):
        # TODO: add logic for positional args
        url: str = kw['url']
        lat: str = kw['latitude']
        lon: str = kw['longitude']
        decimal.getcontext().prec = 4 # set the decimal number precision to 4 places TODO: figure out correct precision
        lat = str(decimal.Decimal(lat)) # reduce latitude to 4 sig fig
        lon = str(decimal.Decimal(lon)) # reduce longitude to 4 sig fig
        cached_value: LocationData = await get_weather(latitude=lat, longitude=lon, url=url)#func(*a,**kw)
        if cached_value is None:
            net_data: LocationData  = await func(latitude=lat, longitude=lon, url=url)
            await cache_data(data=net_data, lat=lat, lon=lon, url=url)
            return net_data
        return cached_value
    return cache_or_net


'''
{
    url: {
            f'{lat},{lon}': {
                'data': data
                'time': timestamp (on creation)
            },
        }
}
'''