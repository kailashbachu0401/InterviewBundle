'''
problem: https://leetcode.com/problems/combination-sum/description/
'''

def combinationSum(candidates, target):
    result = []
    current = []
    n = len(candidates)

    def backtrack(index, curr_sum):
        if curr_sum == target:
            result.append(current[:])

        if curr_sum > target or index == n:
            return

        for i in range(index, n):
            # choose
            current.append(candidates[i])

            # explore (reuse allowed, so stay at i)
            backtrack(i, curr_sum + candidates[i])

            # undo
            current.pop()

    backtrack(0, 0)
    return result

'''
When stop exploring a path?

since all are positive, stop when sum > target

Because all numbers are positive:
- going deeper only increases sum
- so once you exceed target, this path is hopeless

This is called pruning. ✅

| Problem      | How choices work                    |
| ------------ | ----------------------------------- |
| Subsets      | choose from remaining right side    |
| Permutations | choose any unused element           |
| Combinations | choose any remaining, order ignored |

| Problem         | Next step           |
| --------------- | ------------------- |
| Subsets         | `i + 1`             |
| Permutations    | `used[]`            |
| Combination Sum | `i` (reuse allowed) and `i+1` (no reuse) -> backtrack(i + 1, total + nums[i]) |


1. What if negatives are included?

This is where things change fundamentally.

Problem with negatives, Earlier we used: if total > target: stop ✅

This works because: all numbers are positive → sum only increases

With negatives: nums = [2, -1], target = 1

Now:

2 → total = 2 → exceeds target
but then:
2 + (-1) = 1 → valid

So: ❌ You cannot prune on total > target

Key consequence - Pruning breaks when negatives are allowed

So:
- You don't prune on total > target when negatives are allowed.
- If no reuse, you just do backtrack(i+1, total + nums[i])
- Once for loop is done, fun automatically exits and combination is added to result only when sum equals target, else not.


2. What if negatives + reuse allowed?

This is the most important one, 🚨 Infinite loop problem

It can lead to an infinite loop, when staying at i, As there is no pruning incase of negatives

Reuse + negatives = infinite search space

How to handle this?
Option 1 — Restrict problem

Most problems:

explicitly say “positive integers only”

That's why.

Option 2 — Add constraints

To safely handle negatives, you must:

1. Limit depth
max depth / number of elements
2. Track visited states
visited = set((index, total))
3. Avoid revisiting same state
Example idea
if (index, total) in visited:
    return
visited.add((index, total))

🧠 Big takeaway (VERY IMPORTANT)
Case	Behavior
Positive + reuse	safe
Positive + no reuse	safe
Negative + no reuse	safe (finite)
Negative + reuse	❌ dangerous (infinite)

🔒 Final mental model

Pruning depends on monotonicity
Negatives break monotonicity

Interview-level answer

If asked:

“What if negatives are allowed?”

You say:

“We lose pruning because sum is no longer monotonic. If reuse is also allowed, it can lead to infinite loops,
so we must either restrict input or track visited states to avoid revisiting the same state.”

That's a very strong answer.

'''