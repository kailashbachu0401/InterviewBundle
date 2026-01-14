'''
You are given a binary array nums.
You are allowed to flip at most k 0s to 1s.
Return the maximum number of consecutive 1s in the array.
problem: https://leetcode.com/problems/max-consecutive-ones-iii/description/
'''

nums = [1,1,1,0,0,0,1,1,1,1,0]
k = 2

def longestOnes(nums, k):
    freq_0 = 0
    start = 0
    best = 0
    for end, num in enumerate(nums):
        if num == 0:
            freq_0+=1
        while freq_0 > k:
            if nums[start]==0:
                freq_0-=1
            start+=1
        best = max(best, end - start +1)
    return best

print(longestOnes(nums, k))