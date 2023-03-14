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

