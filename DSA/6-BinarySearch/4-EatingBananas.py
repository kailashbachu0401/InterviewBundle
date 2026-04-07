'''
problem: https://leetcode.com/problems/koko-eating-bananas/description/
You are given an array of integers piles where piles[i] represents the number of bananas in the ith pile.
You are also given an integer h.
You need to find the minimum number of bananas that Koko should eat per hour so that she can eat all the bananas in h hours.

Binary Search Pattern 3
'''
import math

def minEatingSpeed(piles, h):
    left, right = 1, max(piles)
    ans = right

    def can_finish(k) -> bool:
        hours = 0
        for pile in piles:
            hours += math.ceil(pile / k)
        return hours <= h

    while left <= right:
        mid = (left + right) // 2
        if can_finish(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
    return ans

'''
Why binary search works

As k increases: time needed decreases → monotonic condition

So:

k small → too slow → ❌
k large → fast enough → ✅

So we get:

❌ ❌ ❌ ❌ ✅ ✅ ✅

👉 Monotonic condition

🔥 That's why binary search works

We are finding: first k where can_finish(k) = True
'''