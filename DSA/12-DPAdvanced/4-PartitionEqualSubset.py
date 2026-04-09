'''
problem: https://leetcode.com/problems/partition-equal-subset-sum/description/
'''

def canPartition(nums):
    total_sum = sum(nums)

    '''
    If Array is being split into two parts, then sum of both parts should be total sum
    we want both parts to have equal sum

    If total sum is odd, can't be split equally, hence false

    target = total_sum // 2
    if you are able to make one subset with target sum, then my answer is true
    cuz all the other elements go to another subset with exact same sum
    - Final asnwer true
    '''
    if total_sum % 2 != 0:
        return False

    target = total_sum // 2

    # Subset sum
    dp = [False] * (target + 1)
    dp[0] = True
    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]

    return dp[target]