'''
problem: https://leetcode.com/problems/graph-valid-tree/description/
You have a graph of n nodes labeled from 0 to n - 1.
You are given an integer n and a list of edges where edges[i] = [ai, bi] indicates that there is an undirected edge between nodes ai and bi in the graph.

Return true if the edges of the given graph make up a valid tree, and false otherwise.
'''

from collections import defaultdict


def validTree(n, edges):
    if edges != n - 1:
        return False

    # build graph
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # visited set
    visited = set()

    def dfs(node, parent):
        visited.add(node)
        for nei in graph[node]:
            if nei == parent:
                continue
            if nei in visited:
                return False # cycle found
            if not dfs(nei, node):
                return False
        return True

    return dfs(0, -1) and len(visited) == n # all nodes visited and no cycles