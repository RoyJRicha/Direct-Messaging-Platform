"""
Tests the ds_messenger module
"""
import unittest
from unittest.mock import MagicMock
from ds_messenger import DirectMessage, DirectMessenger
import socket

class TestDirectMessage(unittest.TestCase):
    """
    Tests the init of DM Class
    """
    def test_direct_message_init(self):
        """
        Tests initialization
        """
        dm = DirectMessage()
        self.assertIsNone(dm.recipient)
        self.assertIsNone(dm.message)
        self.assertIsNone(dm.timestamp)

class TestDirectMessenger(unittest.TestCase):
    """
    Tests the functions of DirectMessenger class
    """
    def setUp(self):
        """
        Sets Up object
        """
        self.dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")

    def test_direct_messenger_init(self):
        """
        Tests the intitialization
        """
        self.assertIsNone(self.dm.token)
        self.assertEqual(self.dm.username, "Friend2")
        self.assertEqual(self.dm.password, "friend")
        self.assertEqual(self.dm.dsuserver, "168.235.86.101")
        self.assertEqual(self.dm.port, 3021)

    def test_send(self):
        """
        Tests Send
        """
        result = self.dm.send("Hello, World!", "TestRecipient")
        self.assertTrue(result)

    def test_invalid_send(self):
        """
        Test invalid sending
        """
        result = self.dm.send(1234, True)
        self.assertFalse(result)

    def test_retrieve_new(self):
        """
        Test retrieving new
        """
        result = self.dm.retrieve_new()
        self.assertIsInstance(result, list)

    def test_retrieve_all(self):
        """
        Test retrieving all
        """
        result = self.dm.retrieve_all()
        self.assertIsInstance(result, list)

    def test_invalid_ip_address(self):
        """
        Tests invalid ip address
        """
        dm = DirectMessenger(dsuserver="invalid_ip", username="Friend2", password="friend")
        result, _ = dm.retrieve_token()
        self.assertFalse(result)

    def test_invalid_input_types(self):
        """
        Tests invalid input types
        """
        dm = DirectMessenger(dsuserver=123, username=345, password=False)
        result, _ = dm.retrieve_token()
        self.assertFalse(result)

    def test_timeout_error(self):
        """
        Tests a timeout error
        """
        with unittest.mock.patch('socket.socket.connect', side_effect=socket.timeout()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_connection_refused_error(self):
        """
        Tests a connection refused error
        """
        with unittest.mock.patch('socket.socket.connect', side_effect=ConnectionRefusedError()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_socket_gaierror(self):
        """
        Tests a gaierror
        """
        with unittest.mock.patch('socket.socket.connect', side_effect=socket.gaierror()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_os_error(self):
        """
        Tests an os error
        """
        with unittest.mock.patch('socket.socket.connect', side_effect=OSError()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="Friend2", password="friend")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)
        
    def test_retrieve_dms_error(self):
        """
        Tests a retrieving dms error
        """
        self.dm.retrieve_token = MagicMock(return_value=(True, MagicMock()))
        with unittest.mock.patch('ds_protocol.unread_dms', return_value='{"token": "f21ccb88-6aac-4592-aebf-4b6bd9b4d033", "directmessage": "new"}'):
            with unittest.mock.patch('socket.socket.recv', return_value='{"response": {"type": "error", "message": "An error occurred"}}'.encode()):
                result = self.dm.retrieve_dms("new")
        self.assertFalse(result)

    def test_retrieve_dms_invalid_token(self):
        """
        Tests retriving dms invalid token error
        """
        self.dm.retrieve_token = MagicMock(return_value=(False, None))
        result = self.dm.retrieve_dms("new")
        self.assertFalse(result)
