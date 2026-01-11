# 🌳 TREES & DFS — FROM ZERO

We will go in **4 very small steps**:

- What is a tree really?
- Why recursion is natural here
- What DFS actually means (without code)
- The 3 DFS templates (this is the gold)

No rushing.

---

## 1️⃣ What is a Tree (forget CS definition)

Forget “nodes, edges, blah blah”.

Think of a tree as:

> A set of choices that branch, but never loop back.

### Examples you already understand

- Folder structure
- Organization hierarchy
- Family tree
- Game decision paths

### Key properties

- One starting point (root)
- Every node can lead to multiple children
- No cycles (you never come back)

That’s it.

---

## 2️⃣ Why recursion is NATURAL for trees

This is the biggest mental block for people — so let’s kill it early.

Ask yourself this:

> How would a human solve a tree problem?

### Example

“Find the height of a tree”

A human instinctively says:

> Height of tree =
> 1 + max(height of left subtree, height of right subtree)

That sentence **is recursion**.

- You didn’t think about stack frames.
- You didn’t think about base cases explicitly.
- You just defined the problem in terms of itself.

That’s why recursion fits trees like a glove.

---

## 3️⃣ What DFS really means (no jargon)

DFS = **Depth First Search**

In human words:

> “Go as deep as possible before coming back.”

You:

- go down one path
- hit a dead end
- come back up
- try the next path

This is exactly how you explore:

- mazes
- decisions
- hierarchies

---

## 4️⃣ The MOST IMPORTANT PART: DFS has only 3 patterns

Every tree DFS problem is one of these.

---

### 🧱 Template 1: Compute something from children
*(aka post-order thinking)*

#### Core idea

“I don’t know the answer myself.
I’ll ask my children, then combine.”

#### Characteristics

- No shared mutable state
- Each call returns one value
- Parent waits for children
- No backtracking

#### Examples

- height of tree
- diameter
- sum of subtree
- balanced tree check

#### Pattern

    def dfs(node):

      if not node:
          return base_value

      left = dfs(node.left)
      right = dfs(node.right)

      return combine(left, right, node)

#### Checklist — use Template 1 if:

- ❓ You’re asked for a single value
- ❓ Answer depends on children’s answers
- ❓ You can define answer as
f(node) = combine(f(left), f(right))

---

### 🧱 Template 2: Carry something from parent to children
*(aka pre-order thinking)*

#### Core idea

“The parent gives me some information.
I must respect it and pass updated info to my children.”

#### Characteristics

- State is passed as argument
- No shared mutable structure needed
- Usually returns boolean / nothing

#### Examples

- path sum
- max root-to-leaf
- validate BST
- prefix-based constraints

#### Pattern

    def dfs(node, state):
      if not node:
          return

      new_state = update(state, node)
      dfs(node.left, new_state)
      dfs(node.right, new_state)


#### Checklist — use Template 2 if:

- ❓ There are constraints from ancestors
- ❓ You need to “carry info” downwards
- ❓ Validity depends on path from root

---

### 🧱 Template 3: Path tracking / backtracking
*(choices + undo)*

#### Core idea

“I’m making choices.
I must undo them when I come back.”

#### Characteristics

- Uses shared mutable state (path, list)
- Must undo changes
- DFS + backtracking
- Results collected in a list

#### Examples

- all root-to-leaf paths
- path sum = target
- combinations

#### Pattern

    def dfs(node):
      if not node:
          return

      path.append(node.val)      # choose

      if leaf_condition:
          result.append(path.copy())
      else:
          dfs(node.left)
          dfs(node.right)

      path.pop()                 # un-choose

#### Checklist — use Template 3 if:

- ❓ You must return all paths / combinations
- ❓ The output is a list of lists
- ❓ You need to record history

---

## 🌳 DFS vs Backtracking — Crystal Clear

### Core idea
- **All tree problems use DFS**
- **Not all tree problems need backtracking**

---

### Templates 1 & 2 (Pure DFS — no backtracking)
- You **go down the tree**, optionally carrying some info
- Results **come back via return statements**
- You **do NOT undo choices**
- No add/remove, no un-visit

👉 This is **DFS without backtracking**

**Examples**
- Compute values from children
- Carry info top → down (sum, depth, constraints)

---

### Template 3 (DFS + Backtracking)
- You **DFS the tree**
- You **make a choice**
- You **undo the choice** (backtrack)
- Typically involves a **mutable list**
  - `add → recurse → pop`

**Example**
- `BinaryTreePaths`

---

### What DFS answers
> **How do I explore the structure?**

---

### What Backtracking answers
> **How do I manage shared, mutable choices during exploration?**

---

### Key distinction
- Templates 1 & 2:
  - May pass shared info
  - **No undo, no un-visit**

- Template 3:
  - Shared mutable state
  - **Must undo choices**

---

## 🔒 One sentence to lock it forever
> **All backtracking uses DFS, but not all DFS is backtracking.**


---

## 🧩 How to identify the right template (30-second rule)

When you see a tree problem, ask in this order:

❓ Do I need all paths / all answers?

Yes → Template 3

❓ Do I need to carry info from parent?

Yes → Template 2

❓ Else → Template 1

This rule works shockingly well.

---

## 🚨 Very important reassurance

You do **NOT** need:

- fancy tree theory
- memorizing traversals
- drawing diagrams

If you master these **3 DFS templates**, you can solve:

> **90% of tree interview problems.**