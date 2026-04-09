'''
problem: https://leetcode.com/problems/subarrays-with-median-k/description/
Given an array, find the number of subarrays with median k.
Median is the middle value in the sorted array.
'''

from collections import defaultdict


def subarraysWithMedianK(nums, k):
    pos = nums.index(k)

    balance = 0
    balance_count = defaultdict(int)
    balance_count[0] = 1

    ans = 0

    # calculate balances for subarrays to the right of k
    for i in range(pos + 1, len(nums)):
        if nums[i] > k:
            balance += 1
        else:
            balance -= 1
        balance_count[balance] += 1

    balance = 0

    # calculate balances for subarrays to the left of k
    for i in range(pos, -1, -1):
        if nums[i] > k:
            balance += 1
        elif nums[i] < k:
            balance -= 1

        ans += balance_count[-balance] + balance_count[1-balance]
    return ans


'''
Key observation

For median to be k:
- subarray must contain k
- elements greater than k and less than k must be balanced in a certain way

Transform the array

Relative to k:

if num > k → +1
if num < k → -1
if num == k → special pivot

Now think only about the balance: balance = (#greater_than_k) - (#less_than_k)

When is median k?
- For a subarray containing k, median is k when balance is: 0 or 1

Why?
- odd length: counts on both sides equal → balance 0
- even-style centered handling in this problem's definition leads to balance 1 also being valid

So we want:
- subarrays containing k whose transformed balance is 0 or 1

Strategy
- Find index of k
- Go right from k, compute balances and count frequencies
- Go left from k, compute balances and look for complements

This is a prefix-balance matching trick.
'''

