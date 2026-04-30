catalog = {
    "basic": {"base_price": 100, "included_units": 10, "overage_price": 15}
}

subscription_records = [
    {"customer": "A", "plan": "basic"}
]

usage_records = [
    {"customer": "X", "units": 5},
    {"customer": "A", "units": 12}
]

def is_valid_usage(usage, subscriptions):
    customer = usage.get("customer")
    units = usage.get("units")

    if not isinstance(customer, str) or not customer:
        return False, "invalid_usage"

    if not isinstance(units, int) or units < 0:
        return False, "invalid_usage"

    if customer not in subscriptions:
        return False, "unknown_customer"

    return True, None

def is_valid_subscription(subscription_record, subscriptions, catalog):
    customer = subscription_record.get("customer")
    plan = subscription_record.get("plan")

    if not isinstance(customer, str) or not customer:
        return False, "invalid_subscription"

    if not isinstance(plan, str) or not plan:
        return False, "invalid_subscription"

    if plan not in catalog:
        return False, "unknown_plan"

    if customer in subscriptions:
        return False, "duplicate_subscription"

    return True, None

def parse_subscriptions(subscription_records, catalog, anomalies):
    subscriptions = {}
    for subscription_record in subscription_records:
        valid, reason = is_valid_subscription(subscription_record, subscriptions, catalog)
        if not valid:
            anomalies.append({"record": subscription_record, "reason": reason})
            continue
        customer = subscription_record["customer"]
        plan = subscription_record["plan"]
        subscriptions[customer] = plan
    return subscriptions

def parse_usages(usage_records, subscriptions, anomalies):
    usages = {customer: 0 for customer in subscriptions}
    for usage_record in usage_records:
        valid, reason = is_valid_usage(usage_record, subscriptions)
        if not valid:
            anomalies.append({"record": usage_record, "reason": reason})
            continue
        customer = usage_record["customer"]
        units = usage_record["units"]
        usages[customer] += units
    return dict(usages)

def compute_invoices(catalog, subscriptions, usages):
    invoices = {}
    for customer, total_usage in usages.items():
        plan = subscriptions[customer]
        pricing = catalog[plan]
        base_price = pricing["base_price"]
        included_units = pricing["included_units"]
        overage_price = pricing["overage_price"]
        invoice = base_price + max(0, total_usage - included_units) * overage_price
        invoices[customer] = invoice
    return invoices

def build_invoices(catalog, subscription_records, usage_records):
    anomalies = []
    subscriptions = parse_subscriptions(subscription_records, catalog, anomalies)
    usages = parse_usages(usage_records, subscriptions, anomalies)
    invoices = compute_invoices(catalog, subscriptions, usages)

    return {
        "invoices": invoices,
        "anomalies": anomalies,
    }

print(build_invoices(catalog, subscription_records, usage_records))

