'''
problem: https://leetcode.com/problems/trapping-rain-water/description/
You are given an array of integers heights representing the histogram's bar height where the width of each bar is 1.
Return the maximum amount of water that can be trapped after raining.
'''

heights = [0,1,0,2,1,0,1,3,2,1,2,1]

def trap(height):
    stack = []  # indices, monotonic decreasing by height
    water = 0

    for right, h in enumerate(height):
        while stack and height[stack[-1]] < h:
            mid = stack.pop()

            # water is trapped only if there are left and right boundaries
            if not stack:
                break  # no left boundary

            left = stack[-1]

            bounded_height = min(height[left], h) - height[mid]
            width = right - left - 1

            if bounded_height > 0:
                water += bounded_height * width

        stack.append(right)

    return water

print(trap(heights))