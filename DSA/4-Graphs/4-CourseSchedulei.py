'''
problem: https://leetcode.com/problems/course-schedule/description/
There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1.
You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.

For example, the pair [0, 1], indicates that to take course 0 you have to first take course 1.

Return true if you can finish all courses. Otherwise, return false.
'''

from collections import deque

def canFinish(numCourses, prerequisites):
    graph = [[] for _ in range(numCourses)]
    preq = [0] * numCourses

    # Calculate all preqs
    for a, b in prerequisites:
        graph[b].append(a)
        preq[a]+=1

    # start with courses with 0 preqs
    q = deque([i for i in range(numCourses) if preq[i] == 0])
    taken = 0

    while q:
        course = q.popleft()
        taken += 1 # visited

        for nxt in graph[course]:
            preq[nxt] -= 1 # reduce a preq
            if preq[nxt] == 0:
                q.append(nxt)

    return taken == numCourses

numCourses = 2
prerequisites = [[1,0]]
print(canFinish(numCourses, prerequisites))