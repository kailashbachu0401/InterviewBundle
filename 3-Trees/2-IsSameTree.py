'''
problem: https://leetcode.com/problems/same-tree/description/
You are given the roots of two binary trees p and q.
Return true if they are the same tree, false otherwise.

Template 1: Compute from children (DFS without backtracking)

Ask each child to check if they are the same tree.

Parent checks if the current node is the same tree.

Every child follows the same logic.
'''

def isSameTree(p, q):
    if not p and not q:
        return True
    if not p or not q:
        return False
    return p.val == q.val and isSameTree(p.left, q.left) and isSameTree(p.right, q.right)