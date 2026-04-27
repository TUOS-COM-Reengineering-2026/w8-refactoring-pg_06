import unittest
import io
import contextlib

from main import (
    CustomerManager,
    calculate_shipping_fee_for_fragile_items,
    calculate_shipping_fee_for_heavy_items,
)

class TestCustomerManager(unittest.TestCase):
    def capture_report(self, customer_manager):
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            customer_manager.generate_report()
        return captured.getvalue()

    def test_add_customer(self):
        cm = CustomerManager()
        name = "Alice"
        purchases = [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]
        cm.add_customer(name, purchases)

        self.assertEqual(
            {name: purchases},
            cm.customers
        )

    def test_add_purchase(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase]},
            cm.customers
        )

    def test_add_purchase_multiple(self):
        cm = CustomerManager()
        name = "Alice"
        purchase = {'price': 50, 'item': 'banana'}
        cm.add_purchase(name, purchase)
        cm.add_purchase(name, purchase)

        self.assertEqual(
            {name: [purchase, purchase]},
            cm.customers
        )

    def test_add_purchases(self):
        cm = CustomerManager()
        cm.add_customer("Alice", [{'price': 50, 'item': 'banana'}])
        cm.add_purchases("Alice", [{'price': 80, 'item': 'apple'}])

        self.assertEqual(
            {"Alice": [{'price': 50, 'item': 'banana'}, {'price': 80, 'item': 'apple'}]},
            cm.customers
        )

    def test_discount_eligibility(self):
        cm = CustomerManager()
        cm.add_customer("Bob", [{'price': 600}])

        output = self.capture_report(cm)

        self.assertIn("Bob", output)
        self.assertIn("Eligible for discount", output)

    def test_no_discount_report_for_lower_spend_customer(self):
        cm = CustomerManager()
        cm.add_customer("Alice", [{'price': 50}, {'price': 80}])

        output = self.capture_report(cm)

        self.assertIn("Alice", output)
        self.assertIn("No discount", output)
        self.assertNotIn("Priority Customer", output)
        self.assertNotIn("VIP Customer!", output)

    def test_potential_future_discount_report(self):
        cm = CustomerManager()
        cm.add_customer("Carol", [{'price': 200}, {'price': 100}])

        output = self.capture_report(cm)

        self.assertIn("Carol", output)
        self.assertIn("Potential future discount customer", output)

    def test_priority_customer_report(self):
        cm = CustomerManager()
        cm.add_customer("Dora", [{'price': 700}])

        output = self.capture_report(cm)

        self.assertIn("Dora", output)
        self.assertIn("Eligible for discount", output)
        self.assertIn("Priority Customer", output)
        self.assertNotIn("VIP Customer!", output)

    def test_vip_customer_report(self):
        cm = CustomerManager()
        cm.add_customer("Eve", [{'price': 900}])

        output = self.capture_report(cm)

        self.assertIn("Eve", output)
        self.assertIn("Eligible for discount", output)
        self.assertIn("VIP Customer!", output)

    def test_heavy_item_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 100, 'weight': 25}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 50)

    def test_heavy_item_shipping_fee_function(self):
        heavy_purchases = [{'price': 100, 'weight': 25}]
        light_purchases = [{'price': 100, 'weight': 10}]

        self.assertEqual(calculate_shipping_fee_for_heavy_items(heavy_purchases), 50)
        self.assertEqual(calculate_shipping_fee_for_heavy_items(light_purchases), 20)

    def test_fragile_item_shipping_fee(self):
        purchases = [{'price': 70, 'fragile': True}]

        fee = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee, 60)

    def test_no_special_items_shipping_fee(self):
        cm = CustomerManager()
        purchases = [{'price': 40, 'weight': 5, 'fragile': False}]

        fee = cm.calculate_shipping_fee(purchases)
        self.assertEqual(fee, 20)

        fee_fragile = calculate_shipping_fee_for_fragile_items(purchases)
        self.assertEqual(fee_fragile, 25)

if __name__ == "__main__":
    unittest.main()
