from fastapi import FastAPI
from util.net import get_weather_data
from typing import Any
from util.exceptions import APIError, APILimitError

app = FastAPI()  # Import the app

async def make_call(latitude: str, longitude: str, url:str, err_msg: str):
    try:
        response: dict[str, dict[str, Any]] = await get_weather_data(latitude = latitude, longitude = longitude, url = url)
    except (OSError, APIError, APILimitError):
        # TODO: Make an error 50x
        pass
    # TODO: return 
    


@app.get('/')
async def get_home(latitude: str | None = None, longitude: str | None = None):
    """
    Home page of the API
    :return: None
    """
    pass # TODO: use JS to get current location then use redirect to/ fetch data from forecast with latlongs


@app.get('/forecast')
async def get_forecast(latitude: str, longitude: str):
    '''
    Get the weather forecast for a location provided the coordinates
    :param latitude: The location latitude
    :param longitude: The location longitude
    :return: None
    '''
    url: str = 'https://api.openweathermap.org/data/2.5/forecast'
    err_msg: str = f'Something went wrong!!'
    make_call(latitude=latitude, longitude=longitude, url=url)

@app.get('/current')
async def get_current_weather(latitude: str, longitude: str):
    # Get the current weather of the caller's location
    url: str = 'https://api.openweathermap.org/data/2.5/weather'
    err_msg: str = f'Something went wrong rn!!'
    make_call(latitude=latitude, longitude=longitude, url=url)


