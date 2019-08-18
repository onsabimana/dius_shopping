import decimal
import json
import unittest

from shopping import checkout

# A list of test cases to check total prices
TEST_CASES = [
    {
        'test_case': 'No discount simple case',
        'shopping_cart': ['ipd', 'mbp', 'atv', 'vga'],
        'expected_total': '2089.48'
    }
]


class TestCheckout(unittest.TestCase):
    def setUp(self):
        self.pricing_rules = {}

        with open('pricing_rules.json', 'r') as f:
            self.pricing_rules = json.load(f)

        self.checkout = checkout.Checkout(self.pricing_rules)

    def test_scan_known_product(self):
        for item in self.pricing_rules:
            self.checkout.scan(item)

        self.assertEqual(len(self.pricing_rules),
                         len(self.checkout.scanned_items),
                         msg="All items in pricing rules are not scanned successfully")

    def test_scan_unkown_product(self):
        with self.assertRaises(ValueError):
            self.checkout.scan('unkownproduct')

    def test_total(self):
        for test_case in TEST_CASES:
            for item in test_case['shopping_cart']:
                self.checkout.scan(item)
            self.assertEqual(self.checkout.total(),
                             decimal.Decimal(test_case['expected_total']),
                             msg='Test case: %s' % test_case)
