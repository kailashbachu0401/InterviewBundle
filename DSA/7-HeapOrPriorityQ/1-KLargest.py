'''
problem: https://leetcode.com/problems/kth-largest-element-in-an-array/description/
You are given an array of integers nums and an integer k.
You need to find the kth largest element in the array.

Heap or Priority Queue
'''
import heapq

def findKthLargest(nums, k):
    heap = [] # min heap
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

'''
✅ Use a MIN heap of size k

Why min heap, not max heap?

Instead of: finding all largest elements

We do: Keep track of the TOP k largest elements only

Step-by-step (feel it)

We process numbers one by one:

Start:

- Heap = []
- Add 3
- Heap = [3]
- Add 2
- Heap = [2, 3]
- (heap size = k = 2)
- Add 1
- Heap = [1, 3, 2]

Now size > k → remove smallest:

- pop 1
- Heap = [2, 3]
- Add 5
- Heap = [2, 3, 5]

pop smallest:

- pop 2
- Heap = [3, 5]
- Add 6
- Heap = [3, 5, 6]

pop smallest:

- pop 3
- Heap = [5, 6]
- Add 4
- Heap = [4, 6, 5]

pop smallest:

- pop 4
- Heap = [5, 6]
- Final heap: [5, 6]

👉 smallest = 5 → answer

🔒 Key pattern

Maintain a min heap of size k
→ heap always stores top k largest elements
→ root = kth largest


🧠 Why this is optimal
Time: O(n log k)
Better than sorting: O(n log n)

🔥 Mental model (lock this)

Min heap of size k → tracks k largest elements
'''