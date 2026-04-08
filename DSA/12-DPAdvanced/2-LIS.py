'''
LIS - Longest Increasing Subsequence
problem: https://leetcode.com/problems/longest-increasing-subsequence/description/
Given an integer array nums, return the length of the longest strictly increasing subsequence.

DP Pattern 2: Build answer ending at each position
'''

nums = [10,9,2,5,3,7,101,18]

def lengthOfLIS(nums):
    n = len(nums)
    dp = [1] * n

    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)

    return max(dp)

'''
Define STATE:
- dp[i] = max length of LIS ending at index i

TRANSITION:
- For each i: Look at all j < i:
    - at i, many earlier j can connect to i, each with different LIS lengths, so we must check all j < i.
- If: nums[j] < nums[i]
- Then: dp[i] = max(dp[i], dp[j] + 1)

BASE CASE:
- dp[i] = 1 # every element itself

FINAL ANSWER:
- max(dp)
'''

'''
🧠 Mental model
- At each index: “What is the best subsequence I can end here?”

🔥 Important insight
- This is: not take/skip
- but: build from previous best answers

| Pattern    | Type        |
| ---------- | ----------- |
| Subset sum | Decision DP |
| LIS        | Build-up DP |

What is the smallest subproblem whose answer helps me build the final answer?

    For LIS, if I ask: “What is the LIS of the whole array?”
    - that is too big and vague.

    So we make it more local:
    - “If I force the subsequence to end at index i, what is the best I can do?”

    That becomes: dp[i] = length of LIS ending at i

    Why is this a good state?

    Because then when I stand at i, I can look backward and ask:
    - which earlier elements can connect to me?
    - among them, which gives the best length?

    That gives a clean transition.

Sequence problems often use dp[i] = best answer ending at i, but not always.

we can solve LIS with backtracking?

    You can do:
    - hold a current subsequence
    - go right only
    - if next element is larger than current last element, take it
    - keep max length

    That works.
'''