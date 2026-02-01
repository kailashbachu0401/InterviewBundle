'''
problem: https://leetcode.com/problems/maximum-depth-of-binary-tree/description/
You are given the root of a binary tree.
Return the maximum depth of the tree.
'''

def maxDepth(root):
    if not root:
        return 0
    return 1 + max(maxDepth(root.left), maxDepth(root.right))

'''
Template 1: Compute from children (DFS without backtracking)

Ask each child to compute its maxDepth.

Parent combines the children's results to get the current node's maxDepth. (Adds 1 to the max of results.)

Every child follows the same logic.

This is post-order thinking: children compute first, parent combines their results, then returns the final value.
'''