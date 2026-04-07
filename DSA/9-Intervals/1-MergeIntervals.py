'''
problem: https://leetcode.com/problems/merge-intervals/description/

Interval Pattern 1: Sort + Merge ✅
'''

def merge(intervals):
    intervals.sort(key = lambda x: x[0])
    merged = []

    for interval in intervals:
        if not merged or interval[0] > merged[-1][1]:
            merged.append(interval)
        else:
            merged[-1][1] = max(merged[-1][1], interval[1])

    return merged


'''
Two intervals overlap if:
- current.start <= previous.end

The KEY trick - Sort intervals by start time first

Without sorting: impossible to reason about overlap cleanly

After sorting: [1,3], [2,6], [8,10], [15,18]

We process one by one:

Start with:

merged = [[1,3]]
Next interval: [2,6]

Check overlap:
2 <= 3 → YES

Merge:
[1, max(3,6)] = [1,6]

Next: [8,10]
8 <= 6 → NO

Add new interval:
merged = [[1,6], [8,10]]

🔒 Core pattern - Compare current interval with last merged interval ✅

🔥 Important variations (must know)

This same pattern is reused in:

1. Insert Interval
Add one interval
merge as needed
2. Non-overlapping intervals
remove minimum intervals to avoid overlap
3. Meeting Rooms
detect overlap count

🧠 Mental model - Intervals problems are always about: How intervals interact when sorted ✅
'''