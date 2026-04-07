'''
problem: https://leetcode.com/problems/reverse-linked-list/description/

🔒 Pattern: Pointer manipulation with 3 variables ✅
- prev
- curr
- next
'''

def reverseList(head):
    prev = None
    curr = head

    while curr:
        next_node = curr.next # save next
        curr.next = prev # Reverse
        prev = curr # Move prev
        curr = next_node # move curr

    return prev

'''
🔁 Reverse Linked List — From First Principles

Problem:
You have: 1 → 2 → 3 → 4 → None

Return:
4 → 3 → 2 → 1 → None

🧠 Step 1 — What is actually changing?

Each node has: node.next
We need to: reverse the direction of every next pointer

🧠 Step 2 — Think locally (key idea)

Focus on one node at a time.
At node 2: 1 → 2 → 3
We want: 1 ← 2   3
So: 2.next = 1

🧠 Step 3 — The problem

If we just do: current.next = prev
- We lose: access to the rest of the list (3 → 4 → ...)

🔥 So we need to remember the next node
- We store: next_node = current.next

🧠 Step 4 — Full process per node

For each node:
- Save next
- Reverse pointer
- Move forward

🔁 Visual walkthrough

Start:

prev = None
curr = 1 → 2 → 3 → 4

Iteration 1
Save next: next = 2
Reverse: 1 → None
Move:
- prev = 1
- curr = 2

Iteration 2

Save next: next = 3
Reverse: 2 → 1
Move:
- prev = 2
- curr = 3

Continue...

Final:

prev = 4 → 3 → 2 → 1
curr = None

👉 prev is the new head

🚀 Variations (important)

This pattern extends to:
- Reverse sublist
- Reverse in k-groups
- Detect cycle (different but same pointer control)
- Reorder list
'''