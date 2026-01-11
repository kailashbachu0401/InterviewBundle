'''
how many subarrays have sum = k (prefix_sum -> count memory)
problem: https://leetcode.com/problems/subarray-sum-equals-k/description/

Array can have negative values

At index i, suppose:

sum_so_far = nums[0] + nums[1] + ... + nums[i]

Now imagine some subarray from j+1 to i has sum k.

That means:

(nums[j+1] + ... + nums[i]) = k

But:

(nums[0] + ... + nums[i]) - (nums[0] + ... + nums[j]) = k
sum_so_far - sum_before_j = k
sum_before_j = sum_so_far - k

Translation:

When you are at position i, to know how many valid subarrays end at i,

you need to know:
How many times in the past we had a prefix-sum value equal to sum_so_far - k (similar to two sum problem)

So the past information we store is:

prefix_sum_value → how many times it has occurred
'''

from collections import defaultdict

nums = [1, 2, 1, 2]
k = 3

def subArraySum(nums, k):
    result = 0
    prefix_sum_count = defaultdict(int)
    prefix_sum_count[0]=1 # sum 0 occurs once before we start
    sum_so_far = 0
    for num in nums:
        sum_so_far+=num
        result += prefix_sum_count[sum_so_far - k]
        prefix_sum_count[sum_so_far]+=1
    return result

print(subArraySum(nums, k))