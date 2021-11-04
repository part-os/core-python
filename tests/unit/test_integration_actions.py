import unittest
import json
from paperless.client import PaperlessClient
from unittest.mock import MagicMock

from paperless.objects.integration_actions import IntegrationAction, ManagedIntegration


class TestIntegrationAction(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/managed_integration.json') as single_integration_data:
            self.mock_managed_integration_json = json.load(single_integration_data)
        with open('tests/unit/mock_data/managed_integration_list.json') as list_integration_data:
            self.mock_managed_integration_list_json = json.load(list_integration_data)
        with open('tests/unit/mock_data/integration_action.json') as single_action_data:
            self.mock_integration_action_json = json.load(single_action_data)
        with open('tests/unit/mock_data/integration_action_list.json') as list_actions_data:
            self.mock_integration_action_list_json = json.load(list_actions_data)

    def test_get_managed_integration(self):
        self.client.get_resource = MagicMock(return_value=self.mock_managed_integration_json)
        managed_integration = ManagedIntegration.get(id=3)
        self.assertEqual(managed_integration.id, 3)
        self.assertEqual(managed_integration.erp_name, "jobboss")
        self.assertEqual(managed_integration.is_active, True)
        self.assertEqual(managed_integration.integrations_version, "2.0")
        self.assertEqual(managed_integration.integrations_project_subcommit, "blah")
        self.assertEqual(managed_integration.create_integration_action_after_creating_new_order, False)

    def test_list_managed_integrations(self):
        self.client.get_resource_list = MagicMock(return_value=self.mock_managed_integration_list_json)
        managed_integration_list = ManagedIntegration.list()
        self.assertEqual(len(managed_integration_list), 3)
        integration_1 = managed_integration_list[0]
        self.assertEqual(integration_1.id, 5)
        self.assertEqual(integration_1.erp_name, "e2")
        self.assertEqual(integration_1.erp_version, "1.5")
        self.assertEqual(integration_1.is_active, False)
        integration_1 = managed_integration_list[-1]
        self.assertEqual(integration_1.id, 1)
        self.assertEqual(integration_1.erp_name, "jobboss")
        self.assertEqual(integration_1.erp_version, "1.0")
        self.assertEqual(integration_1.is_active, True)

    def test_get_integration_action(self):
        self.client.get_resource = MagicMock(return_value=self.mock_integration_action_json)
        int_act = IntegrationAction.get(managed_integration_id=self.mock_managed_integration_json['id'], action_uuid="abc-123")
        self.assertEqual(int_act.action_type, "export_order")
        self.assertEqual(int_act.action_uuid, "abc-123")
        self.assertEqual(int_act.status, "queued")
        self.assertEqual(int_act.status_message, None)
        self.assertEqual(int_act.entity_id, "1")

    def test_list_integration_actions(self):
        self.client.get_resource_list = MagicMock(return_value=self.mock_integration_action_list_json)
        action_list = IntegrationAction.list(managed_integration_id=self.mock_managed_integration_json['id'])
        self.assertEqual(len(action_list), 8)
        action_1 = action_list[0]
        self.assertEqual(action_1.action_type, "export_order")
        self.assertEqual(action_1.action_uuid, "20bf3744-625a-49d3-b6a8-5293334e9476")
        self.assertEqual(action_1.status, "completed")
        self.assertEqual(action_1.status_message, None)
        self.assertEqual(action_1.entity_id, "1")
        action_8 = action_list[-1]
        self.assertEqual(action_8.action_type, "export_order")
        self.assertEqual(action_8.action_uuid, "f9e8b33c-2361-47b2-ad23-c9390d488619")
        self.assertEqual(action_8.status, "queued")
        self.assertEqual(action_8.status_message, None)
        self.assertEqual(action_8.entity_id, "99")
