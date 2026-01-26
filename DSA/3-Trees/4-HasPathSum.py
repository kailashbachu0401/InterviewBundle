'''
problem: https://leetcode.com/problems/path-sum/description/
You are given the root of a binary tree and an integer targetSum.
Return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.

Template 2: carry something from parent to children (DFS without backtracking)
'''

def hasPathSum(root, targetSum):
    if not root:
        return False

    # if leaf, check target sum
    if not root.left and not root.right:
        return root.val == targetSum

    remaining = targetSum - root.val
    return hasPathSum(root.left, remaining) or hasPathSum(root.right, remaining)