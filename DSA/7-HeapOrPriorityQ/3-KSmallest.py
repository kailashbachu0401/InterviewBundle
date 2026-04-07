'''
Find Kth smallest element in an array
'''

import heapq

def findKthSmallest(nums, k):
    heap = []
    for num in nums:
        heapq.heappush(heap, -num)
        if len(heap) > k:
            heapq.heappop(heap)
    return -heap[0]

'''
Why this works

We maintain:
- k smallest elements
- Heap root: largest among them → kth smallest
'''