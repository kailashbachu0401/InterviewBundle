# string s and t are anagrams if they have the same frequency of each character

from typing import Counter


def isAnagram(s, t):
    if len(s) != len(t):
        return False

    need = {}
    for ch in s:
        need[ch] = need.get(ch, 0) + 1

    for ch in t:
        if ch not in need:
            return False
        need[ch] -= 1
        if need[ch] < 0:
            return False
    return True


print(isAnagram("anagram", "nagaram"))

# Alternative solution:

def isAnagram(s, t):
    return Counter(s) == Counter(t)

print(isAnagram("anagram", "nagaram"))