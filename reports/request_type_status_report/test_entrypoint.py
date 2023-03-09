# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from concurrent.futures import process
import unittest

from reports.request_type_status_report.entrypoint import _get_operation


PR_PURCHASED = {
    "type": "purchase"
}

PR_CANCEL = {
    "type": "cancel"
}

PR_ADJUSTMENT = {
    "type": "adjustment"
}

PR_CHANGE = {
    "type": "change"
}

PR_SUSPEND = {
    "type": "suspend"
}

class TestLastestSubscriptionsChanges(unittest.TestCase):
    def test_purchase(self):
        operation = _get_operation(PR_PURCHASED)
        self.assertEqual(operation, 'A')
    def test_cancel(self):
        operation = _get_operation(PR_CANCEL)
        self.assertEqual(operation, 'B')

    def test_adjustment(self):
        operation = _get_operation(PR_ADJUSTMENT)
        self.assertEqual(operation, 'M')

    def test_change(self):
        operation = _get_operation(PR_CHANGE)
        self.assertEqual(operation, 'M')

    def test_suspend(self):
        operation = _get_operation(PR_SUSPEND)
        self.assertEqual(operation, None)
