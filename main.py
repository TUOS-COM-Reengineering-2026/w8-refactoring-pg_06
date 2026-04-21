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
        for name, purchases in self.customers.items():
            total_cost = self._calculate_total_cost(purchases)
            print(name)
            print(self._discount_status(total_cost))

            customer_priority = self._customer_priority(total_cost)
            if customer_priority:
                print(customer_priority)

    def _calculate_total_cost(self, purchases):
        total_cost = 0
        for purchase in purchases:
            total_cost += self._price_with_tax(purchase['price'])
        return total_cost

    def _price_with_tax(self, price):
        if price > self.tax_threshold:
            return price * (1 + self.tax_rate)
        return price

    def _discount_status(self, total_cost):
        if total_cost > self.discount_threshold:
            return "Eligible for discount"
        if total_cost > 300:
            return "Potential future discount customer"
        return "No discount"

    def _customer_priority(self, total_cost):
        if total_cost > 1000:
            return "VIP Customer!"
        if total_cost > 800:
            return "Priority Customer"
        return None

    def calculate_shipping_fee(self, purchases):
        return calculate_shipping_fee_for_heavy_items(purchases)

def calculate_shipping_fee_for_heavy_items(purchases):
    for purchase in purchases:
        if purchase.get('weight', 0) > 20:
            return 50
    return 20

def calculate_shipping_fee_for_fragile_items(purchases):
    for purchase in purchases:
        if purchase.get('fragile', False):
            return 60
    return 25

flat_tax = 0.2
