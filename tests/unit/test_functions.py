import json
import unittest
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.functions.components import GetQuoteItemComponents


class TestGetQuoteItemComponent(unittest.TestCase):
    def setUp(self):
        # instantiate client singleton
        self.client = PaperlessClient()
        with open('tests/unit/mock_data/quote.json') as data_file:
            quote_json = json.load(data_file)
            self.quote_items = {}
            for item in quote_json['quote_items']:
                self.quote_items[item['id']] = item

    def test_invalid_starting_page(self):
        with self.assertRaises(ValueError):
            GetQuoteItemComponents(1, 0)

    def test_get_everything(self):
        qi = self.quote_items[105565]

        class result_set:
            def __init__(self, list_of_maps):
                self.list = list_of_maps
                self.called = 0

            def next_item(self, _url, _params={}):
                self.called += 1
                return self.list.pop(0)

        comps = [
            {
                'next': 'next',  # next just needs to be something aside None to loop to call the API again
                'results': [qi['components'][0], qi['components'][1]],
            },
            {
                'results': [qi['components'][2], qi['components'][3]],
            },
        ]

        rs = result_set(comps)
        self.client.get_resource_list = MagicMock(side_effect=rs.next_item)

        results = GetQuoteItemComponents(1)

        self.assertEqual(4, len(results))
        self.assertEqual(2, rs.called)
