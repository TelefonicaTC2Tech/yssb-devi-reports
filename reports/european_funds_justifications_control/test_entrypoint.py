# -*- coding: utf-8 -*-
#
# Copyright (c) 2022, Telefónica Cybersecurity & Cloud Tech
#

from concurrent.futures import process
import unittest

from reports.european_funds_justifications_control.entrypoint import _get_european_fund_packet


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


# This request does not match with basic packet for EU funds because it contains the item 'Secure Office'
PR_NO_FUNDS_BASIC = {
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


PR_NO_FUNDS_ADVANCED = {
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



class TestFunds(unittest.TestCase):
    def test_get_european_fund_packet_with_no_funds_basic(self):
        packet = _get_european_fund_packet(PR_NO_FUNDS_BASIC)
        self.assertEqual(packet, '')

    def test_get_european_fund_packet_with_funds_basic(self):
        packet = _get_european_fund_packet(PR_FUNDS_BASIC)
        self.assertEqual(packet, 'Basic')

    def test_get_european_fund_packet_with_no_funds_advanced(self):
        packet = _get_european_fund_packet(PR_NO_FUNDS_ADVANCED)
        self.assertEqual(packet, '')

    def test_get_european_fund_packet_with_funds_advanced(self):
        packet = _get_european_fund_packet(PR_FUNDS_ADVANCED)
        self.assertEqual(packet, 'Advanced')
