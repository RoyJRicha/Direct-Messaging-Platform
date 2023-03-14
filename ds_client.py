# Roy Richa
# rricha@uci.edu
# 51514923

import socket
import json
import ast
import traceback
import ds_protocol as dp


def send(server: str, port: int, username: str, password: str, message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    # TODO: return either True or False depending on results of required operation

    results = True
    c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Accessing the username and password

    try:
        c_socket.connect((server, port))

        data = dp.join_usr_pwd(username, password)

        try:
            c_socket.sendall(data.encode())
            received_data = c_socket.recv(4096).decode()
            received_data_dict = json.loads(received_data)
            print()
            print(received_data_dict['response']['message'])
            print()
            if received_data_dict['response']['type'] == 'error':
                results = False
        # This will return a statement if program wasn't able to access user or pass
        except:
            print('Could not access/send username and password or connect to the server.\n')
            results = False
    # Checks for a failed connection
    except ConnectionRefusedError:
        print('\nUnable to connect to the server. Invalid IP Address or Port Number. Please try again!\n')
        results = False
    # Checks for an invalid Port number which causes a TimeoutError
    except TimeoutError:
        print('\nA connection attempt failed because the connected party did not properly respond after a period of time, or established connection failed because connected host has failed to respond\n')
        results = False
    # Checks in case the hard coded function call has incorrect types passed in
    except TypeError:
        print('\nFailed to connect to the server likely due to the following error(s): \n')
        if type(server) != str:
            print('\tThe server IP Address must be given as a string, bytes or bytearray expected, not an integer, float, None, or boolean\n')
        if type(port) != int:
            print('\tPort number must be given as an integer, not a string, float, None, or boolean\n')
        if type(username) != str:
            print('\tUsername must be given as a string, not an integer, float, None, or boolean\n')
        if type(password) != str:
            print('\tPassword must be given as a string, not an integer, float, None, or boolean\n')

        results = False
    # This ensures that the IP address given is valid
    except socket.gaierror:
        print('\nUnable to connect to the server. Invalid IP Address. Please try again!\n')
        results = False
    # This is used to catch an extra errors that may occur
    except:
        # print('Unable to connect to the server. Invalid IP Address or Port Number. Please try again!\n')
        traceback.print_exc()
        print('\nAn Error has occured, please try again!\n')
        results = False

    # Extracting the data from user input
    if results is True:
        try:
            user_extraction = dp.extract_json(received_data)
        # This deals with if the data given is not in json format
        except UnboundLocalError:
            print('Unable to extract data from file. Ensure file is in proper json format.')
            results = False
        # This will print an the error from the server if an error occurs
        except KeyError:
            print(received_data_dict['response']['message'])
            print()
            results = False
    else:
        pass

    # This checks to ensure that bio and message are actual values
    if results is True:
        if message == None and bio == None:
            print('There is nothing to publish, both message and bio are given as type None.\n')
            results = False

    # This will check to see if the type of the input is ok
    # Then it will send the post to the server if everything is in check
    if results is True:
        str_none = True
        # This ensures that the inputs are given as strings, if an input is given
        if (type(message) != str and message != None) or (type(bio) != str and bio != None):
            results = False
            str_none = False
            print('\nUnable to process or extract input due to the following issues: \n')

            if (type(message) != str) and (message != None):
                print(f'\tMessage was given as an incorrect type, please only enter message as a string\n')
            if (type(bio) != str) and (bio != None):
                print(f'\tBio was given as an incorrect type, please only enter bio as a string\n')

        if bio != None and message != None and str_none is True:
            if message == '' or bio == '' or message.isspace() or bio.isspace():
                results = False
                print('\nNothing was posted to the server due to following issue(s): \n')
                if message == '' or message.isspace():
                    print('\tMessage cannot be inputted as a blank or all whitespace input\n')
                if bio == '' or bio.isspace():
                    print('\tBio cannot be inputted as a blank or all whitespace input\n')

        if message == None:
            if bio == '' or bio.isspace():
                results = False
                print('\nNothing was posted to the server due to following issue(s): \n')
                print('\tBio cannot be inputted as a blank or all whitespace input\n')

        if bio == None:
            if message == '' or message.isspace():
                results = False
                print('\nNothing was posted to the server due to following issue(s): \n')
                print('\tMessage cannot be inputted as a blank or all whitespace input\n')

        # Here is where the posting will happen
        if results is True:
            # This checks if a message was requested to post
            if message:
                if user_extraction.response['type'] == 'ok':
                    token = user_extraction.token
                    post_data = dp.post(message, token)
                    c_socket.sendall(post_data.encode())
                    post_received_data = c_socket.recv(4096).decode()
                    post_dict = ast.literal_eval(post_received_data)
                    print('\t' + post_dict['response']['message'])
                    print()
                # Incase type is 'error', data composition will fail
                else:
                    print('Data composition failed.\n')
                    results = False

            # Checks if user inputted a bio
            # If so, will check if input is ok
            # Then send information to the server
            if bio:
                if user_extraction.response['type'] == 'ok':

                    token = user_extraction.token
                    biography_split = dp.bio_post(bio, token)
                    c_socket.sendall(biography_split.encode())
                    biography_recieved = c_socket.recv(4096).decode()
                    bio_dict = ast.literal_eval(biography_recieved)
                    print('\t' + bio_dict['response']['message'])
                    print()
                # Incase type is 'error' Data composition will fail
                else:
                    print('Data composition failed.\n')
                    results = False
            else:
                pass
        else:
            pass

    c_socket.close()

    return results
