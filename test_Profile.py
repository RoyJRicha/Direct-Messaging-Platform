import unittest
from Profile import Post, Message, Sent, Profile, DsuFileError, DsuProfileError

class TestDSUClasses(unittest.TestCase):
    def test_post(self):
        entry = "Test post"
        post = Post(entry)
        self.assertEqual(post.entry, entry)
        self.assertNotEqual(post.timestamp, 0)

    def test_message(self):
        message = "Test message"
        author = "test_user"
        msg = Message(message, author)
        self.assertEqual(msg.message, message)
        self.assertEqual(msg.author, author)
        self.assertNotEqual(msg.timestamp, 0)

    def test_sent(self):
        message = "Test sent message"
        recipient = "test_recipient"
        sent = Sent(message, recipient)
        self.assertEqual(sent.message, message)
        self.assertEqual(sent.recipient, recipient)
        self.assertNotEqual(sent.timestamp, 0)

    def test_profile(self):
        dsuserver = "test_server"
        username = "test_user"
        password = "test_password"
        profile = Profile(dsuserver, username, password)

        self.assertEqual(profile.dsuserver, dsuserver)
        self.assertEqual(profile.username, username)
        self.assertEqual(profile.password, password)

        # Test add_post
        entry = "Test post"
        post = Post(entry)
        profile.add_post(post)
        self.assertIn(post, profile.get_posts())

        # Test add_message
        message = "Test message"
        author = "test_author"
        msg = Message(message, author)
        profile.add_message(msg)
        self.assertIn(msg, profile.get_messages())

        # Test add_sent_messages
        message = "Test sent message"
        recipient = "test_recipient"
        sent = Sent(message, recipient)
        profile.add_sent_messages(sent)
        self.assertIn(sent, profile.get_sent_messages())

        # Test add_author
        friend = "test_friend"
        profile.add_author(friend)
        self.assertIn(friend, profile.get_friends())

        # Test del_post
        post_index = 0
        profile.del_post(post_index)
        self.assertNotIn(post, profile.get_posts())

        # Test save_profile and load_profile
        dsu_file = "test_profile.dsu"
        profile.save_profile(dsu_file)

        loaded_profile = Profile()
        loaded_profile.load_profile(dsu_file)

        self.assertEqual(loaded_profile.dsuserver, dsuserver)
        self.assertEqual(loaded_profile.username, username)
        self.assertEqual(loaded_profile.password, password)

'''
if __name__ == "__main__":
    unittest.main()
'''