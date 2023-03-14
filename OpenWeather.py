# openweather.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Roy Richa
# rricha@uci.edu
# 51514923

# API KEY: af6472f0ac363c93d26a4f628d577fe1

import urllib, json
from urllib import request,error
from WebAPI import WebAPI, ResourceNotFoundError, UnauthorizedError, ForbiddenError, ServiceUnavailableError, URLError, InvalidURL


class OpenWeather(WebAPI):
    def __init__(self, zipcode="92697", ccode="US"):
        self.zipcode = zipcode
        self.ccode = ccode


    def load_data(self) -> None:
        '''
        Calls the web api using the required values and stores the response in class data attributes.
            
        '''
        #TODO: use the apikey data attribute and the urllib module to request data from the web api. See sample code at the begining of Part 1 for a hint.
        #TODO: assign the necessary response data to the required class data attributes
        self.error_code = ""
        try:
            url = f'https://api.openweathermap.org/data/2.5/weather?zip={self.zipcode},{self.ccode}&appid={self.apikey}&units=imperial'
            weather_obj = super()._download_url(url)
            
            self.temperature      = weather_obj['main']['temp']
            self.high_temperature = weather_obj['main']['temp_max']
            self.low_temperature  = weather_obj['main']['temp_min']
            self.longitude        = weather_obj['coord']['lon']
            self.latitude         = weather_obj['coord']['lat']
            self.description      = weather_obj['weather'][0]['description']
            self.humidity         = weather_obj['main']['humidity']
            self.city             = weather_obj['name']
            self.sunset           = weather_obj['sys']['sunset']

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

        except:
            self.error_code = 'Unexpected Error'
            print(self.error_code)


    def transclude(self, message:str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude
            
        :returns: The transcluded message
        '''
        # str((9/5) * (int(self.temperature) - 237.15) + 32)
        #TODO: write code necessary to transclude keywords in the message parameter with appropriate data from API
        try:
            if (("@weather" or "@weather_temp" or "@weather_humidity") in message) and (self.error_code == ""):
                # Replaces the temp keyword wtih actual temperature from API
                if ("@weather_temp" in message):
                    message = message.replace("@weather_temp", str(self.temperature))
                # Replaces the humidity keyword with actual humidity from API
                if ("@weather_humidity" in message):
                    message = message.replace("@weather_humidity", str(self.humidity))
                # Replaces the weather keyword with actual weather description from API
                if ("@weather" in message):
                    message = message.replace("@weather", self.description)
            else:
                # No change if they entered an invalid country or zipcode
                message = message
        except TypeError:
            message = "Failed to transclude. Message should only be of type string."

        return message
