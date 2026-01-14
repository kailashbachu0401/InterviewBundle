'''
problem: https://leetcode.com/problems/unique-paths/description/
There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.
Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.
The test cases are generated so that the answer will be less than or equal to 2 * 109.
'''

def uniquePaths(m, n):
    dp = [[0] * n for _ in range(m)]

    # there is only 1 way for the whole 1st row and columns
    for i in range(n):
        dp[0][i] = 1
    for i in range(m):
        dp[i][0] = 1

    # ways(i) = ways(i-1, j) + ways(i, j-1)
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r-1][c] + dp[r][c-1]

    return dp[m-1][n-1]

# space saving
def uniquePaths(m, n):
    dp = [1] * n
    for i in range(1, m):
        for j in range(1, n):
            dp[j] += dp[j-1]
    return dp[n-1]