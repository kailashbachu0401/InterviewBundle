'''
problem: https://leetcode.com/problems/search-in-rotated-sorted-array/description/
You are given an integer array nums sorted in ascending order (with distinct values), and an integer target.

Suppose that nums is rotated at some pivot unknown to you beforehand (i.e., [0,1,2,4,5,6,7] might become [4,5,6,7,0,1,2]).

You should search for target in nums and if you find it, return its index. If not, return -1.

Binary Search Pattern 2 - Identify which half is sorted
'''

def search(nums, target):
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right)//2

        if nums[mid] == target:
            return mid

        if nums[left] <= nums[mid]: # left half is sorted
            if nums[left] <= target < nums[mid]: # target is in the left half
                right = mid - 1
            else:
                left = mid + 1 # target is in the right half
        else: # right half is sorted
            if nums[mid] < target <= nums[right]: # target is in right half
                left = mid + 1
            else: # target is in left half
                right = mid - 1
    return -1