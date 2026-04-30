from collections import defaultdict

events = [
    {"event_id": "e1", "customer": "A", "type": "charge", "amount": 100, "status": "failed"},
    {"event_id": "e1", "customer": "A", "type": "charge", "amount": 100, "status": "success"},
    {"event_id": "e2", "customer": "A", "type": "refund", "amount": 30, "status": "success"},
    {"event_id": "e3", "customer": "B", "type": "refund", "amount": 20, "status": "success"},
]

VALID_EVENT_TYPES = {"charge", "refund"}
VALID_STATUS = {"success", "failed"}


def validate_event(event, seen_event_ids):
    required_fields = {"event_id", "customer", "type", "amount", "status"}
    if not required_fields.issubset(event):
        return False, "invalid_event"

    event_id = event["event_id"]
    customer = event["customer"]
    event_type = event["type"]
    amount = event["amount"]
    status = event["status"]

    if not isinstance(event_id, str) or not event_id:
        return False, "invalid_event"

    if not isinstance(customer, str) or not customer:
        return False, "invalid_event"

    if event_type not in VALID_EVENT_TYPES:
        return False, "invalid_event_type"

    if not isinstance(amount, int) or amount < 0:
        return False, "invalid_amount"

    if status not in VALID_STATUS:
        return False, "invalid_status"

    if (event_id, status) in seen_event_ids:
        return False, "duplicate_event"

    return True, None


def normalize_event(event):
    return {
        "event_id": event["event_id"],
        "customer": event["customer"],
        "type": event["type"],
        "amount": event["amount"],
        "status": event["status"],
    }


def collect_valid_events(events, anomalies):
    seen_event_ids = set()
    valid_events = []

    for event in events:
        valid, reason = validate_event(event, seen_event_ids)
        if not valid:
            anomalies.append({"record": event, "reason": reason})
            continue

        seen_event_ids.add((event["event_id"], event["status"]))
        valid_events.append(normalize_event(event))

    return valid_events


def apply_event(customer_totals, event):
    customer = event["customer"]
    event_type = event["type"]
    amount = event["amount"]

    if event_type == "charge":
        customer_totals[customer] += amount
    elif event_type == "refund":
        customer_totals[customer] = max(0, customer_totals[customer] - amount)

    return customer_totals


def build_totals(valid_events):
    customer_totals = defaultdict(int)

    for event in valid_events:
        if event["status"] != "success":
            continue

        apply_event(customer_totals, event)

    return dict(customer_totals)


def process_payment_events(events):
    anomalies = []
    valid_events = collect_valid_events(events, anomalies)
    totals = build_totals(valid_events)

    return {
        "totals": totals,
        "anomalies": anomalies,
    }

print(process_payment_events(events))