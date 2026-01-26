'''
problem: https://leetcode.com/problems/shortest-path-in-binary-matrix/description/
You are given an n x n binary matrix grid. You are initially positioned at the top-left cell (0, 0).
Return the shortest path length to reach the bottom-right cell (n - 1, n - 1) if it is possible. If it is not possible, return -1.
'''

from collections import deque

def shortestPathBinaryMatrix(grid):
    n = len(grid)
    if grid[0][0] == 1 or grid[n-1][n-1] == 1:
        return -1

    directions = [
        (1,0), (-1,0), (0,1), (0,-1),
        (1,1), (1,-1), (-1,1), (-1,-1)
    ]

    q = deque([(0,0)])
    grid[0][0] = 1 # visited
    steps = 1

    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if r == n-1 and c == n-1:
                return steps

            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0:
                    grid[nr][nc] = 1
                    q.append((nr, nc))
        steps += 1

    return -1