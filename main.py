class CustomerManager:
    def __init__(self):
        self.customers = {}
        self.tax_rate = 0.2
        self.tax_threshold = 100
        self.discount_threshold = 500

    def add_customer(self, name, purchases):
        if name in self.customers:
            self.customers[name].extend(purchases)
        else:
            self.customers[name] = purchases

    def add_purchase(self, name, purchase):
        self.add_customer(name, [purchase])

    def add_purchases(self, name, purchases):
        self.add_customer(name, purchases)

    def generate_report(self):
        for customer_name, purchases in self.customers.items():
            total_spent = self._calculate_total_spent(purchases)
            print(customer_name)
            self._print_discount_status(total_spent)
            self._print_priority_status(total_spent)

    def _calculate_total_spent(self, purchases):
        total_spent = 0
        for purchase in purchases:
            total_spent += self._apply_tax_if_needed(purchase["price"])
        return total_spent

    def _apply_tax_if_needed(self, price):
        if price > self.tax_threshold:
            return price * (1 + self.tax_rate)
        return price

    def _print_discount_status(self, total_spent):
        if total_spent > self.discount_threshold:
            print("Eligible for discount")
        elif total_spent > 300:
            print("Potential future discount customer")
        else:
            print("No discount")

    def _print_priority_status(self, total_spent):
        if total_spent > 1000:
            print("VIP Customer!")
        elif total_spent > 800:
            print("Priority Customer")

    def calculate_shipping_fee(self, purchases):
        return _calculate_shipping_fee_by_rule(
            purchases,
            lambda purchase: purchase.get("weight", 0) > 20,
            50,
            20,
        )


def _calculate_shipping_fee_by_rule(purchases, condition, matched_fee, default_fee):
    for purchase in purchases:
        if condition(purchase):
            return matched_fee
    return default_fee


def calculate_shipping_fee_for_heavy_items(purchases):
    return _calculate_shipping_fee_by_rule(
        purchases,
        lambda purchase: purchase.get("weight", 0) > 20,
        50,
        20,
    )


def calculate_shipping_fee_for_fragile_items(purchases):
    return _calculate_shipping_fee_by_rule(
        purchases,
        lambda purchase: purchase.get("fragile", False),
        60,
        25,
    )


flat_tax = 0.2