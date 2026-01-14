'''
problem: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/description/
You are given the root of a binary tree and two nodes p and q.
Return the lowest common ancestor of the two nodes.

Template 1: Compute from children (DFS without backtracking)
'''

def lowestCommonAncestor(root, p, q):
    # return early as root is p/q as it becomes a candidate ancestor, and parent will decide if it's LCA
    # if the other subtree returns empty then above found p/q is LCA
    # else parent is LCA
    if not root or root == p or root == q:
        return root

    # parent asks children, if p, q are part fo your subtrees.
    # children either responds with none, or whatever the target they have(p or q)
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    # If both branches return a value, then p, q are in diff branches and root is LCA
    if left and right:
        return root
    return left if left else right