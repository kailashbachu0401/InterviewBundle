# 🧠 What DP Actually Is (No Textbook Explanation)

Dynamic Programming (DP) is used when:

- The **same subproblem appears again and again**
- Recomputing it is **wasteful**

So DP is simply:

- ✅ **Recursion**
- ✅ **Remembering answers** (memoization / table)

That’s it.

---

## 🎯 The DP “Trigger” You Should Feel

When solving a problem, DP becomes natural when you notice:

- “I’m asking the **same question multiple times**”
- “This **recursion tree is repeating**”
- “Brute force explores many **overlapping paths**”

That’s your signal to use DP.

---

## 🔥 The 2 DP Ingredients (Always)

### 1️⃣ State

**What information defines a subproblem?**

Examples:
- `i` → index-based DP
- `i, j` → grid cell
- `i, remaining` → subset sum
- `i, prev` → LIS-style problems

If you can clearly define the state, you’re halfway there.

---

### 2️⃣ Transition

**How do you move from one state to smaller states?**

Examples:
```text
dp[i] = dp[i-1] + dp[i-2]                // Climbing stairs
dp[i] = max(dp[i-1], dp[i-2] + nums[i]) // House robber
```

---

## ✅ DP Styles (Only These 2)

### A) Top-Down DP (Memoized Recursion)

- Write recursion first
- Add a cache (memo)
- Let recursion explore only new states

### B) Bottom-Up DP (Tabulation)

- Build a dp table iteratively
- Start from base cases
- Fill toward the final answer

> 🧠 Same logic, different direction. Choose the style that feels more natural for the problem.