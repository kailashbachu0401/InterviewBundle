# 🔗 Union-Find (Disjoint Set) — From First Principles

## 🧠 What problem does it solve?

Keep track of connected components dynamically, as it processes edge by edge

Meaning:

- You have nodes
- You connect them over time
- You want to quickly answer: 👉 “Are these two nodes connected?”

---

## 🧠 Real-life analogy

Imagine people forming groups:

Initially: everyone is alone

Then:
- A joins B
- B joins C

Now: 👉 A, B, C are in the same group

---

## 🔥 Core idea

Each group has a representative (parent/root)

If two nodes have the same root → they are connected

---

## 🧠 Two operations

### 1️⃣ find(x)

Find the root (representative) of x

### 2️⃣ union(x, y)

Connect x and y → merge their groups

---

## 🧠 Representation

We use an array: parent = [0, 1, 2, 3, 4]

Meaning: each node is its own parent initially

### 🔁 Union example

**union(1, 2)**

- Now: parent[2] = 1

**union(2, 3)**

- Now: parent[3] = 1

**👉 Group:** 1 ← 2 ← 3

**🧠 Find operation**

To find root of 3: 3 → 2 → 1

- Root = 1

---

## 🔥 Optimization 1 — Path Compression

Instead of: 3 → 2 → 1

We flatten it: 3 → 1

```
def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])
    return parent[x]
```

---

## 🔥 Optimization 2 — Union by Rank / Size

Always attach smaller tree under bigger tree.

Why?
- keeps tree shallow
- faster find

---

## 🧠 What problems it solves

👉 You should recognize these patterns:

1. Number of connected components
2. Cycle detection in undirected graph
3. Redundant connection
4. Friend circles / groups
5. Kruskal’s MST

---

### 🔥 Example: Cycle detection

If: union(x, y)

But: find(x) == find(y)

> 👉 already connected → cycle

if graph is given as:

`edges = [[1,2], [2,3], [3,1]]`

You simply:
- process edges one by one, simulate “building” the graph

Example
```
uf = UnionFind(n)

for u, v in edges:
    if uf.find(u) == uf.find(v):
        return True   # cycle found
    uf.union(u, v)
```

---

## 🔒 Mental model

Union-Find = group management system

- find → which group?
- union → merge groups

---

## 🧠 Complexity (important but simple)

- With optimizations: ``~ O(1) per operation``
- Very fast.

---

## Checkout FullCode: [UnionFind.py](./1-UnionFind.py)

### Why find() before union()?

- To know if they belong to same group
- Union should connect roots, not arbitrary nodes

### What happens if you skip find()?

- Suppose: 1 ← 2 ← 3
- Now: union(2, 3)

If you don’t use find():

- you might connect 2 → 3 incorrectly
- create cycles in parent pointers ❌

### Correct way

```
rootX = find(x)
rootY = find(y)
```

Now:
- you always connect roots
- structure remains a tree

### 🔒 Mental model

> Union-Find always connects trees via their roots

### Why `rank += 1` only in else?

> 👉 Because rank represents tree height

Case 1: Unequal heights
- Tree A height = 3
- Tree B height = 2

Attach B under A:
- height stays 3
- no increase needed

Case 2: Equal heights
- Tree A height = 2
- Tree B height = 2

Attach one under another:
- height becomes 3

> 👉 So we increase rank

**🔒 Rule**

> Rank increases only when two equal-height trees are merged

### When NOT to use Union-Find

Union-Find works well for:
- undirected graphs

But not for:
- directed graphs (we’ll explain next)

UnionFind just checks if two nodes are already connected, while dynamically parsing edges
- if not connected, connects their parents
- it doesn't check direction

### Why Union-Find works for cycle detection in undirected graph?

Because:

> Cycle in undirected graph = connecting two nodes already connected

That’s exactly what Union-Find checks.

**🔁 Directed Graph**

Example: 1 → 2 → 3 → 1

Problem here

Even if:
- find(1) == find(3)
- That does NOT necessarily mean:
    - adding edge creates a cycle

Because direction matters.

> For detecting cycles in Directed graphs, DFS/topo works

> “Union-Find works for cycle detection in undirected graphs because a cycle is formed when two nodes already in the same set are connected again. In directed graphs, connectivity alone isn’t enough — direction matters, so we use DFS or topological sorting.”

---

## 🎯 Summary

Union-Find works for:
- building graph
- detecting cycles (undirected)

DFS works for:
- directed cycles
- path-based problems

---
