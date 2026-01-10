'''
You are given two strings:

s → a long string

t → a short string

Your task is to find the smallest continuous part of s (a substring) such that:

This substring contains all characters of t,
including atleast their required frequencies.

Order does not matter.
The substring just needs to contain them.

s = "ADOBECODEBANC"
t = "ABC"

Valid substrings (not all):
"ADOBEC" → contains A, B, C
"BANC" → contains A, B, C

Answer:
"BANC"
'''

from collections import defaultdict
from math import inf
from typing import Counter

s = "ADOBECODEBANC"
t = "ABC"

def minSubstr(s, t):
    need = Counter(t)
    have = defaultdict(int)

    start = 0

    required = len(need) # distinct chars of t
    formed = 0 # how many of those chars currently meet the required count
    #When formed == required, window is valid.

    best_len = float(inf)
    best = [-1, -1]

    for end, ch in enumerate(s):
        have[ch]+=1

        if(ch in need and have[ch] == need[ch]):
            formed+=1

        while formed == required: # valid substring -> shrink it
            if end - start + 1 < best_len:
                best_len = end - start + 1
                best = [start, end]

            left_ch = s[start]
            if(left_ch in need and have[left_ch] == need[left_ch]):
                formed-=1
            have[left_ch]-=1
            start+=1

    if(best_len==float(inf)):
        return ""
    l, r = best
    return s[l:r+1]

print(minSubstr(s, t))




