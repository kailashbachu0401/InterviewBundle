# Heaps / Priority Queue

This is important because:

- shows up frequently in interviews
- used in system design (schedulers, top-k, queues)
- connects to real systems

---

## Step 1 — What problem Heap solves

Imagine:

> 👉 You want the largest element quickly

Without heap:

- sort → O(n log n)
- scan → O(n)

With heap:

- get max/min → O(1)
- insert/remove → O(log n)

What is a Heap?

> A heap is a data structure that always gives you the smallest (or largest) element efficiently.

Two types:

- Min Heap → smallest on top
- Max Heap → largest on top

---

## 🧠 In Python

Python gives you:
```
import heapq
```

**⚠️ Important**:

> Python only has min heap

Basic operations
```
import heapq

nums = [5, 3, 8]

heapq.heapify(nums)   # O(n)

heapq.heappush(nums, 2)
heapq.heappop(nums)   # returns smallest
```

---

## General Pattern (remember this)

Whenever you see:

- Top K largest
- Kth largest
- K most frequent
- K closest points

👉 Think:

> Min heap of size K

---

## MaxHeap

**Trick: invert values**

For max heap:
```
heapq.heappush(heap, -num)
```

Example
```
nums = [3, 1, 5]

heap = []
for num in nums:
    heapq.heappush(heap, -num)

# heap = [-5, -1, -3]
```
Now:

``largest = -heapq.heappop(heap)``

---

## 🔒 Final mental shortcut

Keep K best elements → use opposite heap

- Want largest → use min heap
- Want smallest → use max heap

---

## 🧠 Big Insight (VERY IMPORTANT)

Heap is not about:
- sorting everything

It’s about:
- maintaining a small window of best candidates

---
