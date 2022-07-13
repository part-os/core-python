import datetime
import json
import unittest
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.objects.integration_heartbeats import IntegrationHeartbeat


class TestIntegrationHeartbeat(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open(
            'tests/unit/mock_data/integration_heartbeat.json'
        ) as integration_heartbeat_data:
            self.integration_heartbeat = json.load(integration_heartbeat_data)

    def test_post_heartbeat(self):
        self.client.create_resource = MagicMock(return_value=self.integration_heartbeat)
        heartbeat = IntegrationHeartbeat(60).create(
            managed_integration_uuid="712f4343-a29c-4263-be38-3c1694f53439"
        )
        self.assertEqual(heartbeat, None)
