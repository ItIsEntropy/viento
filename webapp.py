from fastapi import FastAPI

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
    pass # TODO: flesh out by using cache to get data

