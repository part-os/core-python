import unittest
from unittest import mock
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.exceptions import PaperlessAuthorizationException


class TestClient(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        self.test_password = "test_password"
        self.test_username = "test_username"

    def test_client_is_singleton(self):
        # singelton by get_instance
        new_client1 = PaperlessClient.get_instance()
        self.assertTrue(new_client1 is self.client)
        new_client1.username = self.test_username
        self.assertEqual(self.test_username, self.client.username)
        # singleton by new instance
        new_client2 = PaperlessClient()
        self.assertTrue(new_client2 is self.client)
        self.assertEqual(self.test_username, new_client2.username)

    def test_authenticate_no_username_error(self):
        self.client.username = None
        self.client.password = self.test_password
        self.assertRaises(PaperlessAuthorizationException, self.client.authenticate)

    def test_authenticate_no_password_error(self):
        self.client.username = self.test_username
        self.client.password = None
        self.assertRaises(PaperlessAuthorizationException, self.client.authenticate)

    def test_authenticate(self):
        # set up client
        self.client.password = self.test_password
        self.client.username = self.test_username

        # mock data
        test_token = 'test token'
        mock_success = MagicMock()
        mock_success.status_code = 200
        mock_success.json.return_value = {'token': test_token}
        with mock.patch('paperless.client.requests.post', return_value=mock_success) as mock_posts:
            self.client.authenticate()
            mock_posts.assert_called()
            self.assertEqual(self.client.token, test_token)
