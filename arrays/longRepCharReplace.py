'''
You are given a string s and an integer k.
You can replace at most k characters in s with any other character to
maximize the length of the substring returned.

Return the length of the longest substring containing the same letter you can get after replacing at most k characters.
problem: https://leetcode.com/problems/longest-repeating-character-replacement/description/
'''

from collections import defaultdict

def longRepCharReplace(s, k):
    max_freq = 0 # max frequency of any character in any window
    start = 0
    best_len = 0
    freq = defaultdict(int)

    for end, ch in enumerate(s):
        freq[ch]+=1
        max_freq = max(max_freq, freq[ch])
        while (end - start + 1) - max_freq > k: # no.of chars u wanna replace = wLength - max_freq
            freq[s[start]]-=1
            start+=1
        best_len = max(best_len, end - start + 1)
    return best_len

s = "AABABBA"
k = 1

print(longRepCharReplace(s, k))
'''
Core Insight:

To make a substring all one character:

Keep the most frequent character

Change all other characters

Minimum changes needed:

window_length − max_frequency


Window is valid if:

window_length − maxFreq ≤ k

What to Track:

freq[ch] → frequency of characters in current window

maxFreq → maximum frequency seen in the window scan

Two pointers: start, end

best → maximum valid window length

Sliding Window Strategy:

Expand window by moving end

Update freq and maxFreq

If (window_length − maxFreq) > k → shrink window from start

Update best after shrink loop

Important Optimization (Key Concept):

maxFreq is allowed to be stale (not decreased on shrinking)

It only ever increases

A stale maxFreq may delay shrinking, but:

it never causes an incorrect maximum length

because the maximum possible window length is bounded by:

maxFreq + k

Why Stale maxFreq Is Safe:

maxFreq was real at some point during the scan

Any window length L recorded satisfies:

L ≤ maxFreq + k


Therefore, best never exceeds what is actually achievable

Window may be temporarily invalid, but maximum length remains correct

Key Invariant:
best ≤ maxFreq + k

Important Distinction

Sliding window does not always maintain a strictly valid window

In maximization problems, relaxed validity is sometimes safe

In minimization or exact window problems, strict validity is required

Time & Space

Time: O(n)

Space: O(1) (fixed alphabet)

When to Use This Pattern

Longest substring

Constraint like “at most k changes”

Validity depends on dominant element

Can tolerate optimistic / relaxed checks
'''