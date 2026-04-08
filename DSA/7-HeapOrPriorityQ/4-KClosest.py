'''
problem: https://leetcode.com/problems/k-closest-points-to-origin/description/
'''

import heapq

def kClosest(points, k):
    heap = []
    for x, y in points:
        distance = x*x + y*y
        heapq.heappush(heap, (-distance, x, y))

        if len(heap) > k:
            heapq.heappop(heap)

    return [[x, y] for _, x, y in heap]

'''
calculate distance from origin for each point
push it to heap as (-distance, x, y) - mimic max heap
if heap size is greater than k, pop the smallest distance point
return the points in the heap
'''
