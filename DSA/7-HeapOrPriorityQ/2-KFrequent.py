'''
problem: https://leetcode.com/problems/top-k-frequent-elements/description/
You are given an array of integers nums and an integer k.
You need to find the k most frequent elements in the array.

Heap or Priority Queue
'''

from collections import Counter
import heapq

def topKFrequent(nums, k):
    freq = Counter(nums)

    heap = []

    for num, count in freq.items():
        heapq.heappush(heap, (count, num))

        if len(heap) > k:
            heapq.heappop(heap)

    return [num for _, num in heap]

'''
Python heap compares tuple elements from left to right

(1, 100) < (2, 1)   # True
- Why? First compare first element → 1 < 2 → stop

(2, 3) < (2, 5)   # True
- Why? First compare first element → 2 = 2 → compare second → 3 < 5

So when we do:
heapq.heappush(heap, (count, num))

Heap orders by:
- count (primary)
- num (tie-breaker)

Why this works perfectly

We want:
- smallest frequency at top

So:
- count comes first → controls ordering
- num doesn't matter much → just breaks ties

What if we reversed it?
(num, count)

Now heap would:
- prioritize smallest num
- completely wrong behavior


Top K Frequent Elements — Pattern Lock

- Count frequencies → ✅
- Heap stores (freq, element) → ✅
- Heap size = k → ✅
'''