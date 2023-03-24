import unittest
from ds_messenger import DirectMessage, DirectMessenger

class TestDirectMessage(unittest.TestCase):
    def test_direct_message_init(self):
        dm = DirectMessage()
        self.assertIsNone(dm.recipient)
        self.assertIsNone(dm.message)
        self.assertIsNone(dm.timestamp)

    