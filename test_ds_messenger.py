import unittest
from ds_messenger import DirectMessage, DirectMessenger

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