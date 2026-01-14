'''
problem: https://leetcode.com/problems/rotting-oranges/description/
You are given an m x n grid where each cell can have one of three values:

0 representing an empty cell,
1 representing a fresh orange, or
2 representing a rotten orange.
Every minute, any fresh orange that is 4-directionally adjacent to a rotten orange becomes rotten.

Return the minimum number of minutes that must elapse until no cell has a fresh orange. If this is impossible, return -1.
'''

from collections import deque

def orangesRotting(grid):
    if not grid or not grid[0]:
        return -1

    rows, cols = len(grid), len(grid[0])
    mins = 0
    q = deque()
    fresh = 0

    # First add all rotten oranges to q
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                q.append((r, c))
            if grid[r][c] == 1:
                fresh += 1

    directions = [(1,0), (-1,0), (0,1), (0,-1)]

    # BFS
    while q and fresh > 0:
        for _ in range(len(q)):
            r, c = q.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2 # rot it (visited)
                    fresh -= 1
                    q.append((nr, nc))
        mins += 1

    # if still fresh remaining, impossible
    return mins if fresh == 0 else -1

grid = [[2,1,1],[1,1,0],[0,1,1]]
print(orangesRotting(grid))