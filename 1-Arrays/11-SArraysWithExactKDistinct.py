'''
You are given an array of integers nums and an integer k.
Return the number of contiguous subarrays where the number of distinct elements is exactly k.
problem: https://leetcode.com/problems/subarrays-with-k-different-integers/description/
'''

from collections import defaultdict

nums = [1,2,1,2,3]
k = 2

def atmost(nums, k):
    if k <= 0:
        return 0
    distinct = 0
    freq = defaultdict(int)
    start = 0
    ans = 0
    for end, num in enumerate(nums):
        if freq[num] == 0:
            distinct+=1
        freq[num]+=1

        while distinct > k:
            left = nums[start]
            freq[left]-=1
            if freq[left]==0:
                distinct-=1
            start+=1

        ans += end-start+1
    return ans

def subarraysWithKDistinct(nums, k):
    # exactly k = atmost(k) - atmost(k-1)
    return atmost(nums, k) - atmost(nums, k-1)

print(subarraysWithKDistinct(nums, k))