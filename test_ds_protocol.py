import unittest
import json
import ds_protocol as dp

class TestDsProtocol(unittest.TestCase):

    def test_extract_json(self):
        json_msg = '{"response": {"type": "ok", "token": "test_token"}}'
        data_tuple = dp.extract_json(json_msg)
        self.assertEqual(data_tuple.response['type'], 'ok')
        self.assertEqual(data_tuple.token, 'test_token')

    def test_join_usr_pwd(self):
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


'''
if __name__ == '__main__':
    unittest.main()
'''