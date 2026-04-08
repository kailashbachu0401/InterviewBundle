# Advanced DP

## 🧠 What is DP (reset your understanding)

You already know:
- DP = recursion + memoization

But that’s not enough.

**👉 Real DP thinking is:**

- Define a state → define transition → build solution

**🔥 Why DP feels hard**

Because:
- state definition is not obvious
- people try to memorize solutions
- transitions feel unclear

We fix this by building from intuition

---

## Approach

For every DP problem:
- Define State
- Define Transition
- Define Base case
- Define Answer

---

## DP Pattern 1: Decision DP (Knapsack style)

At each element, you have two choices:
- Take it or skip it
- answers are built accordingly

This pattern appears in:
- subset sum
- partition equal subset
- knapsack
- target sum
- coin change

---

## DP Pattern 2: Build answer ending at each position

###Important insight

This is: not take/skip
but: build from previous best answers

This pattern appears in:
- LIS

| Pattern    | Type        |
| ---------- | ----------- |
| Subset sum | Decision DP |
| LIS        | Build-up DP |

---

## How do you define DP STATE

### The rule of thumb

When you see a DP problem, ask:
- What is the smallest subproblem whose answer helps me build the final answer?

### There are a few common DP state styles:

**A) Ending at index i**

Used when:
- current element depends on previous elements
- sequence/subsequence problems

Examples:
- LIS
- max sum increasing subsequence

**B) Using first i elements**

Used when:
- take/skip decisions

Examples:
- subset sum
- knapsack

**C) At position (r, c)**

Used when:
- grid movement

Examples:
- unique paths
- min path sum

---
## Backtracking Vs DP

DP problems can also be solved using Backtracking

Then why DP?
- Because backtracking is too expensive.
- Backtracking explores many repeated possibilities.

Example:
- same suffix gets recomputed many times
- exponential growth

DP compresses that repeated work.

### Important distinction

Backtracking is good when:
- you need to print all subsequences
- you need all answers
- constraints are small

DP is good when:
- you only need the best value
- constraints are bigger
- repeated subproblems exist

> if asked to print all increasing subsequences, backtracking is natural, else if asked only max length, true/false, count or best answers, DP is better

---
