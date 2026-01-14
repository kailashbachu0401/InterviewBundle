'''
problem: https://leetcode.com/problems/max-area-of-island/description/
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical).
Return the maximum area of an island in grid. If there is no island, return 0.
'''

def maxAreaOfIsland(grid):
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    maxArea = 0

    def dfs(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return 0

        if grid[r][c] != 1:
            return 0

        grid[r][c] = 0 # visited

        return (
            1 +
            dfs(r+1, c) +
            dfs(r-1, c) +
            dfs(r, c+1) +
            dfs(r, c-1)
        )

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                maxArea = max(maxArea, dfs(r, c))

    return maxArea