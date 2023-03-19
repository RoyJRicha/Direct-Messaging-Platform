# Profile.py
#
# ICS 32
# Assignment #2: Journal
#
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# Roy Richa
# rricha@uci.edu
# 51514923

import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
    DsuFileError, custom exception handler, you should catch in your own code. It
    is raised when attempting to load or save Profile objects to file the system.

    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError custom exception handler, catch in your own code. It
    is raised when attempting to deserialize a dsu file to a Profile object.

    """
    pass


class Post(dict):
    """

    Post class is responsible for working with individual user posts. It
    supports two features: Timestamp property that is set on instantiation/
    when entry object is set and an entry property that stores post message.

    """
    def __init__(self, entry: str = None, timestamp: float = 0):
        '''
        variable instantiation
        '''
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        '''
        Sets the entry
        '''
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        '''
        gets the entry
        '''
        return self._entry

    def set_time(self, time: float):
        '''
        sets the time
        '''
        self._timestamp = time
        dict.__setitem__(self, 'timestamp', time)

    def get_time(self):
        '''
        gets the time
        '''
        return self._timestamp

    """

    The property method is used to support get and set capability for entry and
    time values. When value for entry is changed, or set, timestamp field is
    updated to the current time.

    """
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Message(dict):
    """
    Message class is responsible for working with individual user messages. It
    supports three features: Timestamp property that is set on instantiation/
    when entry object is set and an entry property that stores post message,
    and the user who sent the message.
    """

    def __init__(self, message: str = None, author: str = None, timestamp: float = 0):
        '''
        Variable instantiation
        '''
        self._timestamp = timestamp
        self.add_message(message)
        self.add_author(author)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, message=self._message, author=self._author, timestamp=self._timestamp)


    def add_message(self, message):
        '''
        Sets the message
        '''
        self._message = message
        dict.__setitem__(self, 'message', message)


    def add_author(self, author):
        '''
        Sets the message
        '''
        self._author = author
        dict.__setitem__(self, 'author', author)

class Sent(dict):
    """
    Message class is responsible for working with individual user messages. It
    supports three features: Timestamp property that is set on instantiation/
    when entry object is set and an entry property that stores post message,
    and the user who sent the message.
    """

    def __init__(self, message: str = None, recipient: str = None, timestamp: float = 0):
        '''
        Variable instantiation
        '''
        self._timestamp = timestamp
        self.add_message(message)
        self.add_recipient(recipient)

        # Subclass dict to expose Post properties for serialization
        # Don't worry about this!
        dict.__init__(self, message=self._message, recipient=self._recipient, timestamp=self._timestamp)


    def add_message(self, message):
        '''
        Sets the message
        '''
        self._message = message
        dict.__setitem__(self, 'message', message)


    def add_recipient(self, recipient):
        '''
        Sets the message
        '''
        self._recipient = recipient
        dict.__setitem__(self, 'recipient', recipient)


class Profile:
    """
    Profile class exposes properties required to join an ICS 32 DSU server. You
    need to use class to manage information provided by each new user
    created in your program for a2. Pay close attention to the properties and
    functions in class as you will need to make use of each of them in program.

    When creating your program you will collect user input for the properties
    exposed by this class. A Profile class ensures that a username and password
    are set, but has no conventions to do so. Make sure that your code
    verifies that required properties are set.

    """

    def __init__(self, dsuserver=None, username=None, password=None):
        '''
        Is responsible for variable 
        instantiation
        '''
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''            # OPTIONAL
        self._posts = []         # OPTIONAL
        self._messages = []
        self.friends = []
        self._sent_messages = []


    def add_post(self, post: Post) -> None:
        """

        add_post accepts a Post object and appends it to posts list. Posts
        are stored in a list object in order they added. If multiple Posts objects
        created, but added to the Profile in a different order, it is possible for
        list to not be sorted by Post.timestamp. So take caution as to how you
        implement your add_post code.

        """
        self._posts.append(post)


    def add_message(self, message):
        """
        Adds messages recieved from
        users
        """
        self._messages.append(message)

    def add_sent_messages(self, message):
        """
        Adds messages sent
        """
        self._sent_messages.append(message)

    
    def get_messages(self):
        """
        Returns a list of messages
        """
        return self._messages

    
    def get_friends(self):
        """
        Returns a list of friends
        """
        return self.friends

    
    def add_author(self, friend):
        """
        Adds authors from messages
        """
        if friend not in self.friends:
            self.friends.append(friend)
        else:
            pass


    def del_post(self, index: int) -> bool:
        """

        del_post removes a Post at a given index and returns True
        if successful and False if an invalid index was supplied.

        To determine which post to delete implement your own search operation on
        the posts returned from the get_posts function to find the correct index.

        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False


    def get_posts(self) -> list[Post]:
        """

        get_posts returns the list object containing all posts that have been
        added to the Profile object

        """
        return self._posts


    def save_profile(self, path: str) -> None:
        """

        save_profile accepts an existing dsu file to save the current
        instance of Profile to the file system.

        Example usage:

        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError

        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'w')
                json.dump(self.__dict__, f)
                f.close()
            except Exception as ex:
                raise DsuFileError("Error while attempting to process the DSU file.", ex)
        else:
            raise DsuFileError("Invalid DSU file path or type")


    def load_profile(self, path: str) -> None:
        """

        load_profile will populate the current instance of
        Profile with data stored in a DSU file.

        Example usage:

        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError

        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                f = open(p, 'r')
                obj = json.load(f)
                self.username = obj['username']
                self.password = obj['password']
                self.dsuserver = obj['dsuserver']
                self.bio = obj['bio']
                for post_obj in obj['_posts']:
                    post = Post(post_obj['entry'], post_obj['timestamp'])
                    self._posts.append(post)
                for msg_obj in obj['_messages']:
                    msg = Message(msg_obj['message'], msg_obj['author'], msg_obj['timestamp'])
                    self._messages.append(msg)
                for friend_obj in obj['friends']:
                    self.friends.append(friend_obj)
                for msg_obj in obj['_sent_messages']:
                    msg = Sent(msg_obj['message'], msg_obj['recipient'], msg_obj['timestamp'])
                    self._sent_messages.append(msg)
                f.close()
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
