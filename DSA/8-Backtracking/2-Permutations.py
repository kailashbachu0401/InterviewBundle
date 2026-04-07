'''
problem: https://leetcode.com/problems/permutations/description/
Given an array nums of distinct integers, return all the possible permutations.
You can return the answer in any order.
'''

def permute(nums):
    result = []
    current = []
    n = len(nums)
    used = [False] * n

    def backtrack():
        if len(current) == n:
            result.append(current[:])

        for i in range(n):
            if used[i] == True:
                continue

            # choose
            current.append(nums[i])
            used[i] = True

            backtrack()

            # undo
            current.pop()
            used[i] = False

    backtrack()
    return result

'''
🧠 Why subsets and permutations are different

In subsets, Order does not matter: [1, 2], [2, 1] are the same subset.

So once you pick 1, you only explore elements after it: i + 1 That avoids duplicates.

In permutations, Order does matter:

[1, 2, 3], [2, 1, 3] are different permutations.

So after picking 1, your next choice is not just from the right side. You should be able to pick: 2 or 3
And if first pick was 2, next you should still be able to pick: 1 or 3

So:

We cannot use i + 1 because permutations are not about position in array, they are about which elements are still unused.

1. Why can't we use i + 1 here?

- Because i + 1 means: "only look to the right"
- That works for subsets/combinations, where order doesn't matter.
- But for permutations, after choosing one element, we want to choose any other unused element, even if it appears earlier in the array.

Example:

nums = [1, 2, 3]

If first choice is 2, next valid choices are: 1, 3
But i + 1 from 2 would only allow 3.
So it would miss: [2, 1, 3] ❌

2. How do we prevent reusing the same element?

We need to track: which elements are already used in the current permutation

So if current path is: [2, 1], then:
- 2 is used
- 1 is used
- only 3 can be chosen next

3. What extra data structure do we need?

We need a data structure to track both used and unused elements.
A used array (or set) is perfect for this.

Example:

used = [False, False, False]

If we pick nums[1] = 2: used[1] = True

When we backtrack: used[1] = False

- That is the undo step. ✅

--- Total number of permutations = n!
'''