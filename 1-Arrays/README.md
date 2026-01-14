# Array Patterns

As we go **left → right** in an array, we don’t remember everything from the past.
Almost all array problems can be reduced to one core question:

> **At index i with value x, what past information would be useful to remember?**

As we move forward:
- What facts from the past could affect the decision now?
- There are only a **few categories of answers**
- All problem-solving patterns come from these

---

## The 5 Kinds of Useful Past Information

When scanning **left → right**, the past can help you in only these ways:

---

### 1️⃣ Positions

- Where did something start?
- Where did something last occur?
- How far back was something?

**Examples:**
- Start index of a range
- Last time a value appeared
- Distance between two points

---

### 2️⃣ Values Seen So Far

- Have I seen this before?
- How many times?
- Which values exist behind me?

**Examples:**
- Duplicates
- Frequencies
- Presence / absence

---

### 3️⃣ Aggregates of the Past

Instead of remembering everything, we **compress information**.

- Sum so far
- Maximum so far
- Minimum so far
- Count so far

**Examples:**
- Running sum
- Best profit until now
- Largest element on the left

> This is **information compression**.

---

### 4️⃣ Best / Worst Result So Far

Sometimes you don’t care about all past data — only the **best decision so far**.

- Best answer till now
- Worst case so far

**Examples:**
- Maximum subarray
- Maximum profit
- Longest valid segment

> This is **optimization thinking**.

---

### 5️⃣ State / Condition History

Sometimes the past matters only because of a **condition**.

- Was something valid?
- Are we currently “inside” something?
- Did a rule break earlier?

**Examples:**
- Valid parentheses
- Balanced conditions
- Constraints being violated

---

## One CRUCIAL Realization (Lock This In)

You never remember **everything** from the past.
You remember **exactly one kind of thing** — dictated by the problem.

Depending on the problem, you might need to remember:
- Positions
- Values you’ve seen
- Compressed information (sums, counts)
- Best result so far

---

## Array Problem-Solving Patterns

### 1️⃣ Ask: What Past Information Matters?

- Existence → use a **set**
- Position → **value → index**
- Frequency → **value → count**
- Aggregate → **prefix sum**
- Sliding window → **two pointers**

---

### 2️⃣ Decide: What Do I Need to Track?

- Longest → track **best**
- How many → track **counts**
- Yes / No → track **existence**

---

### 3️⃣ Maintain an Invariant

- Anagram → all counts end at zero
- Sliding window → window is always valid

---

## Example Patterns

- **Two Sum**
  → value → index memory

- **Contains Duplicate**
  → existence memory

- **Valid Anagram**
  → frequency memory

- **Longest Substring Without Repeating Characters**
  → sliding window + set

- **Subarray Sum Equals K**
  → prefix sum + count

```text
|------------|   -> sum_so_far / prefix_sum
..............
|----|---k---|

At a given position:
How many subarrays have sum = k? → How many times have we seen (sum_so_far - k)
