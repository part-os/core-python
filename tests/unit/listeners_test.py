import unittest
from unittest import mock
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.exceptions import PaperlessAuthorizationException
from paperless.listeners import OrderListener

# test create listener from last updated paramater passed
# test create listener without last update paramater passed but  with an existing cache
# test create listener without last updated paramaer and no existing patch, but return from list
# test create listener without last updated paramaer and no existing patch, without a return from list
# test on_event saves the correct value
# test next event comes from the saved event
# test on event is not called on 404

class TestClient(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        self.test_password = "test_password"
        self.test_username = "test_username"

    def test_instantiate_with_last_updated_param(self):
        self.assertFalse(False)

"""
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
"""