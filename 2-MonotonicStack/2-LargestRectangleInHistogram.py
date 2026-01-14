'''
problem: https://leetcode.com/problems/largest-rectangle-in-histogram/description/
You are given an array of integers heights representing the histogram's bar height where the width of each bar is 1.
Return the area of the largest rectangle in the histogram.

Each height can extend left and right until a smaller height appears.
Area for a height = height × width of its span.

To find the span, we need the previous smaller and next smaller heights.
When a height is popped from the monotonic stack:
Next smaller = current index
Previous smaller = new top of the stack
So width = (right − 1) − (left + 1) + 1 = right − left − 1.

If heights are monotonically increasing, appending a 0 forces all elements to pop, ensuring every area is computed.
'''

heights = [2,1,5,6,2,3]

def largestRectangleArea(heights):
    # Use monotonic inc stack

    heights.append(0)
    maxArea = 0
    mStack = []

    for right, h in enumerate(heights):
        while mStack and heights[mStack[-1]] > h:
            mid = mStack.pop()
            height = heights[mid]

            left = mStack[-1] if mStack else -1
            width = right - left - 1

            maxArea = max(maxArea, height * width)

        mStack.append(right)

    heights.pop()  # restore input
    return maxArea

print(largestRectangleArea(heights))

'''
Time Complexity: O(n)
Space Complexity: O(n)
'''