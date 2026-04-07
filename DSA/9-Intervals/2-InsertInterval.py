'''
problem: https://leetcode.com/problems/insert-interval/description/

Interval Pattern 2: Scan intervals and merge a rolling new interval ✅
'''

def insert(intervals, newInterval):
    # Assumed that given intervals are already sorted, if not, then sort
    # intervals.sort(key = lambda x: x[0])
    merged = []
    for interval in intervals:
        # completely before
        if interval[1] < newInterval[0]:
            merged.append(interval)

        # completely after
        elif interval[0] > newInterval[1]:
            merged.append(newInterval)
            newInterval = interval

        # overlap
        else:
            newInterval[0] = min(interval[0], newInterval[0])
            newInterval[1] = max(interval[1], newInterval[1])

    merged.append(newInterval)
    return merged

'''
Three cases while scanning intervals

For each interval:

1. Current interval completely before newInterval
interval.end < new.start

No overlap → add current interval

2. Current interval completely after newInterval
interval.start > new.end

No overlap, and newInterval should come before this
→ add newInterval first, then rest

3. Overlapping

Otherwise:

merge into newInterval
new.start = min(new.start, interval.start)
new.end   = max(new.end, interval.end)

So newInterval keeps expanding.

In intervals, many problems become:
- Process in sorted order and maintain one rolling interval

That's the pattern here.
'''