'''
problem: https://leetcode.com/problems/01-matrix/description/
Given a matrix of 0s and 1s, return the distance to the nearest 0 for each cell.
'''
from collections import deque

def updateMatrix(mat):
    rows, cols = len(mat), len(mat[0])
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 0:
                queue.append((r,c))
            else:
                mat[r][c] = float('inf')

    directions = [[1, 0], [-1, 0], [0, 1], [0, -1]]

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            if 0 <= nr < rows and 0 <= nc < cols:
                if mat[nr][nc] > mat[r][c] + 1:
                    # shorter distance found
                    mat[nr][nc] = mat[r][c] + 1
                    queue.append((nr, nc))

    return mat

'''
enqueue all 0s first
with BFS, as you step into every neibhour add 1 to it, which is distance from its parent cell

distance from 1 to 0 and 0 to 1 is same, it is symetric.
So forget about 1s, just calculate the distance from 0s to all other cells.

One cell can be reached from multiple 0s, so as you do BFS, override the new cell only if you find a shorter distance.
“BFS explores nodes in increasing order of distance. Since we process all nodes at distance d before d+1, the first time we reach a node must be via the shortest path.”
'''