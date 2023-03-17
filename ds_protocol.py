'''
Responsible for the protocole
of the dsu client module
'''
# Roy Richa
# rricha@uci.edu
# 51514923

import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
DataTuple = namedtuple('DataTuple', ['response', 'token'])


def extract_json(json_msg: str) -> DataTuple:
    '''
    Call the json.loads function on a json string and a DataTuple object

    '''
    try:
        json_obj = json.loads(json_msg)
        response = json_obj['response']
        token = json_obj['response']['token']
    except json.JSONDecodeError:
        print("Json cannot be decoded.")

    return DataTuple(response, token)


def join_usr_pwd(username, password):
    username = '"' + username + '"'
    password = '"' + password + '"'
    json_string = '{"join": {"username": {username}, "password": {password}, "token":""}}'
    json_string = json_string.replace('{username}', username)
    json_string = json_string.replace('{password}', password)

    return json_string


def post(post, token):
    post = '"' + post + '"'
    token = '"' + token + '"'
    timestamp = ''
    json_string = '{"token":{user_token}, "post": {"entry": {post}, "timestamp": "1603167689.3928561"}}'
    json_string = json_string.replace('{user_token}', token)
    json_string = json_string.replace('{post}', post)

    return json_string


def bio_post(bio, token):
    bio = '"' + bio + '"'
    token = '"' + token + '"'
    json_string = '{"token":{token}, "bio": {"entry": {bio}, "timestamp": "1603167689.3928561"}}'
    json_string = json_string.replace('{bio}', bio)
    json_string = json_string.replace('{token}', token)

    return json_string


def send_dm(username, message, token):
    username = '"' + username + '"'
    message = '"' + message + '"'
    token = '"' + token + '"'
    json_string = '{"token":{token}, "directmessage": {"entry": {message}, "recipient": {username}, "timestamp": "1603167689.3928561"}}'
    json_string = json_string.replace('{username}', username)
    json_string = json_string.replace('{message}', message)
    json_string = json_string.replace('{token}', token)

    return json_string


def unread_dms(token):
    token = '"' + token + '"'
    json_string = '{"token":{token}, "directmessage": "new"}'
    json_string = json_string.replace('{token}', token)

    return json_string


def all_dms(token):
    token = '"' + token + '"'
    json_string = '{"token":{token}, "directmessage": "all"}'
    json_string = json_string.replace('{token}', token)

    return json_string



class Post(dict):
    """

    Post class is responsible for working with individual user posts. It
    supports two features: Timestamp property that is set on instantiation/
    when entry object is set and an entry property that stores post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        '''
        variable instantiation
        '''
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        '''
        Sets the entry
        '''
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        '''
        gets the entry
        '''
        return self._entry

    def set_time(self, time: float):
        '''
        sets the time
        '''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        '''
        gets the time
        '''
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and
    time values. When value for entry is changed, or set, timestamp field is
    updated to the current time.

    """
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)

