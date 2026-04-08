'''
DP Pattern 1 — Decision DP (Knapsack style, take or skip)
'''

nums = [1, 2, 3, 4]
target = 6

# True, cuz 2 + 4 = 6

'''
We can do this by backtracking; take it or skip it.

DP style:

Your target sum is 6. When you are at index 3, the question is: can we form the sum 6 using elements up to this index?

At index 3, you have two choices: take the element or skip it.

If you skip it:
- If it was already possible to form sum 6 using elements up to index 2, then it remains possible at index 3.
If you take it:
- Then you must have previously formed the sum 6 - nums[3] using elements up to index 2. If that was possible, then including nums[3] gives you sum 6.

So, define the STATE:
- dp[i][s] = whether it is possible to form sum s using elements up to index i.

TRANSITION:
If you skip the current element:
dp[i][s] = dp[i-1][s]
If you take the current element (only when nums[i] <= s):
dp[i][s] = dp[i-1][s] OR dp[i-1][s - nums[i]]

If nums[i] > s, you cannot take it, so you only skip it.

BASE CASE:
dp[0][0] = True # sum 0 with 0 elements is True

FINAL ANSWER:
dp[n][target]

CODE:
dp[i][s] = dp[i-1][s] # skip it
if nums[i] <= s: # False implies you cannot take it, so you only skip it.
    # now you have two choices
    dp[i][s] = dp[i-1][s] or dp[i-1][s - nums[i]]

return dp[n][target]
'''

def subsetSum(nums, target):
    n = len(nums)
    dp = [[False] * (target + 1) for _ in range(n + 1)]
    dp[0][0] = True # sum 0 with 0 elements is True

    for i in range(1, n + 1):
        for s in range(target + 1):
            dp[i][s] = dp[i-1][s]

            if nums[i-1] <= s:
                # now you have two choices: take it or skip it
                dp[i][s] = dp[i-1][s] or dp[i-1][s - nums[i-1]]
    return dp[n][target]

print(subsetSum(nums, target))

'''
DP =
  s 0, 1, 2, 3, 4, 5, 6
i
0 | T, F, F, F, F, F, F   # sum with first 0 elements
1 | T, T, F, F, F, F, F   # sum with first 1 elements
2 | T, T, T, T, F, F, F   # sum with first 2 elements
3 | T, T, T, T, T, T, F   # sum with first 3 elements
4 | T, T, T, T, T, T, T   # sum with first 4 elements
'''

# Using 1D DP
def subsetSum1D(nums, target):

    dp =[False] * (target + 1)
    dp[0] = True # sum 0 with 0 elements is True

    for num in nums:
        for s in range(target, num - 1, -1):
            dp[s] = dp[s] or dp[s - num]

    return dp[target]

'''
s goes backwards till num, cuz less than that you only skip it.

🔒 Why we loop backwards in 1D DP

We want dp[s - num] to represent the previous row (dp[i-1]), not the current row (dp[i]).

If we loop forward:
- we update dp[s]
- then that updated value gets reused in the same iteration
- 👉 element gets used multiple times ❌

If we loop backward:
- we only use values from previous state
- 👉 each element used once ✅

🧠 One-line intuition
- Backward loop = don't reuse current element
'''


