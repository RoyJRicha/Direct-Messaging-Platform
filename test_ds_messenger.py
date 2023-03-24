import unittest
from unittest.mock import MagicMock
from ds_messenger import DirectMessage, DirectMessenger
import socket

class TestDirectMessage(unittest.TestCase):
    def test_direct_message_init(self):
        dm = DirectMessage()
        self.assertIsNone(dm.recipient)
        self.assertIsNone(dm.message)
        self.assertIsNone(dm.timestamp)

class TestDirectMessenger(unittest.TestCase):

    def setUp(self):
        self.dm = DirectMessenger(dsuserver="168.235.86.101", username="RandomUser1234", password="testpassword")

    def test_direct_messenger_init(self):
        self.assertIsNone(self.dm.token)
        self.assertEqual(self.dm.username, "RandomUser1234")
        self.assertEqual(self.dm.password, "testpassword")
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
        dm = DirectMessenger(dsuserver="invalid_ip", username="RandomUser1234", password="testpassword")
        result, _ = dm.retrieve_token()
        self.assertFalse(result)

    def test_invalid_input_types(self):
        dm = DirectMessenger(dsuserver=123, username=345, password=False)
        result, _ = dm.retrieve_token()
        self.assertFalse(result)

    def test_timeout_error(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=socket.timeout()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="RandomUser1234", password="testpassword")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_connection_refused_error(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=ConnectionRefusedError()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="RandomUser1234", password="testpassword")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_socket_gaierror(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=socket.gaierror()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="RandomUser1234", password="testpassword")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

    def test_os_error(self):
        with unittest.mock.patch('socket.socket.connect', side_effect=OSError()):
            dm = DirectMessenger(dsuserver="168.235.86.101", username="RandomUser1234", password="testpassword")
            result, _ = dm.retrieve_token()
            self.assertFalse(result)

'''
if __name__ == '__main__':
    unittest.main()
'''