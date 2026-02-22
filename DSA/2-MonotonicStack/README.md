# 🧱 MONOTONIC STACK — FROM ZERO

## The kind of questions monotonic stack answers

These questions appear again and again.

For each element:

- What is the next greater element?
- What is the previous smaller element?
- How far can this element extend?
- How long does this element dominate?

### Examples in plain English

- “How many days until a warmer temperature?”
- “How much water is trapped between bars?”
- “What is the largest rectangle in a histogram?”
- “How long can this price stay unbeaten?”

All of these are about:

> relationships between elements based on order and comparison

---

## Why brute force is bad here

Suppose I ask:

> For each element, find the next greater element on the right.

### Naively

- For each `i`, scan `i+1`, `i+2`, …

**Worst case:** `O(n²)`

Your brain already hates this.

---

## The core idea (this is the heart ❤️)

When scanning left → right:

> Once you see a bigger element, some earlier elements become useless forever.

### Example

nums = [2, 1, 3]


When you see `3`:

- `1` will never need to look past `3`
- `2` will never need to look past `3`

So instead of revisiting old elements again and again,
we want a way to:

- resolve their fate once
- and discard them

That’s where monotonic stack comes in.

---

## What is a Monotonic Stack? (conceptual)

A monotonic stack is just:

> A stack that keeps elements in a strict order
> (either increasing or decreasing)

### Two types

- Monotonic increasing (top is largest)
- Monotonic decreasing (top is smallest)

This depends on the question.

---

### The real invariant (THIS is what matters)

While scanning the array:

> The stack holds elements whose answer has not been found yet

That’s it.

Everything else flows from this.

---

## Example 1: Next Greater Element (feel it)

### Problem

For each element, find the next greater element to the right.

### Example

nums = [2, 1, 3]


### Scan step by step

- See `2` → no answer yet → put it aside
- See `1` → no answer yet → put it aside
- See `3` → bigger than `1`
  → `3` is the answer for `1`
- Still bigger than `2`
  → `3` is the answer for `2`
- `3` has no answer yet → put it aside

### Notice

- `1` and `2` were waiting
- `3` resolved them both in one go

That’s the power.

---

## Why a stack, specifically?

Because:

- You want last unresolved element
- You want to resolve in reverse order
- You want `O(1)` removal

A stack gives exactly that.

---

## Monotonicity emerges naturally

In the example:

stack (values): [2, 1]


This is monotonically decreasing.

### Why?

Because if a bigger element were below a smaller one,
it would have already resolved it.

So monotonicity is not forced —
it emerges from the invariant.

---

## When do we use which monotonicity?

Ask ONE question:

> Am I looking for next greater or next smaller?

- Next greater → keep stack decreasing
- Next smaller → keep stack increasing

### Reason

You want to pop elements that the current element can resolve.

---

## What do we store in the stack?

Usually:

- indices, not values

### Why?

You often need:

- distance
- span
- width
- range

But conceptually, think:

> elements waiting for an answer

---

## Time complexity (important intuition)

Each element:

- pushed once
- popped once

Total operations = `O(n)`

That’s why this works.

---

## Conclusion

> The stack holds elements whose answer lies in the future,
> and we remove an element the moment the current element becomes its answer.

That’s monotonic stack in one line.
