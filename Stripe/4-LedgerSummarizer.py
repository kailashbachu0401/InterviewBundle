from collections import defaultdict

entries = [
    "ACCOUNT,A,USD",
    "ACCOUNT,B,USD",
    "ACCOUNT,A,USD",              # duplicate account
    "ACCOUNT,C",                  # invalid format

    "POST,1,A,credit,100",
    "POST,2,A,debit,30",
    "POST,3,B,credit,50",
    "POST,4,B,debit,10",

    "POST,5,Z,credit,20",         # unknown account
    "POST,x,A,credit,10",         # invalid timestamp
    "POST,6,A,unknown,10",        # invalid type
    "POST,7,A,credit,-5",         # invalid amount
    "POST,8,A,credit",            # invalid format

    "POST,9,C,credit,40",         # C was never valid account
]

VALID_POST_TYPES = {"credit", "debit"}


def is_valid_account(record, accounts):
    if len(record) != 3:
        return False, "invalid_account_format"

    account_id, currency = record[1:]

    if account_id in accounts:
        return False, "duplicate_account"

    return True, None


def is_valid_post(record, accounts):
    if len(record) != 5:
        return False, "invalid_post_format"

    timestamp_str, account_id, post_type, amount_str = record[1:]

    try:
        int(timestamp_str)
    except ValueError:
        return False, "invalid_timestamp"

    if post_type not in VALID_POST_TYPES:
        return False, "invalid_transaction_type"

    try:
        amount = int(amount_str)
    except ValueError:
        return False, "invalid_amount"

    if amount < 0:
        return False, "invalid_amount"

    if account_id not in accounts:
        return False, "unknown_account"

    return True, None


def parse_entries(entries):
    anomalies = []
    accounts = {}
    posts = defaultdict(list)

    for entry in entries:
        record = entry.split(",")

        if record[0] == "ACCOUNT":
            valid, reason = is_valid_account(record, accounts)
            if not valid:
                anomalies.append({"record": entry, "reason": reason})
                continue

            account_id, currency = record[1:]
            accounts[account_id] = currency

        elif record[0] == "POST":
            valid, reason = is_valid_post(record, accounts)
            if not valid:
                anomalies.append({"record": entry, "reason": reason})
                continue

            _, account_id, post_type, amount_str = record[1:]
            posts[account_id].append((post_type, int(amount_str)))

        else:
            anomalies.append({"record": entry, "reason": "unknown_record_type"})

    return accounts, posts, anomalies


def apply_transaction(balances, account_id, transaction):
    post_type, amount = transaction

    if post_type == "credit":
        balances[account_id] += amount
    else:
        balances[account_id] -= amount


def compute_balances(accounts, posts):
    balances = {account_id: 0 for account_id in accounts}

    for account_id, transactions in posts.items():
        for transaction in transactions:
            apply_transaction(balances, account_id, transaction)

    return balances


def summarize_ledger(entries):
    accounts, posts, anomalies = parse_entries(entries)
    balances = compute_balances(accounts, posts)

    return {
        "balances": balances,
        "anomalies": anomalies,
    }

'''
to validate ints:
you can use string.isdigit() -> will return True if > 0 else false

'''

