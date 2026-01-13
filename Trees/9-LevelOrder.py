'''
problem: https://leetcode.com/problems/binary-tree-level-order-traversal/description/
You are given the root of a binary tree.
Return the level order traversal of the tree.
'''

from collections import deque


def levelOrder(root):
    if not root:
        return []

    result = []
    q = deque([root])

    #BFS - The current queue size = number of nodes in the current level
    while q:
        level = []
        for _ in range(len(q)):
            node = q.popleft()
            level.append(node.val)

            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        result.append(level)
    return result