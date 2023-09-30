'''
Responsible for the protocole
of the dsu client module
'''

import json
import time
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


def send_dm(message, username, token):
    username = '"' + username + '"'
    message = '"' + message + '"'
    token = '"' + token + '"'
    timestamp = '"' + str(time.time()) + '"'
    json_string = '{"token":{token}, "directmessage": {"entry": {message}, "recipient": {username}, "timestamp": {timestamp}}}'
    json_string = json_string.replace('{username}', username)
    json_string = json_string.replace('{message}', message)
    json_string = json_string.replace('{token}', token)
    json_string = json_string.replace('{timestamp}', timestamp)

    return json_string


def unread_dms(token):
    token = '"' + token + '"'
    json_string = '{"token":{token}, "directmessage": "new"}'
    json_string = json_string.replace('{token}', token)

    # print(json_string)

    return json_string


def all_dms(token):
    token = '"' + token + '"'
    json_string = '{"token":{token}, "directmessage": "all"}'
    json_string = json_string.replace('{token}', token)

    # print(json_string)

    return json_string
