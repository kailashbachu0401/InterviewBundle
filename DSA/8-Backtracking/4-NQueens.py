'''
Problem: https://leetcode.com/problems/n-queens/description/
'''

def solveNQueens(n):
    board = [["."] * n for _ in range(n)]
    result = []
    cols = set()
    diag1 = set() # r-c
    diag2 = set() # r+c

    def backtrack(r):
        if r == n:
            result.append(["".join(row) for row in board])
            return

        for c in range(n):
            if c in cols or (r-c) in diag1 or (r+c) in diag2:
                continue

            # place queen
            board[r][c] = "Q"
            cols.add(c)
            diag1.add(r-c)
            diag2.add(r+c)

            # explore
            backtrack(r+1)

            # undo
            board[r][c] = "."
            cols.remove(c)
            diag1.remove(r-c)
            diag2.remove(r+c)

    backtrack(0)
    return result


'''
For a cell (r, c):

Main diagonal
- Cells on same main diagonal have same: r - c
Anti-diagonal
- Cells on same anti-diagonal have same: r + c

So we track 3 sets:
- cols
- diag1 = r - c
- diag2 = r + c

If any is occupied, queen cannot be placed there.

PATTERN:

At row r:
- try every column c
- if safe:
    - place queen
    - mark sets
    - recurse to r + 1
    - undo
'''

