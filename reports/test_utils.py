# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

import unittest

from reports.utils import get_value, get_value_from_array_by_id

class TestUtilsGetValue(unittest.TestCase):
    def _build_test_dict(self):
        return {
            "asset": {
                "tiers": {
                    "tier1": "test tier 1",
                    "tier2": "test tier 2",
                    "tier3": "test tier 3"
                },
                "numerical": 4,
                "boolean": True,
                "array": ['one', 'two', 'three']
            }
        }

    def test_none_dict(self):
        d = None
        self.assertEqual(get_value(d, 'asset.tiers.tier1'), '-')
        self.assertEqual(get_value(d, 'asset.tiers.tier1', '***'), '***')

    def test_get_valid_value(self):
        d = self._build_test_dict()
        self.assertEqual(get_value(d, 'asset.tiers.tier1'), 'test tier 1')
        self.assertEqual(get_value(d, 'asset.tiers.tier2'), 'test tier 2')
        self.assertEqual(get_value(d, 'asset.tiers.tier3'), 'test tier 3')
        self.assertEqual(get_value(d, 'asset.numerical'), 4)
        self.assertEqual(get_value(d, 'asset.boolean'), True)
        self.assertEqual(get_value(d, 'asset.array'), ['one', 'two', 'three'])

    def test_get_invalid_value(self):
        d = self._build_test_dict()
        self.assertEqual(get_value(d, 'invalid'), '-')
        self.assertEqual(get_value(d, 'invalid.invalid'), '-')
        self.assertEqual(get_value(d, 'not.existent.key'), '-')
        self.assertEqual(get_value(d, 'asset.tiers.invalid'), '-')

    def test_get_valid_value_with_default(self):
        d = self._build_test_dict()
        self.assertEqual(get_value(d, 'asset.tiers.tier1', '***'), 'test tier 1')
        self.assertEqual(get_value(d, 'asset.tiers.tier2', '***'), 'test tier 2')
        self.assertEqual(get_value(d, 'asset.tiers.tier3', '***'), 'test tier 3')
        self.assertEqual(get_value(d, 'asset.numerical', '***'), 4)
        self.assertEqual(get_value(d, 'asset.boolean', '***'), True)
        self.assertEqual(get_value(d, 'asset.array', '***'), ['one', 'two', 'three'])

    def test_get_invalid_value_with_default(self):
        d = self._build_test_dict()
        self.assertEqual(get_value(d, 'invalid', '***'), '***')
        self.assertEqual(get_value(d, 'invalid.invalid', '***'), '***')
        self.assertEqual(get_value(d, 'not.existent.key', '***'), '***')
        self.assertEqual(get_value(d, 'asset.tiers.invalid', '***'), '***')


class TestUtilsGetValueFromArrayById(unittest.TestCase):
    def _build_test_dict(self):
        return {
            "asset": {
                "tiers": {
                    "tier1": "test tier 1",
                    "tier2": "test tier 2",
                    "tier3": "test tier 3"
                },
                "numerical": 4,
                "boolean": True,
                "array": ['one', 'two', 'three'],
                "params": [
                    {
                        "id": "technicalContact",
                        "value": "foo@domain.com",
                        "value_error": ""
                    },
                    {
                        "id": "technicalName",
                        "value": "Foo Foo",
                        "value_error": ""
                    },
                    {
                        "id": "domain",
                        "value": "",
                        "value_error": "error in domain"
                    },
                    {
                        "value": "",
                        "value_error": "no id"
                    }
                ]
            }
        }

    def test_none_dict(self):
        d = None
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalName', 'value'), '-')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalName', 'value', '***'), '***')

    def test_get_valid_param_value(self):
        d = self._build_test_dict()
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalContact', 'value'), 'foo@domain.com')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalContact', 'value_error'), '')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalName', 'value'), 'Foo Foo')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalName', 'value_error'), '')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'domain', 'value'), '')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'domain', 'value_error'), 'error in domain')

    def test_get_valid_param_value_with_default(self):
        d = self._build_test_dict()
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalContact', 'value', '***'), 'foo@domain.com')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalContact', 'value_error', '***'), '')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalName', 'value', '***'), 'Foo Foo')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'technicalName', 'value_error', '***'), '')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'domain', 'value', '***'), '')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'domain', 'value_error', '***'), 'error in domain')

    def test_get_invalid_param_value(self):
        d = self._build_test_dict()
        self.assertEqual(get_value_from_array_by_id(d, 'invalid.params', 'technicalContact', 'value'), '-')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'invalid', 'value'), '-')

    def test_get_invalid_param_value_with_default(self):
        d = self._build_test_dict()
        self.assertEqual(get_value_from_array_by_id(d, 'invalid.params', 'technicalContact', 'value', '***'), '***')
        self.assertEqual(get_value_from_array_by_id(d, 'asset.params', 'invalid', 'value', '***'), '***')

if __name__ == '__main__':
    unittest.main()
