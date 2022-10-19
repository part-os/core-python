import json
import unittest
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.objects.purchased_components import (
    PurchasedComponent,
    PurchasedComponentColumn,
)


class TestPurchasedComponents(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/purchased_components.json') as data_file:
            self.mock_purchased_components_json = json.load(data_file)
            self.mock_pc1 = self.mock_purchased_components_json[0]
        with open(
            'tests/unit/mock_data/purchased_components_batch_response.json'
        ) as data_file:
            self.mock_batch_upsert_pc = json.load(data_file)

    def test_get_column(self):
        self.client.get_resource = MagicMock(return_value=self.mock_pc1)
        component = PurchasedComponent.get(1)
        self.assertEqual(component.id, self.mock_pc1['id'])

    def test_batch_upsert_purchased_components(self):
        self.client.put_resource = MagicMock(return_value=self.mock_batch_upsert_pc)
        response = PurchasedComponent.upsert_many(
            [
                PurchasedComponent(oem_part_number="test", piece_price="3"),
                PurchasedComponent(oem_part_number="test", piece_price="4"),
            ]
        )
        self.assertEqual(len(response.successes), 1)
        self.assertEqual(len(response.failures), 1)


class TestPurchasedComponentColumns(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/purchased_component_columns.json') as data_file:
            self.mock_purchased_component_columns_json = json.load(data_file)
            self.mock_c1 = self.mock_purchased_component_columns_json[0]

    def test_get_column(self):
        self.client.get_resource = MagicMock(return_value=self.mock_c1)
        column = PurchasedComponentColumn.get(1)
        self.assertEqual(column.id, self.mock_c1['id'])
