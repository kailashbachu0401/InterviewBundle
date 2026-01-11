'''
You are given an array of integers nums and an integer k.
Return the number of contiguous subarrays where the number of odd elements is exactly k.
problem: https://leetcode.com/problems/count-number-of-nice-subarrays/description/
'''

nums = [1,1,2,1,1]
k = 3

def atmost(nums, k):
    odds = 0
    start = 0
    ans = 0
    for end, num in enumerate(nums):
        if num % 2 ==1:
            odds+=1
        while odds > k:
            if nums[start] % 2 == 1:
                odds-=1
            start+=1
        ans += end-start+1
    return ans

def numberOfSubarrays(nums, k):
    # exactly k = atmost(k) - atmost(k-1)
    return atmost(nums, k) - atmost(nums, k-1)

print(numberOfSubarrays(nums, k))