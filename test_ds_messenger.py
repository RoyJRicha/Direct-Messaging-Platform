import unittest
from unittest.mock import MagicMock
from ds_messenger import DirectMessage, DirectMessenger
import ds_protocol
import socket

class TestDirectMessage(unittest.TestCase):
    def test_direct_message_init(self):
        dm = DirectMessage()
        self.assertIsNone(dm.recipient)
        self.assertIsNone(dm.message)
        self.assertIsNone(dm.timestamp)

class TestDirectMessenger(unittest.TestCase):

    def setUp(self):
        self.dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")

    def test_direct_messenger_init(self):
        self.assertIsNone(self.dm.token)
        self.assertEqual(self.dm.username, "Friend2")
        self.assertEqual(self.dm.password, "friend")
        self.assertEqual(self.dm.dsuserver, "168.235.86.101")
        self.assertEqual(self.dm.port, 3021)

    def test_send(self):
        result = self.dm.send("Hello, World!", "TestRecipient")
        self.assertTrue(result)

    def test_invalid_send(self):
        result = self.dm.send(1234, True)
        self.assertFalse(result)

    def test_retrieve_new(self):
        result = self.dm.retrieve_new()
        self.assertIsInstance(result, list)

    def test_retrieve_all(self):
        result = self.dm.retrieve_all()
        self.assertIsInstance(result, list)

    def test_invalid_ip_address(self):
        dm = DirectMessenger(dsuserver="invalid_ip", username="Friend2", password="friend")
        result, _ = dm.retrieve_token()
        self.assertFalse(result)

    def test_invalid_input_types(self):
        dm = DirectMessenger(dsuserver=123, username=345, password=False)
        result, _ = dm.retrieve_token()
        self.assertFalse(result)

    def test_timeout_error(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=socket.timeout()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_connection_refused_error(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=ConnectionRefusedError()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_socket_gaierror(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=socket.gaierror()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_os_error(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=OSError()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    '''
    def test_retrieve_dms_new(self):
        self.dm.retrieve_token = MagicMock(return_value=(True, MagicMock()))
        with unittest.mock.patch('ds_protocol.unread_dms', return_value='{"token": "f21ccb88-6aac-4592-aebf-4b6bd9b4d033", "directmessage": "new"}'):
            with unittest.mock.patch('socket.socket.recv', return_value='{"response": {"type": "ok", "messages": [{"message": "Hello", "from": "User1", "timestamp": "1679516335.0818863"}]}}'.encode()):
                result = self.dm.retrieve_dms("new")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].message, "Hello")
        self.assertEqual(result[0].recipient, "User1")
        self.assertEqual(result[0].timestamp, "1679516335.0818863")

    def test_retrieve_dms_all(self):
        self.dm.retrieve_token = MagicMock(return_value=(True, MagicMock()))
        with unittest.mock.patch('ds_protocol.all_dms', return_value='{"token":"f21ccb88-6aac-4592-aebf-4b6bd9b4d033", "directmessage": "all"}'):
            with unittest.mock.patch('socket.socket.recv', return_value=MagicMock(decode=lambda: '{"response": {"type": "ok", "messages": [{"message": "This is my test message", "from": "aritest1", "timestamp": "1679601567.65513"}]}}')):
                result = self.dm.retrieve_dms("all")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].message, "This is my test message")
        self.assertEqual(result[0].recipient, "aritest1")
        self.assertEqual(result[0].timestamp, "1679601567.65513")
    '''
        
    def test_retrieve_dms_error(self):
        self.dm.retrieve_token = MagicMock(return_value=(True, MagicMock()))
        with unittest.mock.patch('ds_protocol.unread_dms', return_value='{"token": "f21ccb88-6aac-4592-aebf-4b6bd9b4d033", "directmessage": "new"}'):
            with unittest.mock.patch('socket.socket.recv', return_value='{"response": {"type": "error", "message": "An error occurred"}}'.encode()):
                result = self.dm.retrieve_dms("new")
        self.assertFalse(result)

    def test_retrieve_dms_invalid_token(self):
        self.dm.retrieve_token = MagicMock(return_value=(False, None))
        result = self.dm.retrieve_dms("new")
        self.assertFalse(result)

'''
if __name__ == '__main__':
    unittest.main()
'''