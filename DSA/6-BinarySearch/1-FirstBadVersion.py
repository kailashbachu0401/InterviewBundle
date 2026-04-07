'''
problem: https://leetcode.com/problems/first-bad-version/description/
You are given an array of versions and a function isBadVersion(version) which returns if the version is bad.
You need to find the first bad version.

Versions go like:
GOOD, GOOD, GOOD, BAD, BAD, BAD, BAD...
- Monotonic change in the answer space
- Binary Search Pattern 1
'''

def isBadVersion(version):
    pass

def firstBadVersion(n):
    left, right = 1, n
    ans = n # worst case → last version is first bad
    while left <= right:
        mid = (left + right)//2
        if isBadVersion(mid):
            right = mid - 1
            ans = mid
        else:
            left = mid + 1
    return ans