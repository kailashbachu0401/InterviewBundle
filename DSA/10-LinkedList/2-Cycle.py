'''
problem: https://leetcode.com/problems/linked-list-cycle/description/

🔒 Pattern 2: Slow/Fast pointer ✅
'''

def hasCycle(head):
    slow = head
    fast = head

    while fast and fast.next:
        slow = slow.next # 1 step
        fast = fast.next.next # 2 step

        if slow == fast:
            return True
    return False

'''
This pattern used in:
- cycle detection
- finding middle
- palindrome linked list
- reorder list

You can detect cycle in LL, using a set
Traverse LL, add nodes to set, if node is already in set, then there is a cycle
this uses O(n) space

This pattern uses O(1) space
- slow pointer moves 1 step at a time
- fast pointer moves 2 steps at a time
- if there is a cycle, slow and fast will meet at some point
- if there is no cycle, fast will reach the end of the list

How to find middle of LL?
- Move slow by 1 and fast by 2 steps at a time.
- when fast reaches the end of the list, slow will be at the middle

How to find Kth element from end of LL?
- Move fast by k steps ahead of slow.
- then move slow and fast one step at a time until fast reaches the end of the list.
- the node where slow is pointing is the Kth element from end of LL.
'''