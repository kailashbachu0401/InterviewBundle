'''
problem: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/description/
Also called as Friends Circles / Groups

Problem idea

You're given people and friendships.
If:
- A is friends with B
- B is friends with C

Then:
- A, B, C are one group

You want:
- How many disconnected groups are there?

This is just:
- number of connected components

Union-Find intuition
- Start with n groups
- Every successful union(x, y) reduces groups by 1
- If already in same group, count doesn't change
'''

class UnionFind:
    def __init_(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find((self.parent[x]))
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
        self.count -= 1
        return True

# if edges are given
def countGroups(n, edges):
    uf = UnionFind(n)
    for u, v in edges:
        uf.union(u, v)
    return uf.count

'''
Count represents disconnected groups, cuz for them to reduce count, there should have been an edge between them.
There is no such edge, so we dint traverse it -> we dint union it -> count is not reduced.
'''

# if adjacency matrix is given
'''
  0,1,2,3,4
0[0,1,0,0,0],
1[1,0,1,0,0],
2[0,1,0,1,0],
3[0,0,1,0,1],
4[0,0,0,1,0]
'''

def findCircleNum(isConnected):
    n = len(isConnected)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)

    return uf.count


# Just figure out a way to traverse edge by edge and union the nodes
