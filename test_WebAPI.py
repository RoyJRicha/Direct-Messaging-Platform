import pytest
import WebAPI
from OpenWeather import OpenWeather
from LastFM import LastFM


class TestAPI:

    def test_weather_download(self):
        weather = OpenWeather()
        weather.set_apikey('invalid_key')
        weather.load_data()
        assert weather.error_code == 'Invalid API key was provided'

