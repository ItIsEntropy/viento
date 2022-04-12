from fastapi import FastAPI
from util.cache import get_weather
from typing import Any
from util.exceptions import APIError, APILimitError

app = FastAPI()  # Import the app


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
    try:
        response: dict[str, dict[str, Any]] = get_weather(latitude = latitude, longitude = longitude, url = url)
    except (OSError, APIError, APILimitError):
        # TODO: Make an error 50x
        pass
    # TODO: return 

@app.get('/current')
async def get_current_weather(latitude: str, longitude: str):
    # Get the current weather of the caller's location
    url: str = 'https://api.openweathermap.org/data/2.5/weather'

