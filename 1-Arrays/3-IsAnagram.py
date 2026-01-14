'''
string s and t are anagrams if they have the same frequency of each character
problem: https://leetcode.com/problems/valid-anagram/description/
'''

from typing import Counter


def isAnagram(s, t):
    if len(s) != len(t):
        return False

    need = {}
    # count the frequency of each character in s
    for ch in s:
        need[ch] = need.get(ch, 0) + 1

    # all frequencies should be 0 at the end, if they are not, then s and t are not anagrams
    for ch in t:
        if ch not in need:
            return False
        need[ch] -= 1
        if need[ch] < 0:
            return False
    return True


print(isAnagram("anagram", "nagaram"))

# Alternative solution)(much faster):
def isAnagram(s, t):
    return Counter(s) == Counter(t)

print(isAnagram("anagram", "nagaram"))