'''
problem: https://leetcode.com/problems/climbing-stairs/description/
You are climbing a staircase. It takes n steps to reach the top.
Each time you can either climb 1 or 2 steps. In how many distinct ways can you climb to the top?
'''

def climbStairs(n):
    if n == 1:
        return 1
    if n == 2:
        return 2
    return climbStairs(n-1) + climbStairs(n-2)

def climbStairs(self, n: int) -> int:
    if n <= 1:
        return 1

    dp = [0]*(n+1)
    dp[0] = 1
    dp[1] = 1

    # At a given step i -> you'd have come with 1 step from i-1 or 2-step from i-2
    # ways(i) = ways(i-1) + ways(i-2)
    # Bottom - Up DP
    for i in range(2, n+1):
        dp[i] = dp[i-1] + dp[i-2]
    return dp[n]

def climbStairs(self, n: int) -> int:
    if n <= 1:
        return 1
    prev, curr = 1, 1
    for i in range(2, n+1):
        prev, curr = curr, prev + curr
    return curr