'''
problem: https://leetcode.com/problems/daily-temperatures/description/
You are given an array of integers temperatures representing the daily temperatures of a city.
Each integer represents the temperature on that day.
Your task is to find the next warmer day for each day in the array.
If there is no next warmer day, return 0 for that day.
'''

temperatures = [73, 74, 75, 71, 69, 72, 76, 73]

def dailyTemperatures(temperatures):
    mStack = [] # Monotonic Stack to store the indices of the temperatures
    ans = [0] * len(temperatures)

    for i, temp in enumerate(temperatures):
        while mStack and temp > temperatures[mStack[-1]]:
            # Resolve the previous day's temperature
            j = mStack.pop()
            ans[j] = i - j
        mStack.append(i)
    return ans

print(dailyTemperatures(temperatures))

'''
Time Complexity: O(n)
Space Complexity: O(n)
'''