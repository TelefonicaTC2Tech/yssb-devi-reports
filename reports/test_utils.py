# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

import unittest

from reports.utils import get_request_type, get_subscription_type, get_value, get_value_from_array_by_id

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

class TestUtilsGetRequestType(unittest.TestCase):

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

    def test_purchase(self):
        operation = get_request_type(self.PR_PURCHASED)
        self.assertEqual(operation, 'A')
    def test_cancel(self):
        operation = get_request_type(self.PR_CANCEL)
        self.assertEqual(operation, 'B')

    def test_adjustment(self):
        operation = get_request_type(self.PR_ADJUSTMENT)
        self.assertEqual(operation, 'M')

    def test_change(self):
        operation = get_request_type(self.PR_CHANGE)
        self.assertEqual(operation, 'M')

    def test_suspend(self):
        operation = get_request_type(self.PR_SUSPEND)
        self.assertEqual(operation, None)

class TestUtilsGetSubscriptionType(unittest.TestCase):
    PR_FUNDS_BASIC = {
	"id": "PR-7815-9060-2103-001",
	"type": "purchase",
	"asset": {
		"id": "AS-7815-9060-2103",
		"status": "active",
		"items": [{
			"id": "PRD_553_048_740_0003",
			"global_id": "PRD-553-048-740-0003",
			"mpn": "SEC_SMB_AA",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Users",
			"display_name": "Antivirus Antiransomware",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0001",
			"global_id": "PRD-553-048-740-0001",
			"mpn": "SEC_SMB_SB",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Users",
			"display_name": "Secure Browsing",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0004",
			"global_id": "PRD-553-048-740-0004",
			"mpn": "SEC_SMB_CE",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Users",
			"display_name": "Clean email",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0006",
			"global_id": "PRD-553-048-740-0006",
			"mpn": "SEC_SMB_SO",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Secure Office",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0007",
			"global_id": "PRD-553-048-740-0007",
			"mpn": "SEC_SMB_RA",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Secure Remote Access",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0009",
			"global_id": "PRD-553-048-740-0009",
			"mpn": "SEC_SMB_AW",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Awareness",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0010",
			"global_id": "PRD-553-048-740-0010",
			"mpn": "SEC_SMB_PCS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protected Cloud  Services",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0012",
			"global_id": "PRD-553-048-740-0012",
			"mpn": "SEC_SMB_UTM_UP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "UTM Upgrade",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0013",
			"global_id": "PRD-553-048-740-0013",
			"mpn": "SEC_SMB_HA",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "High Availability",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0016",
			"global_id": "PRD-553-048-740-0016",
			"mpn": "SEC_SMB_DS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Digital Signature",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0002",
			"global_id": "PRD-553-048-740-0002",
			"mpn": "SEC_SMB_CB",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Cloud backup",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0005",
			"global_id": "PRD-553-048-740-0005",
			"mpn": "SEC_SMB_SU",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Support",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0008",
			"global_id": "PRD-553-048-740-0008",
			"mpn": "SEC_SMB_POP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protect Online Presence",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0014",
			"global_id": "PRD-553-048-740-0014",
			"mpn": "SEC_SMB_CS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Ciberseguro",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0015",
			"global_id": "PRD-553-048-740-0015",
			"mpn": "SEC_SMB_GDPR",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "GDPR Lite",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0022",
			"global_id": "PRD-553-048-740-0022",
			"mpn": "SEC_SMB_REC_FUNDS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "NextGeneration EU subsidized",
			"period": "Monthly",
			"item_type": "Reservation"
		}]
	}
}
    
    PR_BASIC = {
	"id": "PR-7815-9060-2103-001",
	"type": "purchase",
	"asset": {
		"id": "AS-7815-9060-2103",
		"status": "active",
		"items": [{
			"id": "PRD_553_048_740_0003",
			"global_id": "PRD-553-048-740-0003",
			"mpn": "SEC_SMB_AA",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Users",
			"display_name": "Antivirus Antiransomware",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0001",
			"global_id": "PRD-553-048-740-0001",
			"mpn": "SEC_SMB_SB",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Users",
			"display_name": "Secure Browsing",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0004",
			"global_id": "PRD-553-048-740-0004",
			"mpn": "SEC_SMB_CE",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Users",
			"display_name": "Clean email",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0006",
			"global_id": "PRD-553-048-740-0006",
			"mpn": "SEC_SMB_SO",
			"old_quantity": "0",
			"quantity": "20",
			"type": "Units",
			"display_name": "Secure Office",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0007",
			"global_id": "PRD-553-048-740-0007",
			"mpn": "SEC_SMB_RA",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Secure Remote Access",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0009",
			"global_id": "PRD-553-048-740-0009",
			"mpn": "SEC_SMB_AW",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Awareness",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0010",
			"global_id": "PRD-553-048-740-0010",
			"mpn": "SEC_SMB_PCS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protected Cloud  Services",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0012",
			"global_id": "PRD-553-048-740-0012",
			"mpn": "SEC_SMB_UTM_UP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "UTM Upgrade",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0013",
			"global_id": "PRD-553-048-740-0013",
			"mpn": "SEC_SMB_HA",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "High Availability",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0016",
			"global_id": "PRD-553-048-740-0016",
			"mpn": "SEC_SMB_DS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Digital Signature",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0002",
			"global_id": "PRD-553-048-740-0002",
			"mpn": "SEC_SMB_CB",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Cloud backup",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0005",
			"global_id": "PRD-553-048-740-0005",
			"mpn": "SEC_SMB_SU",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Support",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0008",
			"global_id": "PRD-553-048-740-0008",
			"mpn": "SEC_SMB_POP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protect Online Presence",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0014",
			"global_id": "PRD-553-048-740-0014",
			"mpn": "SEC_SMB_CS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Ciberseguro",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0015",
			"global_id": "PRD-553-048-740-0015",
			"mpn": "SEC_SMB_GDPR",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "GDPR Lite",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0022",
			"global_id": "PRD-553-048-740-0022",
			"mpn": "SEC_SMB_REC_FUNDS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "NextGeneration EU subsidized",
			"period": "Monthly",
			"item_type": "Reservation"
		}]
	}
}

    PR_ADVANCED = {
	"id": "PR-9417-9411-3087-001",
	"type": "purchase",
	"asset": {
		"id": "AS-9417-9411-3087",
		"status": "active",
		"items": [{
			"id": "PRD_553_048_740_0003",
			"global_id": "PRD-553-048-740-0003",
			"mpn": "SEC_SMB_AA",
			"old_quantity": "0",
			"quantity": "10",
			"type": "Users",
			"display_name": "Antivirus Antiransomware",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0001",
			"global_id": "PRD-553-048-740-0001",
			"mpn": "SEC_SMB_SB",
			"old_quantity": "0",
			"quantity": "10",
			"type": "Users",
			"display_name": "Secure Browsing",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0004",
			"global_id": "PRD-553-048-740-0004",
			"mpn": "SEC_SMB_CE",
			"old_quantity": "0",
			"quantity": "10",
			"type": "Users",
			"display_name": "Clean email",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0006",
			"global_id": "PRD-553-048-740-0006",
			"mpn": "SEC_SMB_SO",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Secure Office",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0007",
			"global_id": "PRD-553-048-740-0007",
			"mpn": "SEC_SMB_RA",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Secure Remote Access",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0009",
			"global_id": "PRD-553-048-740-0009",
			"mpn": "SEC_SMB_AW",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Awareness",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0010",
			"global_id": "PRD-553-048-740-0010",
			"mpn": "SEC_SMB_PCS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protected Cloud  Services",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0012",
			"global_id": "PRD-553-048-740-0012",
			"mpn": "SEC_SMB_UTM_UP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "UTM Upgrade",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0013",
			"global_id": "PRD-553-048-740-0013",
			"mpn": "SEC_SMB_HA",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "High Availability",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0016",
			"global_id": "PRD-553-048-740-0016",
			"mpn": "SEC_SMB_DS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Digital Signature",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0002",
			"global_id": "PRD-553-048-740-0002",
			"mpn": "SEC_SMB_CB",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Cloud backup",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0005",
			"global_id": "PRD-553-048-740-0005",
			"mpn": "SEC_SMB_SU",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Support",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0008",
			"global_id": "PRD-553-048-740-0008",
			"mpn": "SEC_SMB_POP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protect Online Presence",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0014",
			"global_id": "PRD-553-048-740-0014",
			"mpn": "SEC_SMB_CS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Ciberseguro",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0015",
			"global_id": "PRD-553-048-740-0015",
			"mpn": "SEC_SMB_GDPR",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "GDPR Lite",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0022",
			"global_id": "PRD-553-048-740-0022",
			"mpn": "SEC_SMB_REC_FUNDS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "NextGeneration EU subsidized",
			"period": "Monthly",
			"item_type": "Reservation"
		}]
	},
	"status": "approved"
}

    PR_FUNDS_ADVANCED = {
	"id": "PR-2343-6217-1336-001",
	"type": "purchase",
	"asset": {
		"id": "AS-2343-6217-1336",
		"status": "active",
		"items": [{
			"id": "PRD_553_048_740_0003",
			"global_id": "PRD-553-048-740-0003",
			"mpn": "SEC_SMB_AA",
			"old_quantity": "0",
			"quantity": "23",
			"type": "Users",
			"display_name": "Antivirus Antiransomware",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0001",
			"global_id": "PRD-553-048-740-0001",
			"mpn": "SEC_SMB_SB",
			"old_quantity": "0",
			"quantity": "23",
			"type": "Users",
			"display_name": "Secure Browsing",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0004",
			"global_id": "PRD-553-048-740-0004",
			"mpn": "SEC_SMB_CE",
			"old_quantity": "0",
			"quantity": "23",
			"type": "Users",
			"display_name": "Clean email",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0006",
			"global_id": "PRD-553-048-740-0006",
			"mpn": "SEC_SMB_SO",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Secure Office",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0007",
			"global_id": "PRD-553-048-740-0007",
			"mpn": "SEC_SMB_RA",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Secure Remote Access",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0009",
			"global_id": "PRD-553-048-740-0009",
			"mpn": "SEC_SMB_AW",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Awareness",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0010",
			"global_id": "PRD-553-048-740-0010",
			"mpn": "SEC_SMB_PCS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protected Cloud  Services",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0012",
			"global_id": "PRD-553-048-740-0012",
			"mpn": "SEC_SMB_UTM_UP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "UTM Upgrade",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0013",
			"global_id": "PRD-553-048-740-0013",
			"mpn": "SEC_SMB_HA",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "High Availability",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0016",
			"global_id": "PRD-553-048-740-0016",
			"mpn": "SEC_SMB_DS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Digital Signature",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0002",
			"global_id": "PRD-553-048-740-0002",
			"mpn": "SEC_SMB_CB",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Cloud backup",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0005",
			"global_id": "PRD-553-048-740-0005",
			"mpn": "SEC_SMB_SU",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Support",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0008",
			"global_id": "PRD-553-048-740-0008",
			"mpn": "SEC_SMB_POP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protect Online Presence",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0014",
			"global_id": "PRD-553-048-740-0014",
			"mpn": "SEC_SMB_CS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Ciberseguro",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0015",
			"global_id": "PRD-553-048-740-0015",
			"mpn": "SEC_SMB_GDPR",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "GDPR Lite",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0022",
			"global_id": "PRD-553-048-740-0022",
			"mpn": "SEC_SMB_REC_FUNDS",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "NextGeneration EU subsidized",
			"period": "Monthly",
			"item_type": "Reservation"
		}],
    },
	"status": "approved",
}
   
    PR_PREMIUM = {
	"id": "PR-9417-9411-3087-001",
	"type": "purchase",
	"asset": {
		"id": "AS-9417-9411-3087",
		"status": "active",
		"items": [{
			"id": "PRD_553_048_740_0003",
			"global_id": "PRD-553-048-740-0003",
			"mpn": "SEC_SMB_AA",
			"old_quantity": "0",
			"quantity": "10",
			"type": "Users",
			"display_name": "Antivirus Antiransomware",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0001",
			"global_id": "PRD-553-048-740-0001",
			"mpn": "SEC_SMB_SB",
			"old_quantity": "0",
			"quantity": "10",
			"type": "Users",
			"display_name": "Secure Browsing",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0004",
			"global_id": "PRD-553-048-740-0004",
			"mpn": "SEC_SMB_CE",
			"old_quantity": "0",
			"quantity": "10",
			"type": "Users",
			"display_name": "Clean email",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0006",
			"global_id": "PRD-553-048-740-0006",
			"mpn": "SEC_SMB_SO",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Secure Office",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0007",
			"global_id": "PRD-553-048-740-0007",
			"mpn": "SEC_SMB_RA",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Secure Remote Access",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0009",
			"global_id": "PRD-553-048-740-0009",
			"mpn": "SEC_SMB_AW",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Awareness",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0010",
			"global_id": "PRD-553-048-740-0010",
			"mpn": "SEC_SMB_PCS",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "Protected Cloud  Services",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0012",
			"global_id": "PRD-553-048-740-0012",
			"mpn": "SEC_SMB_UTM_UP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "UTM Upgrade",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0013",
			"global_id": "PRD-553-048-740-0013",
			"mpn": "SEC_SMB_HA",
			"old_quantity": "0",
			"quantity": "1",
			"type": "Units",
			"display_name": "High Availability",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0016",
			"global_id": "PRD-553-048-740-0016",
			"mpn": "SEC_SMB_DS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Digital Signature",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0002",
			"global_id": "PRD-553-048-740-0002",
			"mpn": "SEC_SMB_CB",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Cloud backup",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0005",
			"global_id": "PRD-553-048-740-0005",
			"mpn": "SEC_SMB_SU",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Users",
			"display_name": "Support",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0008",
			"global_id": "PRD-553-048-740-0008",
			"mpn": "SEC_SMB_POP",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Protect Online Presence",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0014",
			"global_id": "PRD-553-048-740-0014",
			"mpn": "SEC_SMB_CS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "Ciberseguro",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0015",
			"global_id": "PRD-553-048-740-0015",
			"mpn": "SEC_SMB_GDPR",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "GDPR Lite",
			"period": "Monthly",
			"item_type": "Reservation"
		}, {
			"id": "PRD_553_048_740_0022",
			"global_id": "PRD-553-048-740-0022",
			"mpn": "SEC_SMB_REC_FUNDS",
			"old_quantity": "0",
			"quantity": "0",
			"type": "Units",
			"display_name": "NextGeneration EU subsidized",
			"period": "Monthly",
			"item_type": "Reservation"
		}]
	},
	"status": "approved"
}

    def test_get_basic_subscription(self):
        packet = get_subscription_type(self.PR_BASIC)
        self.assertEqual(packet, 'Paquete Básico')

    def test_get_basic_funds_subscription(self):
        packet = get_subscription_type(self.PR_FUNDS_BASIC)
        self.assertEqual(packet, 'Paquete Básico Fondos')

    def test_get_advanced_subscription(self):
        packet = get_subscription_type(self.PR_ADVANCED)
        self.assertEqual(packet, 'Paquete Avanzado')

    def test_get_advanced_funds_subscription(self):
        packet = get_subscription_type(self.PR_FUNDS_ADVANCED)
        self.assertEqual(packet, 'Paquete Avanzado Fondos')

    def test_get_premium_subscription(self):
        packet = get_subscription_type(self.PR_PREMIUM)
        self.assertEqual(packet, 'Paquete Premium')


if __name__ == '__main__':
    unittest.main()
