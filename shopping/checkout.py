
from decimal import Decimal


class Checkout(object):
    def __init__(self, pricing_rules):
        """ Checkout is used to scan items from a shopping cart. It applies
            the pricing rules provided to calculate the total amount to pay.

        Args:
            pricing_rules: a dictionary of price and discount rules
                           applicable to each item.
        """
        self.pricing_rules = pricing_rules
        self.scanned_items = {}
        self._total = Decimal(0)

    def scan(self, item):
        """ Scans Item for checkout.

        Args:
            item: stock keeping unit (SKU) for the item.
        Raises:
            ItemNotFound: If the scanned item's SKU does not exist in the pricing rules.
        """
        if item not in self.pricing_rules:
            raise ValueError('Item %s is not known.', item)
        if item in self.scanned_items:
            self.scanned_items[item] += 1
        else:
            self.scanned_items[item] = 1

    def total(self):
        """ Adds the total price for all scanned items.
            Discounts are applied according to the rules.

        Returns:
            The total price.
        """
        for item in self.scanned_items:
            pricing_rule = self.pricing_rules[item]
            self._total += Decimal(pricing_rule['Price'])
        return self._total
