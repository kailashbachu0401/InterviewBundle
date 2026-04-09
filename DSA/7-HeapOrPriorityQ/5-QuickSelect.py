'''
🧠 What problem does it solve?
- Find the k-th smallest / largest element efficiently
problem: https://leetcode.com/problems/kth-largest-element-in-an-array/description/
'''

nums = [3,2,1,5,6,4], k = 2
# → 2nd largest = 5

def partition(nums, left, right):
    pivot = nums[right]
    i = left # points first highest element from left of the array

    for j in range(left, right):
        if nums[j] <= pivot:
            nums[i], nums[j] = nums[j], nums[i]
            i += 1

    nums[i], nums[right] = nums[right], nums[i] # swap the pivot to the correct position
    return i # return the index of the pivot


def quickSelect(nums, left, right, k):
    if left == right:
        return nums[left]

    pivot_index = partition(nums, left, right)

    if pivot_index == k:
        return nums[pivot_index]
    elif pivot_index > k:
        return quickSelect(nums, left, pivot_index - 1, k)
    else:
        return quickSelect(nums, pivot_index + 1, right, k)


def kthLargest(nums, k):
    n = len(nums)
    return quickSelect(nums, 0, n - 1, n-k)

'''
Assume the array is sorted in ascending order
kth largest is the (n-k)th element in the sorted array

In QuickSelect, you pick a pivot
put all smaller elements than pivot to the left.
now if pivot index == (n-k), you found answer(kth largest)
if pivot index > (n-k), you know answer is in the left half, so you perform quickSelect on the left half
if pivot index < (n-k), you know answer is in the right half, so you perform quickSelect on the right half

If you want kth smallest, just start with quickSelect(nums, 0, n - 1, k-1)
cuz k - 1 will be the index of the kth smallest element in the sorted array

Worst case:
Input array is [1, 2, 3, 4, 5], k = 5th largest
5th largest element is 1 -> 0th(n-k) element the sorted array.
As we choose right element as pivot all the time, it takes O(n) for pivot to reach 0, from 5th index.
For every pivot is chosen, j iterates through left to right.

Best case:
Input array is [5,4,3,2,1], k = 5th largest
4th index is the pivot and is swapped with 0th index in the first iteration itself.

Time complexity:
Worst = O(n^2) # bad pivot
Average = O(n) # good pivot
Choice of pivot is important in QuickSelect.

| Situation              | Use         |
| ---------------------- | ----------- |
| Need k-th element once | Quickselect |
| Need top-k repeatedly  | Heap        |
| Streaming data         | Heap        |
| In-place required      | Quickselect |
'''