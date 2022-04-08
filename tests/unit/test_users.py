import json
import unittest
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.objects.users import User


class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/user.json') as data_file:
            self.mock_user_json = json.load(data_file)

    def test_get_user(self):
        self.client.get_resource = MagicMock(return_value=self.mock_user_json)
        user = User.get(1)
        self.assertEqual(user.erp_code, 'test123')
        self.assertEqual(user.uuid, '7ef60b12-f9b4-4459-90f6-cfccfea6c7f3')
        self.assertEqual(user.first_name, 'Test')
        self.assertEqual(user.last_name, 'Testerson')
        self.assertEqual(user.email, 'test@testerson.com')

    def test_convert_user_to_json(self):
        self.client.get_resource = MagicMock(return_value=self.mock_user_json)
        self.maxDiff = None
        user = User.get(1)
        expected_user_json = {"erp_code": "test123"}
        self.assertEqual(json.loads(user.to_json()), expected_user_json)


class TestUserList(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/user_list.json') as data_file:
            self.mock_user_list_json = json.load(data_file)

    def test_get_user_list(self):
        self.client.get_resource_list = MagicMock(return_value=self.mock_user_list_json)
        users = User.list()
        self.assertEqual(len(users), 2)
        self.assertEqual(users[1].uuid, "7ef60b12-f9b4-4459-90f6-cfccfea6c7f4")
        self.assertEqual(users[1].first_name, "Boaty")
        self.assertEqual(users[1].last_name, "McBoatFace")
        self.assertEqual(users[1].email, "boaty@mcboatface.com")
        self.assertEqual(users[1].erp_code, "321boat")
