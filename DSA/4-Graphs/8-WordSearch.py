'''
problem: https://leetcode.com/problems/word-search/description/
'''

def exist(board, word):
    rows, cols = len(board), len(board[0])
    n = len(word)

    def dfs(r, c, w):
        if w == n:
            return True

        char = board[r][c]
        board[r][c] = '#' # visited

        # explore
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if board[nr][nc] == word[w] and dfs(nr, nc, w + 1):
                    board[r][c] = char # restore
                    return True # Return true only if the DFS succeeds; else explore other nei.

        # restore
        board[r][c] = char
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if dfs(r, c, 1):
                    return True
    return False

# cleaner

def exist(board, word):
    rows, cols = len(board), len(board[0])
    n = len(word)

    def dfs(r, c, w):
        if w == n:
            return True

        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[w]:
            return False

        # mark visted
        temp = board[r][c]
        board[r][c] = '#'

        # explore
        found = (
            dfs(r+1, c, w+1) or
            dfs(r-1, c, w+1) or
            dfs(r, c+1, w+1) or
            dfs(r, c-1, w+1)
        )

        # restore/undo
        board[r][c] = temp
        return found


    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False



