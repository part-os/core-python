import json
import unittest
from unittest.mock import MagicMock

from paperless.client import PaperlessClient
from paperless.functions.components import get_quote_item_components, get_quote_items


class TestGetPaginatedAPIObjects(unittest.TestCase):
    class result_set:
        def __init__(self, list_of_maps):
            self.list = list_of_maps
            self.called = 0

        def next_item(self, _url, _params={}):
            self.called += 1
            return self.list.pop(0)

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
            get_quote_item_components(1, 0)

        with self.assertRaises(ValueError):
            get_quote_items(1, 0)

    def test_get_all_components(self):
        qi = self.quote_items[105565]

        comps = [
            {
                'next': 'next',  # next just needs to be something aside None to loop to call the API again
                'results': [qi['components'][0], qi['components'][1]],
            },
            {
                'results': [qi['components'][2], qi['components'][3]],
            },
        ]

        rs = self.result_set(comps)
        self.client.get_resource_list = MagicMock(side_effect=rs.next_item)

        results = get_quote_item_components(1)

        self.assertEqual(4, len(results))
        self.assertEqual(2, rs.called)

    def test_get_all_quote_items(self):
        api_response = [
            {
                'next': 'next_page_url',
                'results': [
                    {
                        'id': 1,
                        'component_ids': [2, 3, 4],
                        'export_controlled': True,
                        'metadata': {
                            'stuff': 'more_stuff',
                        },
                        'position': 1,
                        'private_notes': 's3kr3t',
                        'public_notes': 'n0t s3kr3t',
                        'type': 'the type',
                        'workflow status': 'something',
                    },
                    {
                        'id': 2,
                        'component_ids': [5, 6, 7],
                        'export_controlled': True,
                        'metadata': {
                            'stuff': 'more_stuff',
                        },
                        'position': 2,
                        'private_notes': 's3kr3t',
                        'public_notes': 'n0t s3kr3t',
                        'type': 'the type',
                        'workflow status': 'something',
                    },
                ],
            },
            {
                'results': [
                    {
                        'id': 3,
                        'component_ids': [2, 3, 4],
                        'export_controlled': True,
                        'metadata': {
                            'stuff': 'more_stuff',
                        },
                        'position': 3,
                        'private_notes': 's3kr3t',
                        'public_notes': 'n0t s3kr3t',
                        'type': 'the type',
                        'workflow status': 'something',
                    },
                ],
            },
        ]

        rs = self.result_set(api_response)
        self.client.get_resource_list = MagicMock(side_effect=rs.next_item)

        quote_items = get_quote_items(1)

        self.assertEqual(3, len(quote_items))
        self.assertEqual(2, rs.called)
