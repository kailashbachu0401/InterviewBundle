'''
problem: https://leetcode.com/problems/search-insert-position/description/
You are given a sorted array of distinct integers and a target value.
You need to find the index of the target value in the array.
If the target is not found, return the index where it would be if it were inserted in order.

Binary Search Pattern 1
'''

def searchInsert(nums, target):
    left, right = 0, len(nums) - 1
    ans = len(nums) # worst case → insert at the end, else find left most valid index to insert
    while left <= right:
        mid = (left + right) // 2
        # gives leftmost valid position automatically
        if nums[mid] >= target: # works for both found and insert cases
            ans = mid
            right = mid - 1
        else:
            left = mid + 1

    return ans

'''
In binary search left eventually converges to first valid index/answer
Do a dry run to understand better

We're basically pushing:

right to the last < target
left to the first >= target

At the end of loop

Condition:

- left > right

And we get:

- right → last element < target
- left  → first element >= target

👉 That means:

left is exactly the answer

🔍 Then why did we use ans?

Because:

👉 ans is a safe pattern for all “first true” problems

It works even when:
- condition is complex
- boundaries are tricky

It makes logic explicit: “store best candidate”

🔒 Final mental model

Binary search for boundary →
left always ends at first valid position
'''