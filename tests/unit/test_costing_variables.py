import json
import unittest
from typing import List

from paperless.api_mappers.quotes import QuoteComponentMapper
from paperless.functions.costing import (
    get_component_costing_updates,
    get_costing_variable_updates,
)
from paperless.objects.quotes import (
    CostingVariablePayload,
    QuoteComponent,
    QuoteCostingVariable,
    QuoteCostingVariableMixin,
)


class TestCostingVariableUpdateData(unittest.TestCase):

    def setUp(self):
        self.basic_vars: List[QuoteCostingVariable] = [
            QuoteCostingVariable(
                label='test_basic',
                quantity_specific=False,
                quantities={},
                variable_class='basic',
                value_type='number',
                value=1.024,
            ),
            QuoteCostingVariable(
                label='test_basic_qs',
                quantity_specific=True,
                quantities={
                    1: CostingVariablePayload(value=1.5, row=None, options=None),
                    2: CostingVariablePayload(value=True, row=None, options=None),
                    3: CostingVariablePayload(value='test', row=None, options=None),
                },
                variable_class='basic',
                value_type='number',
                value='',
            ),
        ]

        self.drop_down_vars: List[QuoteCostingVariable] = [
            QuoteCostingVariable(
                label='test_dd',
                quantity_specific=False,
                quantities={},
                variable_class='drop_down',
                value_type='string',
                value='something here',
            ),
            QuoteCostingVariable(
                label='test_dd_qs',
                quantity_specific=True,
                quantities={
                    1: CostingVariablePayload(value=1, row=None, options=None),
                    2: CostingVariablePayload(value=False, row=None, options=None),
                    3: CostingVariablePayload(value='words', row=None, options=None),
                },
                variable_class='drop_down',
                value_type='string',
                value='',
            ),
        ]

        self.table_vars: List[QuoteCostingVariable] = [
            QuoteCostingVariable(
                label='test_table',
                quantity_specific=False,
                quantities={
                    1: CostingVariablePayload(
                        row={
                            'key1': 'some value',
                            'key2': 42,
                            'key3': True,
                        },
                        value=None,
                        options=None,
                    ),
                },
                variable_class='table',
                value_type='string',
                value='',
            ),
            QuoteCostingVariable(
                label='test_table_qs',
                quantity_specific=True,
                quantities={
                    1: CostingVariablePayload(
                        row={
                            'key1': 'string',
                            'key2': 25,
                            'key3': False,
                        },
                        value=None,
                        options=None,
                    ),
                    5: CostingVariablePayload(
                        row={
                            'key1': 'another string',
                            'key2': 100,
                            'key3': True,
                        },
                        value=None,
                        options=None,
                    ),
                },
                variable_class='table',
                value_type='string',
                value='',
            ),
        ]

    class TestVariableContainer(QuoteCostingVariableMixin):
        # TestVariableContainer is a fake QuoteOperation (or anything else that inherits
        # from QuoteCostingVariableMixin)
        def __init__(self, vars: List[QuoteCostingVariable]):
            super().__init__(costing_variables=vars)

    def test_basic_variables(self):
        tvc = self.TestVariableContainer(vars=self.basic_vars)
        cvs = get_costing_variable_updates(tvc)
        self.assertTrue(cvs.get('drop_down_variables') is None)
        self.assertTrue(cvs.get('table_variables') is None)
        basic_vars = cvs['variables']
        self.assertTrue(basic_vars is not None)
        self.assertEqual(
            len(basic_vars),
            2,
            f'unexpected basic vars collection length:{len(basic_vars)}',
        )
        non_qs = basic_vars.get('test_basic')
        self.assertTrue(non_qs is not None)
        self.assertEqual(non_qs, 1.024)
        qs = basic_vars.get('test_basic_qs')
        self.assertTrue(isinstance(qs, dict))
        self.assertTrue(len(qs) == 3)
        self.assertEqual(qs[1], 1.5)
        self.assertTrue(qs[2])
        self.assertEqual(qs[3], 'test')

    def test_drop_down_variables(self):
        tvc = self.TestVariableContainer(vars=self.drop_down_vars)
        cvs = get_costing_variable_updates(tvc)
        self.assertTrue(cvs.get('variables') is None)
        self.assertTrue(cvs.get('table_variables') is None)
        dd_vars = cvs['drop_down_variables']
        self.assertEqual(
            len(dd_vars),
            2,
            f'unexpected drop-down vars collection length:{len(dd_vars)}',
        )
        non_qs = dd_vars.get('test_dd')
        self.assertTrue(non_qs is not None)
        self.assertEqual(non_qs, 'something here')
        qs = dd_vars.get('test_dd_qs')
        self.assertTrue(isinstance(qs, dict))
        self.assertTrue(len(qs) == 3)
        self.assertEqual(qs[1], 1)
        self.assertTrue(qs[2] is False)
        self.assertEqual(qs[3], 'words')

    def test_table_variables(self):
        tvc = self.TestVariableContainer(vars=self.table_vars)
        cvs = get_costing_variable_updates(tvc)
        self.assertTrue(cvs.get('variables') is None)
        self.assertTrue(cvs.get('drop_down_variables') is None)
        t_vars = cvs['table_variables']
        self.assertEqual(
            len(t_vars), 2, f'unexpected table vars collection length:{len(t_vars)}'
        )
        non_qs = t_vars.get('test_table')
        self.assertTrue(non_qs is not None)
        self.assertTrue(isinstance(non_qs, dict))
        self.assertEqual(non_qs, dict(key1='some value', key2=42, key3=True))
        qs = t_vars.get('test_table_qs')
        self.assertTrue(isinstance(qs, dict))
        self.assertTrue(len(qs) == 2)
        self.assertEqual(qs[1], dict(key1='string', key2=25, key3=False))
        self.assertEqual(qs[5], dict(key1='another string', key2=100, key3=True))


class TestQuoteComponentUpdatePayload(unittest.TestCase):
    def setUp(self):
        with open('tests/unit/mock_data/quote.json') as data_file:
            quote_json = json.load(data_file)
        self.test_component = quote_json['quote_items'][0]['components'][1]

    def test_component_level_updates(self):
        ctor_args = QuoteComponentMapper.map(self.test_component)
        qc = QuoteComponent(**ctor_args)
        self.assertTrue(isinstance(qc, QuoteComponent))
        updates = get_component_costing_updates(qc)
        self.assertTrue(isinstance(updates, dict))
        self.assertEqual(len(updates), 9)
        self.assertEqual(
            list(updates.keys()),
            [89927, 89928, 89929, 89930, 89931, 89932, 89933, 89934, 89935],
        )
