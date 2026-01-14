# 🕸️ GRAPHS — FROM ZERO (PROPERLY)

Before any code, we fix mental models.
Graphs are not scary — they are just Trees + extra rules.

---

## 1️⃣ What is a Graph (forget textbook definitions)

A graph is just:

A set of things (nodes) connected by relationships (edges)

That’s it.

### Examples you already understand:
- Cities + roads
- Services + network calls
- Files + references
- People + friendships

---

## 2️⃣ How graphs differ from trees (THIS IS KEY)

| Tree | Graph |
|----|----|
| One root | No root |
| No cycles | Cycles possible |
| One path between nodes | Multiple paths |
| Implicit visited | Visited must be tracked |

👉 The only new danger in graphs is cycles.

Everything else you already know from Trees.

---

## 3️⃣ The ONE NEW RULE in Graphs 🔴

Never visit the same node twice.

That’s it.

In trees:
- structure guarantees no cycles

In graphs:
- YOU must prevent infinite loops

So every graph traversal has:
- a visited set (or array)

---

## 4️⃣ Graph representation (minimal, interview-safe)

### Adjacency List (THIS IS ALL YOU NEED)

```python
graph = {
    0: [1, 2],
    1: [0, 3],
    2: [0],
    3: [1]
}
```

Meaning:
- Node 0 connects to 1 and 2
- Undirected graph

For directed graph:

```python
graph = {
    0: [1],
    1: [2],
    2: []
}
```

- Edges go only in the listed direction

---

## 5️⃣ Graph traversal = Tree traversal + visited

### DFS (Depth First Search)

```python
def dfs(node):
    if node in visited:
        return

    visited.add(node)

    for nei in graph[node]:
        dfs(nei)

```

Key idea:
- If node is already visited → stop
- Otherwise mark visited and explore neighbors

### BFS (Breadth First Search)

```python
from collections import deque

def bfs(start):
    q = deque([start])
    visited.add(start)

    while q:
        node = q.popleft()
        for nei in graph[node]:
            if nei not in visited:
                visited.add(nei)
                q.append(nei)
```

Key idea:
- Start from a node
- Visit neighbors level by level
- Track visited to avoid revisits

⚠️ Notice:
- Same logic as trees
- Only addition: visited

---
### 🔒 rule (keep it)

BFS: mark visited when enqueuing (prevents duplicates), and distance increments per level

DFS: mark visited as soon as you enter the node (prevents cycles)
---

## 6️⃣ When to use DFS vs BFS (graph intuition)

Use DFS when:
- You want to explore a region
- You care about connectivity
- Flood-fill style problems

Use BFS when:
- You want shortest path
- You care about minimum steps
- Level / distance matters

---

## 7️⃣ Graph problems reduce to 5 patterns (memorize THIS)

| Pattern | Tool |
|------|------|
| Connected components | DFS |
| Flood fill | DFS |
| Shortest path (unweighted) | BFS |
| Cycle detection | DFS |
| Ordering dependencies | Topological sort |

If you can identify which row a problem falls into → you’re 80% done.
