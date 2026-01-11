'''
You are given an array of positive integers nums and an integer k.
Return the number of contiguous subarrays where the product of all the elements in the subarray is strictly less than k.
problem: https://leetcode.com/problems/subarray-product-less-than-k/description/
'''

nums = [10, 5, 2, 6]
k = 100

def numSubarrayProductLessThanK(nums, k):
    if k <= 1:
        return 0
    product = 1
    start = 0
    ans = 0
    for end, num in enumerate(nums):
        product *= num
        while product >= k and start <= end:
            product //= nums[start]
            start+=1
        ans += end - start + 1 # number of subarrays ending at end
    return ans

print(numSubarrayProductLessThanK(nums, k))