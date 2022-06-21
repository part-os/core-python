import datetime
import json
import unittest
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.objects.events import Event


class TestEvent(unittest.TestCase):
    def setUp(self):
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/event_list.json') as event_list_data:
            self.event_list_json = json.load(event_list_data)

    def test_list_events(self):
        self.client.get_resource_list = MagicMock(return_value=self.event_list_json)
        event_list = Event.list()
        self.assertEqual(len(event_list), 2)
        event_1: Event = event_list[0]
        self.assertEqual(event_1.uuid, "445ddb7c-6cde-4c42-aebc-489c4587d3bb")
        self.assertEqual(event_1.type, "part.created")
        self.assertEqual(event_1.related_object, "f3802d7b-16a9-46f7-bf17-c57eeff9edf0")
        self.assertEqual(event_1.related_object_type, "part")
        self.assertIsInstance(event_1.data, dict)
        self.assertEqual(event_1.data["type"], "manufactured")
        self.assertEqual(event_1.data["thickness_units"], "mm")
        self.assertEqual(event_1.created, "2022-02-01T22:21:58.718957Z")
        self.assertIsInstance(event_1.created_dt, datetime.datetime)
        event_2 = event_list[-1]
        self.assertEqual(event_2.uuid, "245ddb7c-6cde-4c42-aebc-489c4587d3bb")
        self.assertEqual(event_2.type, "integration_action.requested")
        self.assertEqual(event_2.related_object, "d3802d7b-16a9-46f7-bf17-c57eeff9edf0")
        self.assertEqual(event_2.related_object_type, "order")
        self.assertIsInstance(event_2.data, dict)
        self.assertEqual(event_2.data["action_type"], "export_order")
        self.assertEqual(event_2.data["status"], "completed")
        self.assertEqual(event_2.created, "2022-02-01T22:21:58.718956Z")
        self.assertIsInstance(event_2.created_dt, datetime.datetime)
