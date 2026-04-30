balances = {
    "AU": 80,
    "US": 140,
    "MX": 110,
    "SG": 120,
    "FR": 70,
}

def plan_transfers(balances, min_balance):
    deficits = []
    surpluses = []

    total_deficits = 0
    total_surpluses = 0

    for account, balance in balances.items():
        if balance < min_balance:
            need = min_balance - balance
            deficits.append([account, need])
            total_deficits += need
        elif balance > min_balance:
            extra = balance - min_balance
            surpluses.append([account, extra])
            total_surpluses += extra

    # below two ifs are two diff behaviors
    # total_deficits == 0 - means nothing needs to be done
    # total_surpluses < total_deficits - nothing can be done
    # do not combine two behaviors under one if or one def, keep them separate
    if total_deficits == 0:
        return []
    if total_surpluses < total_deficits:
        return None

    deficit_idx = 0
    surplus_idx = 0
    planned_transfers = []

    while deficit_idx < len(deficits) and surplus_idx < len(surpluses):
        to_account, needed = deficits[deficit_idx]
        from_account, available = surpluses[surplus_idx]

        amount = min(needed, available)
        planned_transfers.append(
            {
                "from": from_account,
                "to": to_account,
                "amount": amount,
            }
        )

        deficits[deficit_idx][1] -= amount
        surpluses[surplus_idx][1] -= amount

        if deficits[deficit_idx][1] == 0:
            deficit_idx += 1
        if surpluses[surplus_idx][1] == 0:
            surplus_idx += 1

    return planned_transfers

    '''
    if you want minimum number of moves, then sort deficits and surpluses in DESC
    When total surplus is less than total deficit, and u wann fill max accounts and not min moves
    then sort deficits in ASC and surpluses in DESC
    '''

def apply_transfers(planned_transfers, original_balances):
    updated_balances = original_balances.copy()

    for transfer in planned_transfers:
        from_account = transfer["from"]
        to_account = transfer["to"]
        amount = transfer["amount"]

        updated_balances[from_account] -= amount
        updated_balances[to_account] += amount

    return updated_balances

def verify_transfers(planned_transfers, original_balances, min_balance):
    updated_balances = apply_transfers(planned_transfers, original_balances)
    all_balances_valid = all(balance >= min_balance for balance in updated_balances.values())
    total_preserved = sum(original_balances.values()) == sum(updated_balances.values())

    return {
        "updated_balances": updated_balances,
        "all_balances_valid": all_balances_valid,
        "total_preserved": total_preserved,
    }

def execute_transfers(original_balances, planned_transfers, min_balance):
    verification_result = verify_transfers(planned_transfers, original_balances, min_balance)
    # Based on verification result
    # this will execute all transfers, meaning updates in DB
    # performs single bulk write query to update
    # if query fails, DB automatically reverts its state
    return {
        "executed_transfers": planned_transfers,
        "original_balances": original_balances,
        "success": 0 or 1
    }

def validate_transfers(executed_transfers, orginal_balances):
    # checks against DB if all accounts have expected balances after executed transfers
    # return validation true or false
    pass

def move_balances(balances, min_balance):
    planned_transfers = plan_transfers(balances, min_balance)
    execution_result = execute_transfers(balances, planned_transfers, min_balance)
    validation_result = validate_transfers(execution_result["executed_transfers"], balances)

    # if validation fails:
    # stop any further dependent actions
    # mark the operation as failed / partial
    # alert and create a reconciliation task
    # retry only if operations are idempotent and safe
    # otherwise escalate for manual investigation depending on system design


'''
How would you check in reality that each balance is at least 100?

After executing the transfers, I would fetch the final balances again from the source of truth and verify:

every balance is at least 100
total money is preserved
every planned transfer was either executed successfully or marked failed

This is what our validate_transfers is doing
'''

'''
If this were moving millions of dollars in production, how would you change it?

I would separate:

planning transfers
executing transfers
verifying outcomes

I would also:

make each transfer idempotent with a unique transfer ID
log every planned and executed move
validate preconditions before execution
execute through a system of record that supports auditability and reconciliation
avoid relying only on in-memory balances if there are concurrent updates
'''



















