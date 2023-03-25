"""
Tests the Profile module
"""
import unittest
import os
from Profile import Post, Message, Sent, Profile

class TestDSUClasses(unittest.TestCase):
    """
    Tests the DSU functions in Profile
    """
    def test_prof(self):
        """
        Tests the Profile Class
        """
        path = os.path.abspath('TestError.dsu')
        post = Post()
        post.set_entry('entry')
        post.set_time(10.0)
        save = Profile()
        save.save_profile(path)
        save.add_post(post)
        save.add_message('message')
        save.add_sent_messages('sent message')
        save.add_author('friend')
        save.del_post(0)
        save.get_posts()
        save.get_friends()
        path = os.path.abspath('TestError.dsu')
        save.load_profile(path)

    def test_post(self):
        """
        Tests the Post Class
        """
        save = Post()
        save.set_entry('entry')
        save.get_entry()
        save.set_time(10.0)
        save.get_time()

    def test_sent(self):
        """
        Tests the Sent Class
        """
        save = Sent()
        save.add_message('message')
        save.add_recipient('to')

    def test_message(self):
        """
        Tests the Message Class"""
        save = Message()
        save.add_message('message')
        save.add_author('to')
