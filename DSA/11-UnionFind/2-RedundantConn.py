'''
problem: https://leetcode.com/problems/redundant-connection/description/
'''

class UnionFind:
    def __init__(self, n):
        self.parent = [i for i in range(n + 1)]
        self.rank = [0] * (n + 1)

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        elif self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        return True


def findRedundantConnection(edges):
    n = len(edges)
    uf = UnionFind(n)

    for u, v in edges:
        if uf.find(u) == uf.find(v):
            return [u, v]   # cycle found
        uf.union(u, v)

edges = [[1,2],[1,3],[2,3]]
# Output: [2,3]