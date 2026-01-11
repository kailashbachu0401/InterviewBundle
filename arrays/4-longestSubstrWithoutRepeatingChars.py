'''
Longest Substring Without Repeating Characters
problem: https://leetcode.com/problems/longest-substring-without-repeating-characters/description/

Input: s = "abcabcbb"
Output: 3
Explanation: The answer is "abc", with the length of 3.

Sliding window(always valid) + set(existence)
'''

s = "abcabcbb"

def longestSubstrWithoutRepeatingChars(s):
    seen = set() # existence
    max_length = 0
    start = 0
    for end, ch in enumerate(s):
        # Once window is valid, keep stretching it until the current character is not in the set
        # When current character is in the set, shrink the window untill it is valid again
        while ch in seen:
            seen.remove(s[start])
            start += 1
        seen.add(ch)
        max_length = max(max_length, end - start + 1)
    return max_length

print(longestSubstrWithoutRepeatingChars(s))

# Optimized -> Sliding window(always valid) + value -> index memory
def longestSubstrWithoutRepeatingChars(s):
    seen = {} # value -> index
    max_length = 0
    start = 0
    for end, ch in enumerate(s):
        # Instead of incrementing start by 1 as above, jump directly to last seen pos + 1 of seen character
        if ch in seen and seen[ch] >= start:
            start = seen[ch] + 1
        seen[ch] = end
        max_length = max(max_length, end - start + 1)
    return max_length

print(longestSubstrWithoutRepeatingChars(s))