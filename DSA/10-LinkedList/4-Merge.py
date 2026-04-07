'''
problem: https://leetcode.com/problems/merge-two-sorted-lists/description/
'''
class ListNode:
    pass

def mergeTwoLists(list1, list2):
    dummy = ListNode()
    tail = dummy

    while list1 and list2:
        if list1.val < list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next

        tail = tail.next

    tail.next = list1 if list1 else list2
    return dummy.next


'''
How to rotate LL by k times?
- if k is greater than length of LL, then k = k % length of LL
- calculate length of LL, by traversing the list
- traverse the list to the (length - k)th node (temp)
- new head = temp.next
- new tail = temp
- point original tail to original head
'''