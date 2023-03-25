"""
Tests the ds_protocol.py module
"""
import unittest
import json
import ds_protocol as dp

class TestDsProtocol(unittest.TestCase):
    """
    Tests the functions of protocol"""
    def test_extract_json(self):
        """
        Tests Extraction
        """
        json_msg = '{"response": {"type": "ok", "token": "test_token"}}'
        data_tuple = dp.extract_json(json_msg)
        self.assertEqual(data_tuple.response['type'], 'ok')
        self.assertEqual(data_tuple.token, 'test_token')

    def test_join_usr_pwd(self):
        """
        Tests join user and pass
        """
        username = "test_username"
        password = "test_password"

        json_string = dp.join_usr_pwd(username, password)
        json_obj = json.loads(json_string)

        self.assertIn("join", json_obj)
        self.assertIn("username", json_obj["join"])
        self.assertIn("password", json_obj["join"])
        self.assertIn("token", json_obj["join"])
        self.assertEqual(json_obj["join"]["username"], username)
        self.assertEqual(json_obj["join"]["password"], password)
        self.assertEqual(json_obj["join"]["token"], "")

    def test_send_dm(self):
        """
        Tests send dm
        """
        message = "Random Test Message"
        username = "RandomUsername1234"
        token = "41476543.89283928"
        json_string = dp.send_dm(message, username, token)
        json_obj = json.loads(json_string)
        self.assertEqual(json_obj['token'], token)
        self.assertEqual(json_obj['directmessage']['entry'], message)
        self.assertEqual(json_obj['directmessage']['recipient'], username)

    def test_unread_dms(self):
        """
        Tests getting unread dms
        """
        token = "41476543.89283928"
        json_string = dp.unread_dms(token)
        json_obj = json.loads(json_string)
        self.assertEqual(json_obj['token'], token)
        self.assertEqual(json_obj['directmessage'], 'new')

    def test_all_dms(self):
        """
        Tests getting all dms
        """
        token = "41476543.89283928"
        json_string = dp.all_dms(token)
        json_obj = json.loads(json_string)
        self.assertEqual(json_obj['token'], token)
        self.assertEqual(json_obj['directmessage'], 'all')
