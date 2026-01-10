'''
Problem: https://leetcode.com/problems/two-sum/description/

Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
'''

nums = [2,7,11,15]
target = 9
seen = {} # value -> index

def twoSum(nums, target):
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i


print(twoSum(nums, target))