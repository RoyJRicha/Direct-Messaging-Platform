import unittest
import pytest
from LastFM import LastFM

class TestLastFM(unittest.TestCase):

    def test_set_apikey(self):
        '''
        test apikey
        '''
        lastfm = LastFM()
        lastfm.set_apikey("441e295d5bbbdf8c61fcea2b4bd20fb0")
        self.assertEqual(lastfm.apikey, "441e295d5bbbdf8c61fcea2b4bd20fb0")


    def test_load_data(self):
        '''
        test loading data
        '''
        lastfm = LastFM()
        lastfm.set_apikey("441e295d5bbbdf8c61fcea2b4bd20fb0")
        lastfm.load_data()
        self.assertIsInstance(lastfm.top_artists, list)
        self.assertIsInstance(lastfm.top_artists[0], str)
        self.assertIsInstance(lastfm.top_listeners, list)
        self.assertIsInstance(lastfm.top_listeners[0], str)
        self.assertEqual(lastfm.error_code, "")


    def test_succeed_transclude(self):
        '''
        test successful transclude
        '''
        lastfm = LastFM(limit=1)
        lastfm.set_apikey("441e295d5bbbdf8c61fcea2b4bd20fb0")
        lastfm.load_data()
        message = "The top artist today is @lastfm"
        self.assertIn(lastfm.top_artists[0], lastfm.transclude(message))


    def test_fail_load_data(self):
        '''
        test failed data
        '''
        lastfm = LastFM()
        lastfm.set_apikey("441e295d5bbbdf8c61fcea2b4bd")
        lastfm.load_data()
        assert lastfm.error_code != ""


    def test_fail_transclude(self):
        '''
        test fail transclude
        '''
        lastfm = LastFM()
        lastfm.set_apikey("441e295d5bbbdf8c61fcea2b4bd20fb0")
        lastfm.load_data()
        lastfm.error_code = "ERROR"
        message = "The top artist today is @lastfm"
        self.assertEqual(lastfm.transclude(message), message)

    def test_fail_load_data_UnauthorizedError(self):
        '''
        test fail load Unathorized
        '''
        lastfm = LastFM()
        lastfm.set_apikey("invalid_key")
        lastfm.load_data()
        assert lastfm.error_code == 'Server refusing to fulfill request from the user possibly due to invalid api key'
    
    def test_fail_load_data_InvalidURL(self):
        '''
        test invalid url
        '''
        lastfm = LastFM()
        lastfm.set_apikey("invalid key")
        lastfm.load_data()
        assert lastfm.error_code == 'Invalid URL. Formatting rules were broken'

    def test_fail_load_data_KeyError(self):
        '''
        test key error
        '''
        lastfm = LastFM(5000000)
        lastfm.set_apikey("441e295d5bbbdf8c61fcea2b4bd20fb0")
        lastfm.load_data()
        assert lastfm.error_code == 'Limit was set to a number too large'
