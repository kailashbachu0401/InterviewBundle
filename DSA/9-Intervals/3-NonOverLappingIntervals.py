'''
problem: https://leetcode.com/problems/non-overlapping-intervals/description/

Interval Pattern 3: Greedy → sort by end time ✅
'''

def eraseOverlapIntervals(intervals):
    intervals.sort(key = lambda x: x[1])
    count = 0
    prev_end = intervals[0][1]
    for i in range(1, len(intervals)):
        if intervals[i][0] < prev_end:
            count += 1 # remove this interval
        else:
            prev_end = intervals[i][1]
    return count


'''
🧠 Step 1 — What are we minimizing?

👉 Remove minimum intervals
👉 Equivalent to: Keep maximum non-overlapping intervals

🧠 Step 2 — Key greedy idea

Always keep the interval with the smallest end

Why? - smaller end leaves more room for future intervals

🧠 Step 3 — Sort by end time
intervals.sort(key=lambda x: x[1])

🧠 Step 4 — Process

Keep track of: prev_end

Loop:

If current.start >= prev_end → keep it
Else → overlap → remove it

🧠 Why this works

Example (sorted by end): [1,3], [2,4]

We keep [1,3] (ends earlier)

Then [2,4] overlaps → remove it

If we kept [2,4] instead: we lose more future options ✅

| Problem         | Pattern              |
| --------------- | -------------------- |
| Merge intervals | sort by start        |
| Insert interval | scan + merge         |
| Non-overlapping | sort by end (greedy) |

We sort by end time because choosing the interval with the smallest end leaves maximum space for the remaining intervals, maximizing the number of non-overlapping intervals.

🧠 Greedy pattern unlocked
- When you want to fit maximum intervals → sort by end time
'''