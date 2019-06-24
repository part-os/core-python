import unittest

from paperless.client import PaperlessClient
from paperless.exceptions import PaperlessAuthorizationException


class TestClient(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        self.access_token = "test_accesstoken"

    def test_client_is_singleton(self):
        # singelton by get_instance
        new_client1 = PaperlessClient.get_instance()
        self.assertTrue(new_client1 is self.client)
        new_client1.access_token = self.access_token
        self.assertEqual(self.access_token, self.client.access_token)
        # singleton by new instance
        new_client2 = PaperlessClient()
        self.assertTrue(new_client2 is self.client)
        self.assertEqual(self.access_token, new_client2.access_token)

    def test_without_bearer_token_throws_an_error(self):
        """
        Without a proper access token the client will raise a PaperlessAuthorizationException.
        """
        client = PaperlessClient.get_instance()
        client.access_token = None
        self.assertEqual(client.access_token, None)
        self.assertRaises(PaperlessAuthorizationException, self.client.get_authenticated_headers)

    def test_authorization_token(self):
        """
        Test that we generate the properly formatted authenticated headers.
        """
        client = PaperlessClient.get_instance()
        client.access_token = self.access_token
        self.assertEqual(client.access_token, self.access_token)
        headers = self.client.get_authenticated_headers()
        self.assertEqual(headers['Authorization'], 'API-Token {}'.format(self.access_token))
