'''
Fractional Knapsack — From First Principles
Problem
- You have:
    - items with value
    - items with weight
    - bag capacity W
- But unlike 0/1 knapsack:
    - You are allowed to take fractions of an item

Example:
- Items: (value, weight) = (60, 10), (100, 20), (120, 30)
- Capacity: 50
- Answer: 240 (100 + 120)

Approach:
- Sort items by value/weight ratio
'''

def fractionalKnapsack(weights, values, capacity):
    items = []
    for i in range(len(weights)):
        items.append((values[i] / weights[i], values[i], weights[i]))

    items.sort(reverse=True)

    total_value = 0

    for _, value, weight in items:
        if capacity == 0:
            break
        if capacity >= weight:
            # take full item
            total_value += value
            capacity -= weight
        else:
            # take fraction of item
            fraction = capacity / weight
            total_value += fraction * value
            capacity = 0

    return total_value


'''
🔥 Key difference from normal knapsack
0/1 knapsack
- take whole item or skip
- DP needed
If you greedily take items with highest value, you will lose capacity.
Fractional knapsack
- can take partial item
- greedy works

Greedy Pattern:
- Choose locally optimal item first

🔒 Why greedy works here

Because: taking the highest value-per-weight first is always best when fractions are allowed
- You are never “wasting” space on a lower-density item before a higher-density one.
- That's why greedy is correct here.
'''