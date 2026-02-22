# 🧠 Python Backend Mastery — A Long-Term Mental Model

## Procedural Programming

> Program is a sequence of steps (procedures/functions) operating on data.

**Core ideas:**

- Functions
- Variables
- Control flow (if, for, while)
- State is explicit and mutable
- Data and behavior are separate

> C is a procedural language

**C has:**

- Functions
- Structs (data only)
- No methods bound to data
- No objects
- No inheritance / polymorphism (built-in)

```
struct User {
    int id;
};

void print_user(struct User u) {
    printf("%d", u.id);
}
```

- 👉 Data (struct)
- 👉 Behavior (function)
- They are not coupled → procedural.

**Contrast with OOP:**

```
class User:
    def print(self):
        print(self.id)
```

- Data + behavior bundled → object.

🔥 Interview line:

> “Procedural programming organizes code around functions, OOP organizes code around objects.”

---

## Is Java only OOP? Is it functional?

**Historically: Java was PURE OOP (almost)**

Before Java 8:

- No functions as values
- No lambdas
- No higher-order functions
- Everything lived inside classes

**After Java 8:**

- Java became partially functional.

Java today is:

> Primarily OOP, with limited functional features

What Java added:

- Lambdas
- Functional interfaces
- Streams
- map, filter, reduce
```
list.stream()
    .filter(x -> x % 2 == 0)
    .map(x -> x * x)
    .toList();
```

BUT ⚠️
Java is not a functional language at its core.

Why?

No true immutability by default

Functions are not first-class in the same way

Everything still revolves around classes

FP features feel bolted on

