import httpx
import pytest
import starlette.testclient
from fastapi.testclient import TestClient
from webapp import app
from httpx import AsyncClient
from decouple import config

client: starlette.testclient.TestClient = TestClient(app)  # create a TestClient for orchestrating tests with the webapp
API_KEY: str = config('WIND_API_KEY')

def test_get_homepage():
    '''
    test the homepage of the API to see if it redirects you to the forecast page and contains the js file
    :return: None
    '''
    response = client.get("/")
    # TODO: flesh out
    assert response.status_code == 200  # FIXME: not sure this is right
    # assert response.json() ==
    pass


@pytest.mark.anyio
async def test_get_forecast():
    async with AsyncClient(app=app, base_url='https://api.openweathermap.org/data/2.5/forecast') as ac:
        url: str = "/forecast"
        query_params = {'lat': '-34.156113', 'lon': '-118.131943', 'appid': API_KEY}
        response: httpx.Response = await ac.get(url, params=query_params)
    assert response.status_code == 200
    # assert response.json() == # TODO: read the response.json file and compare it in the assert here
    pass
