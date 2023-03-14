# webapi.py

# Starter code for assignment 4 in ICS 32
# Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Roy Richa
# rricha@uci.edu
# 51514923

from abc import ABC, abstractmethod
import urllib, json
from urllib import request, error
import socket
import http


class ResourceNotFoundError(Exception):
    pass


class UnauthorizedError(Exception):
    pass


class ForbiddenError(Exception):
    pass


class ServiceUnavailableError(Exception):
    pass


class URLError(Exception):
    pass


class InvalidURL(Exception):
    pass


class WebAPI(ABC):

    def _download_url(self, url: str) -> dict:
        response = None
        r_obj = None

        try:
            response = urllib.request.urlopen(url)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print(f'Status code: {e.code}')
            if e.code == 404:
                raise ResourceNotFoundError('Page was not found and/or invalid zipcode or country was provided')
            elif e.code == 401:
                raise UnauthorizedError('Invalid API key was provided')
            elif e.code == 403:
                raise ForbiddenError('Server refusing to fulfill request from the user possibly due to invalid api key')
            elif e.code == 503:
                raise ServiceUnavailableError('Server is currently unable to handle the request')
            
        except urllib.error.URLError as u:
            print('Failed to download contents of URL')
            print(f'Reason: {u.reason}')
            raise URLError('Failed to connect to the internet or URL was invalid.')

        except http.client.InvalidURL:
            print('Failed to download contents of URL')
            raise InvalidURL('Invalid URL. Formatting rules were broken')

        except ConnectionRefusedError:
            print('\nUnable to connect to the server. Invalid IP Address or Port Number. Please try again!\n')

        except TimeoutError:
            print('\nA connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond\n')
        
        except socket.gaierror:
            print('\nUnable to connect to the server. Invalid IP Address. Please try again!\n')

        except (IndexError, KeyError) as err:
            print('Invalid data formatting')
            print(f'Error code: {err}')

        except:
            print('Unable to download data from URL. Unexpted Error.')

        finally:
            if response != None:
                response.close()
        
        return r_obj

    def set_apikey(self, apikey:str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
            
        '''
        self.apikey = apikey

    @abstractmethod
    def load_data(self):
        pass

    @abstractmethod
    def transclude(self, message:str) -> str:
        pass
