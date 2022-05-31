# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from concurrent.futures import process
import unittest

from reports.fields import Field, Fields
from reports.utils import get_value

class TestField(unittest.TestCase):
    def test_name(self):
        t = Field('test-name', None)
        self.assertEqual(t.name, 'test-name')
    
    def test_f(self):
        f = lambda x, y: x+y
        t = Field('test-name', f)
        self.assertEqual(t.f, f)
        self.assertEqual(t.f('hello', 'world'), 'helloworld')


class TestFields(unittest.TestCase):
    def test_names(self):
        l = (
            Field('first', None),
            Field('Second Field', None),
            Field('third field', None),
        )
        t = Fields(l)
        self.assertEqual(list(t.names()), ['first', 'Second Field', 'third field'])

    def test_json_names(self):
        l = (
            Field('first', None),
            Field('Second Field', None),
            Field('third field', None),
        )
        t = Fields(l)
        self.assertEqual(list(t.json_names()), ['first', 'second_field', 'third_field'])

    def test_process(self):
        r = {
            "id": "test-request-id",
            "type": "test-request-type",
            "asset": {
                "id": "test-asset-id",
                "product": {
                    "id": "test-product-id",
                    "name": "test-product-name"
                },
                "connection": {
                    "hub": {
                        "id": "test-hub-id",
                        "name": "test-hub-name"
                    }
                }
            }
        }
        l = (
            Field('Request ID', lambda r: get_value(r, 'id')),
            Field('Request Type', lambda r: get_value(r, 'type')),
            Field('Product ID', lambda r: get_value(r, 'asset.product.id')),
            Field('Product Name', lambda r: get_value(r, 'asset.product.name')),
            Field('Asset ID', lambda r: get_value(r, 'asset.id')),
            Field('Hub ID', lambda r: get_value(r, 'asset.connection.hub.id')),
            Field('Hub Name', lambda r: get_value(r, 'asset.connection.hub.name')),
        )
        t = Fields(l)
        expectedValues = [
            'test-request-id',
            'test-request-type',
            'test-product-id',
            'test-product-name',
            'test-asset-id',
            'test-hub-id',
            'test-hub-name'
        ]
        self.assertEqual(list(t.process(r)), expectedValues)


if __name__ == '__main__':
    unittest.main()
