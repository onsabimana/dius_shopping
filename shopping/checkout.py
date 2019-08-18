""" Checkout Module """

from decimal import Decimal


class Checkout():
    """Checkout is used to scan items from a shopping cart. It applies
    the pricing rules provided to calculate the total amount to pay.
    """
    def __init__(self, pricing_rules):
        """
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
            raise ValueError('Item %s is not known.' % item)
        if item in self.scanned_items:
            self.scanned_items[item] += 1
        else:
            self.scanned_items[item] = 1

    def clear(self):
        """Clears the scanned items and total prices."""
        self._total = Decimal(0)
        self.scanned_items = {}

    def total(self):
        """ Adds the total price for all scanned items.
            Discounts are applied according to the rules.

        Returns:
            The total price.
        """
        for item in self.scanned_items:
            item_price_rule = self.pricing_rules[item]
            item_count = self.scanned_items[item]
            multiplier = item_price_rule['Discount']['Multiplier']
            divider = item_price_rule['Discount']['Divider']
            discount_threshold_count = item_price_rule['Discount']['ItemCount']

            sales_price = Decimal(item_count) * \
                Decimal(item_price_rule['Price'])

            # Bulk discount pricing on iPad more than 4 purchased.
            if item == 'ipd' and item_count > discount_threshold_count:
                sales_price = Decimal(item_count) * \
                    Decimal(item_price_rule['Discount']['Price'])

            # VGA Adapter is given free for each MacBook Pro Purchase
            # The discount is dependent on another item being in the cart.
            # This prove challenging to generalise as it has at least one level of indirection.
            # TBD: Figure out how to represent this case in the price model.
            if item == 'vga' and 'mbp' in self.scanned_items:
                if self.scanned_items['mbp'] > item_count:
                    sales_price = Decimal(0)
                else:
                    # Charge for VGA not matching one-to-one with MacBook Pro
                    sales_price = Decimal(
                        item_count - self.scanned_items['mbp']) * \
                        Decimal(item_price_rule['Price'])

            # Selective discount pricing.
            # E.g 3 for 2 type of discount.
            # We use the concept of multiplier and divider in an attempt
            # to generalise this calculation. The modulus operation is used to project
            # the actual item counts to the chargeable count.
            # For example in the case above (3 -> 2) if you bought 7 items you pay for 5.
            # Mod(7, 3) == 1 to find the number of items not included in the discount.
            # 7 - 1 == 6 which the number of items to be included in the discount.
            # If 3 -> 2 then 6 -> 4. Therefore you pay for the tital of (4 + 1) == 5 items.
            if item == 'atv' and item_count >= discount_threshold_count:
                remainder = item_count % discount_threshold_count
                new_item_count = remainder + multiplier * \
                    (item_count - remainder) / divider
                sales_price = Decimal(new_item_count) * \
                    Decimal(item_price_rule['Price'])

            self._total += sales_price
        return self._total
