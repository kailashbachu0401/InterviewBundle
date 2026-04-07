'''
problem: https://leetcode.com/problems/subsets/description/
Given an integer array nums of unique elements, return all possible subsets (the power set).
The solution set must not contain duplicate subsets. Return the solution in any order.
'''

def subsets(nums):
    result = []
    current = []
    def backtrack(index):
        # store current subset
        result.append(current[:])

        for i in range(index, len(nums)):
            # choose
            current.append(nums[i])

            # explore
            backtrack(i+1)

            # undo
            current.pop()

    backtrack(0)
    return result

'''
1. Choice at each element - Take it OR skip it ✅
2. What do we store? - Current subset (list) ✅

🔥 Pattern you just learned
Backtracking = build solution incrementally, undo after exploring

we did backtrack(i+1) and not backtrack(i) so same element is not picked
if backtrack(i) was used, then u'd get [1,1], [2,2], ... ❌

- Index controls reuse vs no-reuse

--- Total number of subsets = 2^n

'''


