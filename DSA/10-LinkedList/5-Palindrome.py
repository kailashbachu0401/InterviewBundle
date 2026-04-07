'''
problem: https://leetcode.com/problems/palindrome-linked-list/description/
'''

def isPalindrome(head):
    # find middle
    slow, fast = head, head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # reverse 2nd half
    prev = None
    curr = slow
    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    # compare both halves
    first, second = head, prev
    while second:
        if first.val != second.val:
            return False
        first = first.next
        second = second.next
    return True

'''
How to delete a given node in LL?
- you are given the node to delete, not the head of the list
- node.val = node.next.val
- node.next = node.next.next
'''