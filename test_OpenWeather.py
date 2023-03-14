import unittest
import pytest
from OpenWeather import OpenWeather
from WebAPI import WebAPI, ResourceNotFoundError, UnauthorizedError, ForbiddenError, ServiceUnavailableError


class TestOpenWeather(unittest.TestCase):


    def test_set_apikey(self):
        '''
        testing
        '''
        weather = OpenWeather()
        weather.set_apikey("af6472f0ac363c93d26a4f628d577fe1")
        self.assertEqual(weather.apikey, "af6472f0ac363c93d26a4f628d577fe1")
    

    def test_load_data(self):
        '''
        testing
        '''
        weather = OpenWeather(zipcode="92697", ccode="US")
        weather.set_apikey("af6472f0ac363c93d26a4f628d577fe1")
        weather.load_data()
        self.assertIsInstance(weather.temperature, (float, int))
        self.assertIsInstance(weather.high_temperature, float)
        self.assertIsInstance(weather.low_temperature, float)
        self.assertIsInstance(weather.longitude, float)
        self.assertIsInstance(weather.latitude, float)
        self.assertIsInstance(weather.description, str)
        self.assertIsInstance(weather.humidity, int)
        self.assertIsInstance(weather.city, str)
        self.assertIsInstance(weather.sunset, int)
        assert weather.error_code == ""
    

    def test_succeed_transclude(self):
        '''
        testing
        '''
        weather = OpenWeather()
        weather.set_apikey("af6472f0ac363c93d26a4f628d577fe1")
        weather.load_data()
        weather.temperature = 75.0
        weather.humidity = 30
        weather.description = "Sunny"
        message = "The weather today is @weather with a temperature of @weather_temp degrees and a humidity of @weather_humidity percent."
        self.assertEqual(weather.transclude(message), "The weather today is Sunny with a temperature of 75.0 degrees and a humidity of 30 percent.")


    def test_fail_load_data_ResourceNotFoundError(self):
        '''
        testing
        '''
        weather = OpenWeather(zipcode="92620", ccode="WW")
        weather.set_apikey("af6472f0ac363c93d26a4f628d577fe1")
        weather.load_data()
        assert weather.error_code == 'Page was not found and/or invalid zipcode or country was provided'


    def test_fail_load_data_ResourceNotFoundError_2(self):
        '''
        testing
        '''
        weather = OpenWeather(zipcode="926098620", ccode="US")
        weather.set_apikey("af6472f0ac363c93d26a4f628d577fe1")
        weather.load_data()
        assert weather.error_code == 'Page was not found and/or invalid zipcode or country was provided'


    def test_fail_load_data_UnauthorizedError(self):
        '''
        testing
        '''
        weather = OpenWeather(zipcode="92620", ccode="US")
        weather.set_apikey("invalid_key")
        weather.load_data()
        assert weather.error_code == 'Invalid API key was provided'
    
    def test_fail_load_data_InvalidURL(self):
        '''
        testing
        '''
        weather = OpenWeather(zipcode="92620", ccode="US")
        weather.set_apikey("invalid key")
        weather.load_data()
        assert weather.error_code == 'Invalid URL. Formatting rules were broken'


    def test_fail_transclude(self):
        '''
        testing
        '''
        weather = OpenWeather()
        weather.set_apikey("af6472f0ac363c3d26a4f628d577fe1")
        weather.load_data()
        weather.error_code != ""
        message = "The weather today is @weather with a temperature of @weather_temp degrees and a humidity of @weather_humidity percent."
        self.assertEqual(weather.transclude(message), message)
