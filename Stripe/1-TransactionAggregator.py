transactions = [
    {"user": "A", "amount": 100, "type": "credit"},
    {"user": "A", "amount": 50, "type": "debit"},
    {"user": "B", "amount": 200, "type": "credit"},
]

'''
Output:
{
    "balances": {...},
    "top_k": [...]
}
'''

'''
Approach:
balances is a default dict of int (key = user, value = balance)
Assuming alll transaction are already ordered by time
Iterate through transactions and update the balance for each user
- if credit, add to balance
- if debit, subtract from balance
Invaid cases:
- if amount amount negative, continue
- if balance goes negative while debit, continue (not enough balance to debit)
balances is ready

- take minheap of size k
- iterate through balances and push to heap (balance, user)
- size(heap) > k, pop the smallest balance
- left over heap size is top K users with top k balances

format the output and return
'''

from collections import defaultdict
import heapq

VALID_TRANSACTION_TYPES = {"credit", "debit"}

def validate_transaction(transaction):

    required_fields = {"user", "amount", "type"}
    if not required_fields.issubset(transaction):
        return False

    user = transaction["user"]
    amount = transaction["amount"]
    transaction_type = transaction["type"]

    if not isinstance(user, str) or not user: # user can't be ""
        return False

    if not isinstance(amount, (int, float)) or amount < 0:
        return False

    if transaction_type not in VALID_TRANSACTION_TYPES:
        return False
    return True

def apply_transaction(transaction, balances):
    user = transaction["user"]
    amount = transaction["amount"]
    transaction_type = transaction["type"]
    if transaction_type == "credit":
        balances[user] += amount
    elif transaction_type == "debit":
        balances[user] -= amount

def aggregate_balances(transactions):
    balances = defaultdict(int)
    for transaction in transactions:
        if not validate_transaction(transaction):
            continue
        apply_transaction(transaction, balances)

    return dict(balances)

def get_top_k_users(balances, k):
    if k <= 0:
        return []
    min_heap = []
    for user, balance in balances.items():
        heapq.heappush(min_heap, (balance, user))
        if len(min_heap) > k:
            heapq.heappop(min_heap)

    top_users = []
    while min_heap:
        balance, user = heapq.heappop(min_heap) # “In case of equal balances, ordering is broken by user name due to tuple comparison.”
        top_users.append({"user": user, "balance": balance})

    top_users.reverse()
    return top_users

def summarize_transactions(transactions, k):
    balances = aggregate_balances(transactions)
    top_k_users = get_top_k_users(balances, k)
    return {
        "balances": balances,
        "top_k": top_k_users
    }


transactions = [
    {"user": "A", "amount": 100, "type": "credit"},
    {"user": "A", "amount": 50, "type": "debit"},
    {"user": "B", "amount": 200, "type": "credit"},
]

print(summarize_transactions(transactions, 2))