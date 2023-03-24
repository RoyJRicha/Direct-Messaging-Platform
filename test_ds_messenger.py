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

    def test_send(self):
        result = self.dm.send("Hello, World!", "TestRecipient")
        self.assertTrue(result)

    def test_retrieve_new(self):
        result = self.dm.retrieve_new()
        self.assertIsInstance(result, list)

    def test_retrieve_all(self):
        result = self.dm.retrieve_all()
        self.assertIsInstance(result, list)

'''
if __name__ == '__main__':
    unittest.main()
'''