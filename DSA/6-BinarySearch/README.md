# 🔎 BinarySearch

Binary serach is not about arrays, its about searching on answer space.

**Binary search works when:**
- The answer space is monotonic (one-directional change).

---

## 🧠 Binary Search Pattern (VERY IMPORTANT)

You’re not searching for value.

You’re searching for:
- boundary / transition point

---

## Binary Search Pattern 1

> Find first index where condition becomes true

Find first true / leftmost valid / boundary

Eg: [FirstBadVersion](./1-FirstBadVersion.py), [searchInsertPosition](./2-SearchInsertPosition.py)

**Mental model 🔒**

> Whenever you search for “first occurrence”, keep track of the best candidate.

This pattern alone solves:

- first bad version
- search insert position
- lower bound
- first occurrence
- many “minimum satisfying condition” problems

---

## Binary Search Pattern 2

Array not fully sorted, but one half is sorted

Eg: [Search on rotated array](./3-SearchRotatedArray.py)

---

## Binary Search Pattern 3:

Search on answer space using a monotonic condition

**🔒 Mental model**

Whenever you see:

- “minimum X such that condition holds”
- “maximize X under constraint”
- “find smallest/largest value satisfying something”

👉 Think:

> Binary Search on Answer

🧠 Recognizing this pattern

Trigger words:

- minimum speed
- minimum capacity
- maximum feasible value
- can we do it in X?
- within k operations / hours / days

Eg: [Eating Bananas](./4-EatingBananas.py)