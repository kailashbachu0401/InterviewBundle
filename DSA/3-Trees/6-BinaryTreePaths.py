'''
problem: https://leetcode.com/problems/binary-tree-paths/description/
You are given the root of a binary tree.
Return all root-to-leaf paths in any order.

Template 3: choices + undo (DFS with backtracking)
'''

def binaryTreePaths(root):
    result = []
    path = []
    def dfs(node):
        if not node:
            return

        # visit this node
        path.append(str(node.val))

        # check if leaf
        if not node.left and not node.right:
            result.append("->".join(path))
        else:
            dfs(node.left)
            dfs(node.right)

        # backtrack/unvisit
        path.pop()

    dfs(root)
    return result