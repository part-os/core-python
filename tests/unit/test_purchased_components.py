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

    def test_get_column(self):
        self.client.get_resource = MagicMock(return_value=self.mock_pc1)
        component = PurchasedComponent.get(1)
        self.assertEqual(component.id, self.mock_pc1.id)


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
        self.assertEqual(column.id, self.mock_c1.id)
