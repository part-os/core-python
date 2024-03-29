import unittest

from paperless.objects.quotes import CostingVariablePayload
from paperless.objects.utils import safe_init


class TestObjects(unittest.TestCase):
    def test_safe_instantiate(self):
        attr_class = CostingVariablePayload
        with self.assertRaises(TypeError):
            attr_class(value=1, row=None, options=None, new_kwarg=1)

        cvp = safe_init(attr_class, dict(value=1, row=None, options=None, new_kwarg=1))
        self.assertEqual(1, cvp.value)
        self.assertIsNone(cvp.row)
        self.assertIsNone(cvp.options)

        d = safe_init(dict, dict(value=2, row=None, options=None, new_kwarg=1))
        self.assertTrue(isinstance(d, dict))
        self.assertEqual(2, d['value'])
