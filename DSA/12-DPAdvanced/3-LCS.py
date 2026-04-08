'''
LCS - Longest Common Subsequence
problem: https://leetcode.com/problems/longest-common-subsequence/description/
'''

text1 = "abcde"
text2 = "ace"

def longestCommonSubsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i-1] == text2[j-1]:
                # match - take it
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                # no match - skip char from each
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]


'''
STATE:
- dp[i][j] = LCS length using first i chars of text1 and first j chars of text2

Example
text1 = "abc"
text2 = "ac"

TRANSITION:
If characters match: text1[i-1] == text2[j-1]
👉 take it:
dp[i][j] = 1 + dp[i-1][j-1]

If not match:
dp[i][j] = max(
    dp[i-1][j],   # skip from text1
    dp[i][j-1]    # skip from text2
)

Do a dry run to feel it better
'''