'''
shortest path from a given source to all nodes in a graph.

Important:
- weights are non-negative
- graph can be directed or undirected
'''

from collections import defaultdict
import heapq

def djikshtras(n, edges, src):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        # if an undirected graoh, append for v too

    distances = [float('inf')] * n

    heap = [(0, src)]

    while heap:
        curr_dist, node = heapq.heappop(heap)

        # stale entry in heap
        if curr_dist > distances[node]:
            continue

        for nei, weight in graph[node]:
            new_dist = curr_dist + weight
            if new_dist < distances[nei]:
                distances[nei] = new_dist
                heapq.heappush(heap, (new_dist, nei))

    return distances

'''
Why BFS is not enough
- BFS works when: every edge has same cost

Example: each move costs 1

Then: fewer edges = shorter path

But if weights differ:

A --1--> B --1--> C
A --10-> C

BFS might think:

A -> C is 1 edge, so maybe better

But actually:

A -> B -> C = 2
A -> C = 10

So we need:
- minimum total weight, not minimum number of edges
- That's where Dijkstra comes in.

CORE IDEA: Always expand the node with the smallest distance seen so far
- This is why we use a min heap.

Greedy Pattern:
- Choose locally optimal item first

standing at a node with a current_distance to it (for source it is 0), we calculate distances to its neis(current_distance + weight)
a nei would have been reached by other paths too, so it would already have current_distance value.
if the new distance is smaller, we update the distance and push the node to the heap.

So:
- Everytime we pop from heap - get node with min current distance.
- We update distances to its neis and push them to the heap.
- We continue this process until the heap is empty.
- At the end, we have the shortest distances to all nodes from the source.

Inference:
Lets say a node is pushed once and its distance is 10, and it never got updated, This means there was no other path where new distance was less than 10.

- Djikshtras is basically a BFS with a heap.
- When a node is popped, it is assumed that this is the best distance for this node
and negetives break this thesis, hence Djikshtras breaks for negatives

Why this “stale entry” check is needed
if curr_dist > dist[node]:
    continue

This is VERY IMPORTANT.

🔥 The problem

We may push multiple entries for same node.

Example
A → B (10)
A → C (1)
C → B (2)

Step-by-step

Start:
- dist[A] = 0

From A:
- B = 10
- C = 1

Heap:
- (1, C), (10, B)

Pop C:
- C → B = 1 + 2 = 3

Update:
- dist[B] = 3
heap = [(3, B), (10, B)]

Now heap has TWO entries for B:
- (3, B)   ← correct
- (10, B)  ← stale

Pop (3, B)
- Good → process

Pop (10, B)
- This is outdated. Skip.


When to think Dijkstra:
Trigger words:
- Weighted graph
- Shortest path
- Minimum cost
- Minimum effort
- Network delay
- Non-negative weights
'''



