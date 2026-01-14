'''
problem: https://leetcode.com/problems/number-of-islands/description/
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 4-directionally (horizontal or vertical).
Return the number of islands.
'''

def numIslands(grid):

    # no grid or empty grid
    if not grid or not grid[0]:
        return 0

    islands = 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        # check if the current position is out of bounds
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return

        # check if the current position is not land
        if grid[r][c] != "1":
            return

        grid[r][c] = "0" # visited (sink land)

        # explore if there are connected lands
        dfs(r+1, c)
        dfs(r-1, c)
        dfs(r, c+1)
        dfs(r, c-1)

    # iterate through the grid and find the islands
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1":
                # When you find the land, its an island so increment it
                # dfs will take care of sinking all the land connected to this island
                islands+=1
                dfs(r,c)

    return islands