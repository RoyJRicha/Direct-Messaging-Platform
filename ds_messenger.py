"""
ds_messenger.py is responsible
for the connection and retrieval of
information from the local server on
port 3021. The Classes allow for the
retrieval of tokens, sent messages,
recieved messages, and the saving
of DirectMessage in a list of objects
of that class
"""
import socket
import json
import traceback
import ds_protocol as dp


class DirectMessage:
    """
    This class is called
    to allow for the saving
    of messages in a single
    object so that they can be
    accessed easier outside
    this class
    """
    def __init__(self):
        """
        Institialization of the variables
        that are needed for this class
        """
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    """
    DirectMessenger is responsible for the
    retrieval of tokens, sending messages, and
    the retrieval of new and all messages for
    a specific profile taking in an IP address, 
    username, and password
    """
    def __init__(self, dsuserver=None, username=None, password=None):
        """
        Initialization of all variables,
        including the port, that are needed
        for all functions in the Class to
        work together and function properly
        """
        self.token = None
        self.username = username
        self.password = password
        self.dsuserver = dsuserver
        self.port = 3021

    def retrieve_token(self):
        """
        This function is used for the sole
        purpose of retrieve the token from the
        server and setting it if and only if
        there was no error from the server
        as it requested the token. It also
        returns T/F depending on status of
        connection as well as the socket,
        if it was obtained
        """
        results = True
        c_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Accessing the username and password

        try:
            c_socket.connect((self.dsuserver, self.port))

            data = dp.join_usr_pwd(self.username, self.password)

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
            if isinstance(self.dsuserver) != str:
                print('\tThe server IP Address must be given as a string, bytes or bytearray expected, not an integer, float, None, or boolean\n')
            if isinstance(self.port) != int:
                print('\tPort number must be given as an integer, not a string, float, None, or boolean\n')
            if isinstance(self.username) != str:
                print('\tUsername must be given as a string, not an integer, float, None, or boolean\n')
            if isinstance(self.password) != str:
                print('\tPassword must be given as a string, not an integer, float, None, or boolean\n')

            results = False
        # This ensures that the IP address given is valid
        except socket.gaierror:
            print('\nUnable to connect to the server. Invalid IP Address. Please try again!\n')
            results = False
        # Connection Lost/No Connection Error
        except OSError:
            print('Connection Error: Check internet and/or host connection')
            results = False
        # This is used to catch an extra errors that may occur
        except Exception as error:
            # print('Unable to connect to the server. Invalid IP Address or Port Number. Please try again!\n')
            # traceback.print_exc()
            print('\nAn Error has occured, please try again:', error)
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
            except Exception as error:
                print('Error has occured:', error)
        else:
            pass

        if results is True:
            if user_extraction.response['type'] == 'ok':
                self.token = user_extraction.token

        return results, c_socket

    def retrieve_dms(self, category):
        """
        Simply put, this is both the retrieve all
        and retrieve new functions essentially put
        and condenced to one class. When the functions
        are called independently, they pass in either
        'new' or 'all' to this function to determine
        what to grab. This was done because the
        functions were essentially identical with
        the only difference being dp.unread_dms
        or dp.all_dms
        """
        results, c_socket = self.retrieve_token()

        if results is True:
            try:
                if category == "new":
                    data = dp.unread_dms(self.token)
                elif category == "all":
                    data = dp.all_dms(self.token)

                try:
                    c_socket.sendall(data.encode())
                    received_data = c_socket.recv(4096).decode()
                    # print("Received data:", received_data)
                    received_data_dict = json.loads(received_data)
                    print()
                    print(received_data_dict['response']['messages'])
                    dms_dict = received_data_dict['response']['messages']
                    new_dms = []
                    print()
                    if received_data_dict['response']['type'] == 'error':
                        results = False
                # This will return a statement if program wasn't able to access user or pass
                except Exception as error:
                    traceback.print_exc()
                    print('Could not access/send message and recipient or connect to the server:', error)
                    results = False

            except Exception as error:
                print("An error occurred:", error)
                results = False

        if results is True:
            for element in dms_dict:
                message_class = DirectMessage()
                message_class.message = element['message']
                message_class.recipient = element['from']
                message_class.timestamp = element['timestamp']

                new_dms.append(message_class)

        if results is False:
            return results

        return new_dms

    def send(self, message: str, recipient: str) -> bool:
        """
        Responsible for actually sending
        the requested message to the server
        and therefor the recipient. The function
        takes message and recipient as parameters
        and sneds the message to the requested
        recipient
        """
        # must return true if message successfully sent, false if send failed.
        results, c_socket = self.retrieve_token()
        print(recipient)
        # Accessing the username and password
        if results is True:
            try:
                data = dp.send_dm(message, recipient, self.token)

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
                except Exception as error:
                    print('Could not access/send message and recipient or connect to the server:', error)
                    results = False
            # Checks in case the hard coded function call has incorrect types passed in
            except TypeError:
                print('\nFailed to connect to the server likely due to the following error(s): \n')
                if isinstance(self.dsuserver) != str:
                    print('\tThe server IP Address must be given as a string, bytes or bytearray expected, not an integer, float, None, or boolean\n')
                if isinstance(self.port) != int:
                    print('\tPort number must be given as an integer, not a string, float, None, or boolean\n')
                if isinstance(recipient) != str:
                    print('\tRecipient must be given as a string, not an integer, float, None, or boolean\n')
                if isinstance(message) != str:
                    print('\tMessage must be given as a string, not an integer, float, None, or boolean.\n')

                results = False

        c_socket.close()

        return results

    def retrieve_new(self) -> list:
        """
        Retrieve new retrieves only the new
        messages a specific profile may have
        recieved. If retrieving dm's failes, it
        will return false, otherwise, as requested
        from the assignment, it will return a list
        of objects from the DirectMessage class
        """
        # must return a list of DirectMessage objects containing all new messages
        result = self.retrieve_dms("new")

        print(result)

        return result

    def retrieve_all(self) -> list:
        """
        Retrieve all retrieves all the
        messages a specific profile may have
        recieved. If retrieving dm's failes, it
        will return false, otherwise, as requested
        from the assignment, it will return a list
        of objects from the DirectMessage class
        """
        # must return a list of DirectMessage objects containing all messages
        result = self.retrieve_dms("all")

        print(result)

        return result
