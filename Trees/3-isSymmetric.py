'''
problem: https://leetcode.com/problems/symmetric-tree/description/
You are given the root of a binary tree.
Return true if the tree is symmetric around its center, false otherwise.

Template 1: compute from children (Paired DFS without backtracking)

Earlier problems (depth / same tree):
each child subtree could answer independently, and the parent combined results.

Symmetric tree:
the answer depends on a relationship between two subtrees, so you ask them as a pair:
“Are you two mirrors of each other?”
'''

def isMirror(a, b):
    # both not existing
    if not a and not b:
        return True

    # one exists and other not
    if not a or not b:
        return False

    # both exists
    return (
        a.val == b.val and
        isMirror(a.left, b.right) and
        isMirror(a.right, b.left)
    )

def isSymmetric(root):
    if not root:
        return True
    return isMirror(root.left, root.right)

'''
🧱 New Tree DFS block you just learned

There are two “modes” of DFS questions:

1) Single-subtree DFS

dfs(node) → returns something about that subtree
Examples: depth, same-tree, height, sum

2) Paired DFS

dfs(a, b) → returns something about the relationship between two subtrees
Examples: symmetric tree, isSameTree (also can be written as paired), subtree check, etc.
'''
