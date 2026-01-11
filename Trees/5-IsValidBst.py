'''
problem: https://leetcode.com/problems/validate-binary-search-tree/description/
You are given the root of a binary tree.
Return true if the tree is a valid binary search tree, false otherwise.

Template 2: pass range from parent to children (DFS without backtracking)

Ask each child to check if they are in the range.

Parent checks if the current node is in the range.

Every child follows the same logic.
'''

def isValidBST(root):
    def dfs(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return dfs(node.left, low, node.val) and dfs(node.right, node.val, high)
    return dfs(root, float('-inf'), float('inf'))