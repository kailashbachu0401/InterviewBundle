'''
problem: https://leetcode.com/problems/linked-list-cycle-ii/description/
'''

def detectCycle(head):
    slow = head
    fast = head

    # detect cycle
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

        if slow == fast:
            break

    # No cycle
    if not fast or not fast.next:
        return None

    # cycle
    slow = head
    while slow != fast:
        slow = slow.next
        fast = fast.next

    return slow

'''
Once you detect the cycle, reset slow to head and move slow and fast one step at a time until they meet
the node where they meet is the start of the cycle

How to find cycle length?
Once you detect the cycle, keep fast at the meeting point and move slow one step at a time until they meet again
the number of steps they take is the cycle length
'''