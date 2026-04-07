# 👉 Backtracking (full closure)

You touched it in trees, but not formally.

This is important for:

- subsets
- permutations
- combinations

---

## 🧠 Mental template
```
def backtrack(...):
    if base case:
        store result

    for choice in choices:
        make choice
        backtrack(...)
        undo choice
```

### 🚀 What this unlocks

This exact pattern solves:

- subsets
- combinations
- permutations
- N-Queens
- word search
- partitioning problems

---