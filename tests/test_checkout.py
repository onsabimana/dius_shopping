import decimal
import json
import unittest

from shopping import checkout

# A list of test cases to check total prices
TEST_CASES = [
    {
        'test_case': 'No discount simple case',
        'shopping_cart': ['ipd', 'mbp', 'atv'],
        'expected_total': '2059.48'
    },
    {
        'test_case': 'No discount simple case double',
        'shopping_cart': ['ipd', 'ipd', 'mbp', 'mbp', 'atv', 'atv'],
        'expected_total': '4118.96'
    },
    {
        'test_case': '3 for 2 ATV',
        'shopping_cart': ['atv', 'atv', 'atv', 'vga'],
        'expected_total': '249.00'
    },
    {
        'test_case': 'Discount for 4 or more IPD',
        'shopping_cart': ['atv', 'ipd', 'ipd', 'atv', 'ipd', 'ipd', 'ipd'],
        'expected_total': '2718.95'
    },
    {
        'test_case': 'No discount for 4 IPD.',
        'shopping_cart': ['atv', 'ipd', 'ipd', 'atv', 'ipd', 'ipd'],
        'expected_total': '2418.96'
    },
    {
        'test_case': 'Free VGA for Macbook Pro Purchase',
        'shopping_cart': ['mbp', 'vga', 'ipd'],
        'expected_total': '1949.98'
    },
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

    def test_clear(self):
        # Initially all initialized to 0.
        self.assertEqual(len(self.checkout.scanned_items), 0)
        self.assertEqual(self.checkout.total(), 0)

        # scan new items in
        self.checkout.scan('atv')
        self.checkout.scan('vga')

        self.assertNotEqual(len(self.checkout.scanned_items), 0)
        self.assertNotEqual(self.checkout.total(), 0)

        # clear
        self.checkout.clear()
        self.assertEqual(len(self.checkout.scanned_items), 0)
        self.assertEqual(self.checkout.total(), 0)

    def test_total(self):
        for test_case in TEST_CASES:
            self.checkout.clear()
            for item in test_case['shopping_cart']:
                self.checkout.scan(item)
            self.assertEqual(self.checkout.total(),
                             decimal.Decimal(test_case['expected_total']),
                             msg='Test case: %s' % test_case)
