'''
problem: https://leetcode.com/problems/path-sum-ii/description/
You are given the root of a binary tree and an integer targetSum.
Return all root-to-leaf paths where the sum of the node values in the path equals targetSum.
Each path should be returned as a list of the node values, not node references.

Template 2 + 3: carry running sum from parent to children + DFS with backtracking
you need backtracking here as you need all those paths with targetSum.

Earlier in HasPathSum, you only needed to know if there was a path with targetSum, not all paths.
Hence only DFS(template 2), no backtracking.
'''

def pathSum(root, targetSum):
    result = []
    path = []
    def dfs(node, curr_sum):
        if not node:
            return

        # Visit node
        path.append(node.val)
        curr_sum += node.val

        # leaf?
        if not node.left and not node.right and curr_sum == targetSum:
            result.append(path.copy())
        else:
            dfs(node.left, curr_sum)
            dfs(node.right, curr_sum)

        path.pop()

    dfs(root, 0)
    return result