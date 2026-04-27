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
            total_spend = self._calculate_total_spend(purchases)
            print(customer_name)
            print(self._get_discount_status(total_spend))

            customer_tier = self._get_customer_tier(total_spend)
            if customer_tier:
                print(customer_tier)

    def _calculate_total_spend(self, purchases):
        total_spend = 0
        for purchase in purchases:
            total_spend += self._get_purchase_total(purchase)
        return total_spend

    def _get_purchase_total(self, purchase):
        price = purchase['price']
        if price > self.tax_threshold:
            return price * (1 + self.tax_rate)
        return price

    def _get_discount_status(self, total_spend):
        if total_spend > self.discount_threshold:
            return "Eligible for discount"
        if total_spend > 300:
            return "Potential future discount customer"
        return "No discount"

    def _get_customer_tier(self, total_spend):
        if total_spend > 1000:
            return "VIP Customer!"
        if total_spend > 800:
            return "Priority Customer"
        return None

    def calculate_shipping_fee(self, purchases):
        return calculate_shipping_fee_for_heavy_items(purchases)


def has_purchase_matching(purchases, field, threshold=None, expected_value=True):
    for purchase in purchases:
        value = purchase.get(field, 0 if threshold is not None else False)
        if threshold is not None and value > threshold:
            return True
        if threshold is None and value == expected_value:
            return True
    return False

def calculate_shipping_fee_for_heavy_items(purchases):
    if has_purchase_matching(purchases, 'weight', threshold=20):
        return 50
    return 20


def calculate_shipping_fee_for_fragile_items(purchases):
    if has_purchase_matching(purchases, 'fragile'):
        return 60
    return 25

flat_tax = 0.2
