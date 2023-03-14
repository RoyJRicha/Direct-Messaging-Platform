# lastfm.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Roy Richa
# rricha@uci.edu
# 51514923

# API KEY: 441e295d5bbbdf8c61fcea2b4bd20fb0

import urllib, json
from urllib import request,error
from WebAPI import WebAPI, ResourceNotFoundError, UnauthorizedError, ForbiddenError, ServiceUnavailableError, URLError, InvalidURL


class LastFM(WebAPI):
    # add ccode if wanting country specified
    def __init__(self, limit=500):
        '''
        Initializes variables
        '''
        # self.ccode = ccode
        self.limit = limit


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
            
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        self.error_code = ""
        try:
            # add "country={self.ccode}&" to url if wanting country specified
            url = f"https://ws.audioscrobbler.com/2.0/?method=chart.gettopartists&limit={self.limit}&api_key={self.apikey}&format=json"
            fm_obj = super()._download_url(url)
            # print(fm_obj)
            artists_lst = []
            listeners_lst = []
            
            for artist in range(len(fm_obj['artists']['artist'])):
                artists_lst.append(fm_obj['artists']['artist'][artist]['name'])
            
            for artist in range(len(fm_obj['artists']['artist'])):
                listeners_lst.append(fm_obj['artists']['artist'][artist]['listeners'])

            self.top_artists = artists_lst
            self.top_listeners = listeners_lst

        except ResourceNotFoundError as r:
            self.error_code = r.args[0]
            print(self.error_code)
        
        except UnauthorizedError as u:
            self.error_code = u.args[0]
            print(self.error_code)

        except ForbiddenError as f:
            self.error_code = f.args[0]
            print(self.error_code)

        except ServiceUnavailableError as s:
            self.error_code = s.args[0]
            print(self.error_code)

        except URLError as u:
            self.error_code = u.args[0]
            print(self.error_code)

        except InvalidURL as i:
            self.error_code = i.args[0]
            print(self.error_code)

        except KeyError:
            self.error_code = "Limit was set to a number too large"
            print(self.error_code)

        except:
            self.error_code = 'Unexpected Error'
            print(self.error_code)

    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
        try:
            if (("@lastfm" or "@lastfm_listeners") in message) and (self.error_code == ""):
                if ("@lastfm_listeners" in message):
                    message = message.replace("@lastfm_listeners", self.top_listeners[0])
                if ("@lastfm" in message):
                    message = message.replace("@lastfm", self.top_artists[0])
            else:
                message = message
        except TypeError:
            message = "Failed to transclude. Message should only be of type string."

        return message
