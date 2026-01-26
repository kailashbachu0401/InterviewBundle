'''
problem: https://leetcode.com/problems/house-robber/description/
You are a professional robber planning to rob houses along a street.
Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and it will automatically contact the police if two adjacent houses were broken into on the same night.
Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.
'''

def rob(nums):
    if not nums:
        return 0
    if len(nums) == 1:
        return nums[0]
    return max(rob(nums[:-1]), rob(nums[:-2]) + nums[-1])

def rob(nums):
    n = len(nums)
    if n == 1:
        return nums[0]

    dp = [0]*(n)

    dp[0] = nums[0]
    dp[1] = max(nums[0], nums[1])

    # At given i, u can choose to rob it or skip it
    for i in range(2, n):
        dp[i] = max(dp[i-1], dp[i-2] + nums[i])

    return dp[n-1]

def rob(nums):
    prev2 = 0  # dp[i-2]
    prev1 = 0  # dp[i-1]

    for n in nums:
        curr = max(prev1, n + prev2)
        prev2 = prev1
        prev1 = curr

    return prev1

'''
🔒 DP Rule to Remember (VERY IMPORTANT)

DP is always about “what choice do I make now, and what past state does that force me to use?”

Here:

Choosing house i forces you to use dp[i-2]

Skipping house i lets you keep dp[i-1]

This “choice → constraint → transition” pattern appears everywhere in DP.
'''