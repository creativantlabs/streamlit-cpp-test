"""
Extra questions (appended after the 150 base questions in questions.py):
pointers, arrays, namespaces, libraries, the standard library and flowcharts.

Flowchart questions use Graphviz DOT source (rendered with st.graphviz_chart).
In "pick the right diagram/code" questions the options are labelled
"Flowchart A..D" / "Code A..D" and the visuals live in Question.option_visuals.
"""
from __future__ import annotations

import random
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from questions import Question


# ── Flowchart builder ────────────────────────────────────────────────────

_SHAPES = {
    "t": 'shape=ellipse, style=filled, fillcolor="#E6F4F1"',  # start / end
    "p": "shape=box",                                          # process
    "io": "shape=parallelogram",                               # input / output
    "d": 'shape=diamond, style=filled, fillcolor="#FFF7E0"',   # decision
}


def _esc(text: str) -> str:
    return text.replace('"', '\\"').replace("\n", "\\n")


def _fc(nodes: list[tuple[str, str, str]], edges: list[tuple]) -> str:
    """nodes: (id, kind, label); edges: (src, dst) or (src, dst, edge_label)."""
    lines = [
        "digraph G {",
        '  rankdir=TB; nodesep=0.4; ranksep=0.35;',
        '  node [fontname="Helvetica", fontsize=11];',
        '  edge [fontname="Helvetica", fontsize=10];',
    ]
    for nid, kind, label in nodes:
        lines.append(f'  {nid} [label="{_esc(label)}", {_SHAPES[kind]}];')
    for e in edges:
        if len(e) == 3:
            lines.append(f'  {e[0]} -> {e[1]} [label="{_esc(e[2])}"];')
        else:
            lines.append(f"  {e[0]} -> {e[1]};")
    lines.append("}")
    return "\n".join(lines)


def _sum_flow(*, init: str = "sum = 0\ni = 1", cond: str = "i <= n ?",
              reset_in_loop: bool = False, increment: bool = True) -> str:
    nodes = [
        ("s", "t", "Start"), ("r", "io", "Read n"), ("i", "p", init),
        ("c", "d", cond), ("a", "p", "sum = sum + i"),
        ("o", "io", "Print sum"), ("e", "t", "End"),
    ]
    edges: list[tuple] = [("s", "r"), ("r", "i"), ("i", "c")]
    if reset_in_loop:
        nodes.append(("z", "p", "sum = 0"))
        edges.append(("c", "z", "Yes"))
        edges.append(("z", "a"))
    else:
        edges.append(("c", "a", "Yes"))
    if increment:
        nodes.append(("n", "p", "i = i + 1"))
        edges += [("a", "n"), ("n", "c")]
    else:
        edges.append(("a", "c"))
    edges += [("c", "o", "No"), ("o", "e")]
    return _fc(nodes, edges)


def _even_odd_flow(variant: str = "ok") -> str:
    cond = "n / 2 == 0 ?" if variant == "wrong_cond" else "n % 2 == 0 ?"
    nodes = [
        ("s", "t", "Start"), ("r", "io", "Read n"), ("c", "d", cond),
        ("ev", "io", 'Print "even"'), ("od", "io", 'Print "odd"'), ("e", "t", "End"),
    ]
    edges: list[tuple] = [("s", "r"), ("r", "c")]
    if variant == "swapped":
        edges += [("c", "od", "Yes"), ("c", "ev", "No"), ("od", "e"), ("ev", "e")]
    elif variant == "fallthrough":
        edges += [("c", "ev", "Yes"), ("ev", "od"), ("c", "od", "No"), ("od", "e")]
    else:
        edges += [("c", "ev", "Yes"), ("c", "od", "No"), ("ev", "e"), ("od", "e")]
    return _fc(nodes, edges)


def _prime_flow(*, init: str = "isPrime = true\ni = 2", increment_when_divisible: bool = True) -> str:
    nodes = [
        ("s", "t", "Start"), ("r", "io", "Read n  (n >= 2)"), ("i", "p", init),
        ("c", "d", "i * i <= n ?"), ("m", "d", "n % i == 0 ?"),
        ("f", "p", "isPrime = false"), ("n", "p", "i = i + 1"),
        ("g", "d", "isPrime ?"), ("y", "io", 'Print "prime"'),
        ("x", "io", 'Print "not prime"'), ("e", "t", "End"),
    ]
    edges: list[tuple] = [
        ("s", "r"), ("r", "i"), ("i", "c"), ("c", "m", "Yes"),
        ("m", "f", "Yes"), ("m", "n", "No"), ("n", "c"),
        ("c", "g", "No"), ("g", "y", "Yes"), ("g", "x", "No"),
        ("y", "e"), ("x", "e"),
    ]
    edges.append(("f", "n") if increment_when_divisible else ("f", "c"))
    return _fc(nodes, edges)


def _max_flow(*, init: str = "max = a[0]\ni = 1", cond: str = "i < n ?",
              cmp: str = "a[i] > max ?") -> str:
    nodes = [
        ("s", "t", "Start"), ("r", "io", "Read n and a[0..n-1]"), ("i", "p", init),
        ("c", "d", cond), ("g", "d", cmp), ("u", "p", "max = a[i]"),
        ("n", "p", "i = i + 1"), ("o", "io", "Print max"), ("e", "t", "End"),
    ]
    edges: list[tuple] = [
        ("s", "r"), ("r", "i"), ("i", "c"), ("c", "g", "Yes"),
        ("g", "u", "Yes"), ("g", "n", "No"), ("u", "n"), ("n", "c"),
        ("c", "o", "No"), ("o", "e"),
    ]
    return _fc(nodes, edges)


def _avg_flow(variant: str = "ok") -> str:
    nodes = [
        ("s", "t", "Start"), ("i", "p", "sum = 0\ncount = 0"), ("r1", "io", "Read x"),
        ("c", "d", "x != 0 ?"), ("a", "p", "sum = sum + x\ncount = count + 1"),
        ("r2", "io", "Read x"), ("g", "d", "count > 0 ?"),
        ("pa", "io", "Print sum / count\n(as double)"), ("pn", "io", 'Print "No data"'),
        ("e", "t", "End"),
    ]
    if variant == "sentinel_counted":
        # read -> accumulate -> test: the 0 that ends the input is added and counted too
        nodes = [n for n in nodes if n[0] != "r2"]
        edges: list[tuple] = [
            ("s", "i"), ("i", "r1"), ("r1", "a"), ("a", "c"), ("c", "r1", "Yes"),
            ("c", "g", "No"), ("g", "pa", "Yes"), ("g", "pn", "No"), ("pa", "e"), ("pn", "e"),
        ]
    elif variant == "no_reread":
        nodes = [n for n in nodes if n[0] != "r2"]
        edges = [
            ("s", "i"), ("i", "r1"), ("r1", "c"), ("c", "a", "Yes"), ("a", "c"),
            ("c", "g", "No"), ("g", "pa", "Yes"), ("g", "pn", "No"), ("pa", "e"), ("pn", "e"),
        ]
    elif variant == "no_guard":
        nodes = [n for n in nodes if n[0] not in ("g", "pn")]
        edges = [
            ("s", "i"), ("i", "r1"), ("r1", "c"), ("c", "a", "Yes"), ("a", "r2"),
            ("r2", "c"), ("c", "pa", "No"), ("pa", "e"),
        ]
    else:
        edges = [
            ("s", "i"), ("i", "r1"), ("r1", "c"), ("c", "a", "Yes"), ("a", "r2"),
            ("r2", "c"), ("c", "g", "No"), ("g", "pa", "Yes"), ("g", "pn", "No"),
            ("pa", "e"), ("pn", "e"),
        ]
    return _fc(nodes, edges)


def _loop_shape_flow(kind: str) -> str:
    nodes = [("s", "t", "Start"), ("b", "p", "Loop body"), ("c", "d", "Condition true?"), ("e", "t", "End")]
    if kind == "do_while":
        edges: list[tuple] = [("s", "b"), ("b", "c"), ("c", "b", "Yes"), ("c", "e", "No")]
    elif kind == "while":
        edges = [("s", "c"), ("c", "b", "Yes"), ("b", "c"), ("c", "e", "No")]
    elif kind == "if":
        edges = [("s", "c"), ("c", "b", "Yes"), ("b", "e"), ("c", "e", "No")]
    else:  # decision after body, but nothing loops back
        edges = [("s", "b"), ("b", "c"), ("c", "e", "Yes"), ("c", "e", "No")]
    return _fc(nodes, edges)


_ABS_FLOW = _fc(
    [("s", "t", "Start"), ("r", "io", "Read x"), ("c", "d", "x < 0 ?"),
     ("n", "p", "y = -x"), ("k", "p", "y = x"), ("o", "io", "Print y"), ("e", "t", "End")],
    [("s", "r"), ("r", "c"), ("c", "n", "Yes"), ("c", "k", "No"), ("n", "o"), ("k", "o"),
     ("o", "e")],
)

_HALVING_FLOW = _fc(
    [("s", "t", "Start"), ("i", "p", "x = 10\ncount = 0"), ("c", "d", "x > 1 ?"),
     ("h", "p", "x = x / 2\n(integer division)"), ("k", "p", "count = count + 1"),
     ("o", "io", "Print count"), ("e", "t", "End")],
    [("s", "i"), ("i", "c"), ("c", "h", "Yes"), ("h", "k"), ("k", "c"), ("c", "o", "No"),
     ("o", "e")],
)


# ── Question list ────────────────────────────────────────────────────────

def extra_questions(start_id: int) -> list["Question"]:
    from questions import Question

    q: list[Question] = []

    def _add(**kw) -> None:
        q.append(Question(id=start_id + len(q), **kw))

    def mcq(prompt, options, answer, explanation, topic, difficulty, code_snippet=None,
            flowchart=None):
        shuffled = options[:]
        random.Random(start_id + len(q)).shuffle(shuffled)
        _add(type="mcq", prompt=prompt, options=shuffled, answer=answer,
             explanation=explanation, topic=topic, difficulty=difficulty,
             code_snippet=code_snippet, flowchart=flowchart)

    def short(prompt, answer, explanation, topic, difficulty, code_snippet=None):
        _add(type="short", prompt=prompt, options=None, answer=answer,
             explanation=explanation, topic=topic, difficulty=difficulty,
             code_snippet=code_snippet)

    def visual_mcq(prompt, visuals, explanation, topic, difficulty, *, kind="dot",
                   code_snippet=None, flowchart=None):
        """visuals[0] is the correct one; display order is shuffled deterministically."""
        order = list(range(len(visuals)))
        random.Random(start_id + len(q)).shuffle(order)
        prefix = "Flowchart" if kind == "dot" else "Code"
        labels = [f"{prefix} {chr(65 + i)}" for i in range(len(order))]
        answer = labels[order.index(0)]
        _add(type="mcq", prompt=prompt, options=labels, answer=answer,
             explanation=explanation, topic=topic, difficulty=difficulty,
             code_snippet=code_snippet, flowchart=flowchart,
             option_visuals=[visuals[i] for i in order], visual_kind=kind)

    # ═════════════════════════ POINTERS ═════════════════════════
    mcq(
        "What does this program print?",
        ["9", "5", "The address of x", "Undefined behavior"],
        "9",
        "`p` holds the address of `x`; `*p = 9;` writes through the pointer, so `x` becomes 9.",
        "pointers", 1,
        "int x = 5;\nint* p = &x;\n*p = 9;\nstd::cout << x;",
    )
    short(
        "Which C++11 keyword is the type-safe null pointer literal (preferred over `NULL` and `0`)?",
        "nullptr",
        "`nullptr` has its own type `std::nullptr_t` and converts to any pointer type, "
        "which avoids overload ambiguities that `NULL`/`0` cause.",
        "pointers", 1,
    )
    short(
        "Which unary operator gives the address of a variable?",
        "&",
        "`&x` is the address of `x`; `*p` dereferences a pointer. (In declarations `&` instead declares a reference.)",
        "pointers", 1,
    )
    short(
        "Which unary operator dereferences a pointer (accesses the object it points to)?",
        "*",
        "`*p` yields the object `p` points to. Dereferencing a null or dangling pointer is undefined behavior.",
        "pointers", 1,
    )
    mcq(
        "What does this program print?",
        ["30", "20", "12", "Undefined behavior"],
        "30",
        "`p + 2` points two `int` elements past `arr[0]` (the compiler scales by `sizeof(int)`), i.e. to `arr[2]`.",
        "pointers", 2,
        "int arr[3] = {10, 20, 30};\nint* p = arr;\nstd::cout << *(p + 2);",
    )
    mcq(
        "Given `int arr[5] = {0, 1, 2, 3, 4};`, what does this print?",
        ["3", "3 * sizeof(int)", "4", "Compile error"],
        "3",
        "Subtracting two pointers into the same array gives the number of **elements** between them "
        "(type `std::ptrdiff_t`), not bytes: `&arr[4] - &arr[1] == 3`.",
        "pointers", 3,
        "int* p = &arr[1];\nint* q = &arr[4];\nstd::cout << q - p;",
    )
    mcq(
        "Which line does NOT compile?",
        ["`*p = 5;`", "`p = &b;`", "`*q = 5;`", "`std::cout << *p;`"],
        "`*p = 5;`",
        "`const int* p` is a pointer to `const int`: the pointee cannot be modified through `p`, but `p` itself can be "
        "reassigned. `int* const q` is the opposite: `q` cannot be reseated, but `*q` can be modified.",
        "pointers", 3,
        "int a = 1, b = 2;\nconst int* p = &a;\nint* const q = &a;",
    )
    mcq(
        "What does this program print?",
        ["7", "3", "The address of x", "Compile error"],
        "7",
        "`pp` points to `p`, which points to `x`. `**pp` therefore *is* `x`, so assigning 7 changes `x`.",
        "pointers", 3,
        "int x = 3;\nint* p = &x;\nint** pp = &p;\n**pp = 7;\nstd::cout << x;",
    )
    mcq(
        "What does this program print?",
        ["21", "12", "11", "22"],
        "21",
        "The function receives the addresses of `x` and `y` and swaps the pointed-to values. "
        "Passing pointers is how C-style code emulates pass-by-reference.",
        "pointers", 2,
        "void swap_ints(int* a, int* b) { int t = *a; *a = *b; *b = t; }\n\n"
        "int main() {\n    int x = 1, y = 2;\n    swap_ints(&x, &y);\n    std::cout << x << y;\n}",
    )
    mcq(
        "What is wrong with this function?",
        [
            "It returns the address of a local variable, which is destroyed on return (dangling pointer)",
            "Nothing, it is fine",
            "`v` must be declared `static const`",
            "A function cannot return a pointer",
        ],
        "It returns the address of a local variable, which is destroyed on return (dangling pointer)",
        "`v` lives on the stack and ends with the function call. Using the returned pointer is undefined behavior. "
        "Return by value, or allocate with `new`/smart pointers if the object must outlive the call.",
        "pointers", 3,
        "int* make() {\n    int v = 42;\n    return &v;\n}",
    )
    mcq(
        "Memory obtained with `int* p = new int[10];` must be released with:",
        ["`delete[] p;`", "`delete p;`", "`free(p);`", "Nothing, it is released automatically"],
        "`delete[] p;`",
        "`new[]` must be paired with `delete[]`; `new` with `delete`; `malloc` with `free`. "
        "Mixing them is undefined behavior. Prefer `std::vector` or smart pointers.",
        "memory", 2,
    )
    mcq(
        "What happens if you call `delete p;` twice on the same non-null pointer (without resetting it)?",
        ["Undefined behavior (double free)", "The second call is silently ignored",
         "A `std::bad_alloc` exception is thrown", "The pointer is set to `nullptr` automatically"],
        "Undefined behavior (double free)",
        "`delete` does not reset the pointer. Deleting a *null* pointer is safe, so setting `p = nullptr;` after "
        "`delete` is a common defensive habit; smart pointers avoid the problem entirely.",
        "memory", 3,
    )
    mcq(
        "What happens when a program dereferences a null pointer?",
        ["Undefined behavior (typically a crash / segmentation fault)", "It reads the value 0",
         "A `std::exception` is thrown that can be caught", "The compiler always rejects the program"],
        "Undefined behavior (typically a crash / segmentation fault)",
        "C++ does not check pointers at run time. Always make sure a pointer is non-null before dereferencing it.",
        "pointers", 2,
    )

    # ═════════════════════════ ARRAYS ═════════════════════════
    mcq(
        "What value does `a[4]` hold?",
        ["0", "Garbage (indeterminate)", "3", "Compile error: too few initializers"],
        "0",
        "If an aggregate initializer list is shorter than the array, the remaining elements are "
        "value-initialized (zero for `int`).",
        "arrays", 1,
        "int a[5] = {1, 2, 3};",
    )
    mcq(
        "How can you compute the number of elements of a plain array `int a[10];` in the same scope?",
        ["`sizeof(a) / sizeof(a[0])`", "`sizeof(a)`", "`a.size()`", "`length(a)`"],
        "`sizeof(a) / sizeof(a[0])`",
        "`sizeof(a)` is the total size in bytes; dividing by one element's size gives the count (10). "
        "This only works while `a` is a real array, not after it decays to a pointer. (`std::size(a)` in C++17 does the same.)",
        "arrays", 2,
    )
    mcq(
        "What does `sizeof(arr)` yield inside `f`?",
        ["The size of a pointer (e.g. 8 bytes on a 64-bit system), not the array size",
         "The total size of the caller's array", "Always 0", "Compile error"],
        "The size of a pointer (e.g. 8 bytes on a 64-bit system), not the array size",
        "Array parameters decay to pointers: `int arr[]` in a parameter list means `int* arr`. "
        "Pass the length separately, or use `std::array`/`std::vector`/`std::span`.",
        "arrays", 3,
        "void f(int arr[]) {\n    std::cout << sizeof(arr);\n}",
    )
    mcq(
        "Given `int a[5];`, what happens when the program reads `a[5]`?",
        ["Undefined behavior: C++ does not check array bounds",
         "An `std::out_of_range` exception is thrown", "It returns 0", "The compiler always rejects it"],
        "Undefined behavior: C++ does not check array bounds",
        "Valid indices are 0..4. Out-of-bounds access may crash, return garbage, or appear to work. "
        "`std::vector::at()` and `std::array::at()` do bounds checking and throw `std::out_of_range`.",
        "arrays", 2,
    )
    mcq(
        "How many `int` elements does `int m[3][4];` contain?",
        ["12", "7", "3", "4"],
        "12",
        "A 2D array with 3 rows and 4 columns has 3 × 4 = 12 elements, stored contiguously in row-major order.",
        "arrays", 1,
    )
    mcq(
        "What does this program print?",
        ["7", "9", "5", "4"],
        "7",
        "`m[1][0]` is the first element of the second row (4), `m[0][2]` the last of the first row (3): 4 + 3 = 7.",
        "arrays", 2,
        "int m[2][3] = {{1, 2, 3}, {4, 5, 6}};\nstd::cout << m[1][0] + m[0][2];",
    )
    mcq(
        "For an array `a` and index `i`, `a[i]` is exactly equivalent to:",
        ["`*(a + i)`", "`*a + i`", "`&a + i`", "`a + *i`"],
        "`*(a + i)`",
        "Indexing is defined through pointer arithmetic: `a[i]` is `*(a + i)`. (This is also why `i[a]` compiles!)",
        "arrays", 3,
    )
    mcq(
        "What does this program print?",
        ["6 8", "4 6", "2 4", "6 6"],
        "6 8",
        "`p` starts at `a[0]`; `p += 2` moves it to `a[2]` (value 6). `p[1]` is `*(p + 1)`, i.e. `a[3]` = 8.",
        "arrays", 3,
        "int a[] = {2, 4, 6, 8};\nint* p = a;\np += 2;\nstd::cout << *p << ' ' << p[1];",
    )
    mcq(
        "Why does this code fail to compile?",
        ["Plain arrays cannot be assigned to each other with `=`",
         "`b` is not initialized", "Both arrays need `const`", "`3` is not a valid array size"],
        "Plain arrays cannot be assigned to each other with `=`",
        "Use `std::copy`, a loop, or `std::array` (which is copy-assignable) instead.",
        "arrays", 3,
        "int a[3] = {1, 2, 3};\nint b[3];\nb = a;",
    )
    mcq(
        "What does this program print?",
        ["4 0", "4 garbage", "0 0", "Compile error"],
        "4 0",
        "`std::array<int, 4>` has a compile-time size and, with `{}`, value-initializes all elements to zero. "
        "Unlike a plain array it knows its own size via `.size()`.",
        "arrays", 2,
        "#include <array>\n\nstd::array<int, 4> a{};\nstd::cout << a.size() << ' ' << a[0];",
    )

    # ═════════════════════════ NAMESPACES ═════════════════════════
    mcq(
        "What is the main purpose of namespaces?",
        ["To group names and avoid name collisions between different libraries/modules",
         "To make code run faster", "To allocate memory", "To hide code from the compiler"],
        "To group names and avoid name collisions between different libraries/modules",
        "Two libraries may both define e.g. `print()`. Putting them in different namespaces keeps the names distinct.",
        "namespaces", 1,
    )
    short(
        "Which keyword introduces a namespace, as in `___ geometry { ... }`?",
        "namespace",
        "`namespace name { declarations }` can be reopened later (even in another file) to add more names.",
        "namespaces", 1,
    )
    short(
        "Which operator (two characters) is the scope resolution operator, as in `std::cout`?",
        "::",
        "`A::b` names `b` inside namespace (or class) `A`. A leading `::x` refers to the global `x`.",
        "namespaces", 1,
    )
    mcq(
        "What does this program print?",
        ["AB", "A", "BA", "Compile error: redefinition of `f`"],
        "AB",
        "Each `f` lives in its own namespace, so there is no conflict; `A::f()` runs first, then `B::f()`.",
        "namespaces", 1,
        'namespace A { void f() { std::cout << "A"; } }\n'
        'namespace B { void f() { std::cout << "B"; } }\n\n'
        "int main() {\n    A::f();\n    B::f();\n}",
    )
    mcq(
        "What does this program print?",
        ["12", "21", "11", "22"],
        "12",
        "`::x` is the global `x` (1) and `n::x` is the one in namespace `n` (2).",
        "namespaces", 2,
        "int x = 1;\nnamespace n { int x = 2; }\n\n"
        "int main() {\n    std::cout << ::x << n::x;\n}",
    )
    mcq(
        "What does this program print?",
        ["52", "22", "25", "Compile error: `x` is ambiguous"],
        "52",
        "A local variable hides names brought in by a using-directive, so the unqualified `x` is the local 5. "
        "`n::x` is still the namespace's 2.",
        "namespaces", 3,
        "namespace n { int x = 2; }\nusing namespace n;\n\n"
        "int main() {\n    int x = 5;\n    std::cout << x << n::x;\n}",
    )
    mcq(
        "Why is `using namespace std;` considered bad practice in a header file?",
        ["It forces the using-directive on every file that includes the header, polluting the global namespace",
         "It makes the header compile slower only", "It is a syntax error in headers",
         "It deletes all other namespaces"],
        "It forces the using-directive on every file that includes the header, polluting the global namespace",
        "Prefer qualified names (`std::vector`) in headers. In `.cpp` files, a narrow `using std::cout;` is safer "
        "than importing everything.",
        "namespaces", 2,
    )
    mcq(
        "What does `using std::cout;` do?",
        ["Makes only the name `cout` usable without the `std::` prefix",
         "Makes every name in `std` usable without prefix", "Includes `<iostream>`", "Renames `cout`"],
        "Makes only the name `cout` usable without the `std::` prefix",
        "A using-declaration imports a single name; a using-directive (`using namespace std;`) imports them all. "
        "Neither replaces the `#include`.",
        "namespaces", 2,
    )
    mcq(
        "What is the effect of an unnamed (anonymous) namespace at file scope?",
        ["Its names have internal linkage: they are visible only in that translation unit",
         "Its names become visible in all files", "It is a compile error", "It is the same as `std`"],
        "Its names have internal linkage: they are visible only in that translation unit",
        "`namespace { int counter; }` is the modern replacement for file-local `static` variables/functions.",
        "namespaces", 4,
    )
    mcq(
        "What does `namespace A::B { int v; }` (C++17) mean?",
        ["The same as `namespace A { namespace B { int v; } }`",
         "A namespace `A::B` that exists only in headers", "A compile error before C++20",
         "`B` is a class inside `A`"],
        "The same as `namespace A { namespace B { int v; } }`",
        "C++17 added the compact nested-namespace definition; it saves one level of braces and indentation.",
        "namespaces", 3,
    )
    mcq(
        "What does `namespace fs = std::filesystem;` define?",
        ["A namespace alias: `fs::path` now means `std::filesystem::path`",
         "A new, independent namespace called `fs`", "A macro", "A copy of the library"],
        "A namespace alias: `fs::path` now means `std::filesystem::path`",
        "Aliases shorten long namespace names without importing every name into the current scope.",
        "namespaces", 3,
    )
    mcq(
        "Both `A` and `B` define `void f();`. What happens when the program writes "
        "`using namespace A; using namespace B;` and then calls `f();`?",
        ["Compile error: the call is ambiguous", "`A::f` is chosen because it was imported first",
         "`B::f` is chosen because it was imported last", "Both functions are called"],
        "Compile error: the call is ambiguous",
        "Using-directives do not rank names. Qualify the call (`A::f()`) to resolve the ambiguity.",
        "namespaces", 4,
    )

    # ═════════════════════════ LIBRARIES ═════════════════════════
    mcq(
        "What is the usual difference between `#include <vector>` and `#include \"myheader.h\"`?",
        ["`<...>` searches the system/standard include paths; `\"...\"` searches the current project folder first",
         "`<...>` is for `.cpp` files and `\"...\"` for headers", "There is never any difference",
         "`\"...\"` only works for standard headers"],
        "`<...>` searches the system/standard include paths; `\"...\"` searches the current project folder first",
        "Convention: angle brackets for standard/third-party headers, quotes for your own project headers.",
        "libraries", 1,
    )
    short(
        "Which preprocessor directive copies the contents of a header file into the current source file?",
        "#include",
        "The preprocessor literally pastes the header text before compilation begins.",
        "libraries", 1,
    )
    mcq(
        "What are include guards (`#ifndef X_H / #define X_H / ... / #endif`, or `#pragma once`) for?",
        ["To prevent a header's contents from being processed twice in one translation unit",
         "To protect the header from being edited", "To speed up the linker", "To make functions `inline`"],
        "To prevent a header's contents from being processed twice in one translation unit",
        "Without guards, including a header twice (directly and via another header) can cause redefinition errors, "
        "e.g. for classes.",
        "libraries", 2,
    )
    mcq(
        "In a typical multi-file project, what belongs in the header (`.h`) and what in the source file (`.cpp`)?",
        ["Header: declarations (interface). Source: definitions (implementation)",
         "Header: definitions. Source: declarations", "Both contain only `main()`",
         "Header: comments. Source: code"],
        "Header: declarations (interface). Source: definitions (implementation)",
        "`double area(double r);` goes in the header; the function body goes in the `.cpp`. "
        "Users `#include` the header and link the compiled implementation.",
        "libraries", 2,
    )
    mcq(
        "The build fails with `undefined reference to 'foo()'`. At which stage does this error occur?",
        ["Linking: `foo()` was declared and used but its definition was not found/linked",
         "Preprocessing", "Parsing: the syntax is wrong", "Run time, after the program starts"],
        "Linking: `foo()` was declared and used but its definition was not found/linked",
        "The compiler was satisfied by the declaration. The linker then could not find an object file or library "
        "that defines `foo()` — usually a forgotten `.cpp` file or `-l` flag.",
        "libraries", 3,
    )
    mcq(
        "Which is the correct order of the stages that turn C++ source into an executable?",
        ["Preprocess → compile → assemble → link", "Compile → preprocess → link → assemble",
         "Link → compile → preprocess → assemble", "Assemble → preprocess → compile → link"],
        "Preprocess → compile → assemble → link",
        "The preprocessor handles `#include`/`#define`, the compiler produces assembly, the assembler produces object "
        "files and the linker combines them with libraries.",
        "libraries", 3,
    )
    mcq(
        "What is the main difference between a static library (`.a`/`.lib`) and a shared library (`.so`/`.dll`)?",
        ["Static: code is copied into the executable at link time. Shared: loaded at run time and shared between programs",
         "Static libraries can only be used with C, shared only with C++",
         "Static libraries are always faster to download", "There is no difference"],
        "Static: code is copied into the executable at link time. Shared: loaded at run time and shared between programs",
        "Static linking gives a self-contained but bigger executable; shared libraries save space and can be updated "
        "independently, but must be present at run time.",
        "libraries", 3,
    )
    mcq(
        "In `g++ main.cpp -L/opt/mylib/lib -lmylib`, what do `-L` and `-l` mean?",
        ["`-L` adds a directory to the library search path; `-l` names the library to link (`libmylib`)",
         "`-L` links all libraries; `-l` lists them", "`-L` enables logging; `-l` enables lints",
         "Both mean 'optimize for size'"],
        "`-L` adds a directory to the library search path; `-l` names the library to link (`libmylib`)",
        "`-I` is the analogous flag for header search directories.",
        "libraries", 4,
    )
    mcq(
        "Why is it a problem to define a normal (non-`inline`) function body in a header that is included by two `.cpp` files?",
        ["Each translation unit gets its own definition, causing a 'multiple definition' linker error (ODR violation)",
         "The preprocessor refuses to include it twice", "The function would never be called",
         "It is fine, no problem at all"],
        "Each translation unit gets its own definition, causing a 'multiple definition' linker error (ODR violation)",
        "The One Definition Rule allows only one definition across the program. Mark the function `inline` "
        "(or `constexpr`/template) or move the body into a `.cpp` file.",
        "libraries", 4,
    )

    # ═════════════════════ STANDARD LIBRARY ═════════════════════
    mcq(
        "Which header declares `std::sqrt`, `std::pow` and `std::sin`?",
        ["`<cmath>`", "`<cstdlib>`", "`<algorithm>`", "`<numeric>`"],
        "`<cmath>`",
        "`<cmath>` is the C++ version of C's `math.h`. `<numeric>` has `std::accumulate`/`std::iota`; "
        "`<algorithm>` has `std::sort`/`std::find`.",
        "standard_library", 1,
    )
    mcq(
        "Which header do you include for `std::sort`, `std::find` and `std::reverse`?",
        ["`<algorithm>`", "`<vector>`", "`<numeric>`", "`<utility>`"],
        "`<algorithm>`",
        "The algorithms operate on iterator ranges, so they work with any container.",
        "standard_library", 1,
    )
    mcq(
        "What does this program print?",
        ["10", "4", "24", "0"],
        "10",
        "`std::accumulate` (in `<numeric>`) folds the range with `+`, starting from the initial value 0: 1+2+3+4 = 10.",
        "standard_library", 2,
        "std::vector<int> v{1, 2, 3, 4};\nstd::cout << std::accumulate(v.begin(), v.end(), 0);",
    )
    mcq(
        "What does this program print?",
        ["3 2 1", "1 2 3", "3 1 2", "Compile error"],
        "3 2 1",
        "`std::greater<int>` (in `<functional>`) as comparator sorts in descending order.",
        "standard_library", 2,
        "std::vector<int> v{3, 1, 2};\nstd::sort(v.begin(), v.end(), std::greater<int>());\n"
        "for (int x : v) std::cout << x << ' ';",
    )
    mcq(
        "What does `std::find(v.begin(), v.end(), 42)` return if 42 is not in `v`?",
        ["`v.end()`", "`v.begin()`", "`nullptr`", "-1"],
        "`v.end()`",
        "Search algorithms return the end iterator of the range as 'not found'; compare against it before dereferencing.",
        "standard_library", 2,
    )
    mcq(
        "What does this program print?",
        ["9", "3", "4", "Compile error"],
        "9",
        "`std::max` (and `std::min`) have an `initializer_list` overload that returns the largest of several values.",
        "standard_library", 2,
        "std::cout << std::max({3, 9, 4});",
    )
    mcq(
        "Why does `std::min(2.5, 1)` fail to compile?",
        ["Template argument deduction finds two different types (`double` and `int`) for the same parameter `T`",
         "`std::min` only accepts integers", "`std::min` needs three arguments", "`2.5` is not a valid literal"],
        "Template argument deduction finds two different types (`double` and `int`) for the same parameter `T`",
        "`template <class T> const T& min(const T&, const T&)` needs one common type. "
        "Write `std::min(2.5, 1.0)` or `std::min<double>(2.5, 1)`.",
        "standard_library", 4,
    )
    mcq(
        "What does this program print?",
        ["1 2 3 4", "0 1 2 3", "1 1 1 1", "4 3 2 1"],
        "1 2 3 4",
        "`std::iota` (in `<numeric>`) fills a range with consecutive values starting from the given one.",
        "standard_library", 3,
        "std::vector<int> v(4);\nstd::iota(v.begin(), v.end(), 1);\nfor (int x : v) std::cout << x << ' ';",
    )
    mcq(
        "What does this program print?",
        ["3", "6", "0", "2"],
        "3",
        "`std::count_if` counts the elements for which the predicate is true: 2, 4 and 6.",
        "standard_library", 3,
        "std::vector<int> v{1, 2, 3, 4, 5, 6};\n"
        "std::cout << std::count_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });",
    )
    short(
        "Write the qualified name of the `<algorithm>` function that reverses a range, e.g. `___(v.begin(), v.end());`",
        "std::reverse",
        "`std::reverse(first, last)` reverses the elements in place.",
        "standard_library", 2,
    )
    mcq(
        "What does `std::to_string(42)` return?",
        ["A `std::string` containing \"42\"", "The `int` 42", "A `const char*` to a static buffer", "Nothing, it prints 42"],
        "A `std::string` containing \"42\"",
        "`std::to_string` converts numbers to `std::string`; `std::stoi`/`std::stod` convert in the other direction.",
        "standard_library", 2,
    )
    mcq(
        "What is the return type of `std::pow(2, 10)`?",
        ["`double`", "`int`", "`long`", "`unsigned`"],
        "`double`",
        "The `<cmath>` functions promote integer arguments to `double`, so the result is `1024.0` (prints as 1024). "
        "For exact integer powers use a loop or bit shifts.",
        "standard_library", 3,
    )
    mcq(
        "What does this program print (`#include <iomanip>` is present)?",
        ["3.14", "3.1", "3.14159", "3"],
        "3.14",
        "`std::fixed` selects fixed-point notation and `std::setprecision(2)` then means two digits after the decimal point.",
        "standard_library", 3,
        "std::cout << std::fixed << std::setprecision(2) << 3.14159;",
    )
    mcq(
        "How does `std::getline(std::cin, s)` differ from `std::cin >> s`?",
        ["`getline` reads a whole line including spaces; `>>` stops at the first whitespace",
         "They are identical", "`getline` only reads one character", "`>>` reads whole lines"],
        "`getline` reads a whole line including spaces; `>>` stops at the first whitespace",
        "Typing `Ada Lovelace` gives `s == \"Ada\"` with `>>` but `s == \"Ada Lovelace\"` with `getline`.",
        "standard_library", 2,
    )
    mcq(
        "Why is the `<random>` facility (e.g. `std::mt19937`) preferred over C's `std::rand()`?",
        ["Better statistical quality, explicit engines/distributions and no modulo bias",
         "`rand()` was removed from C++", "`<random>` is always faster than every `rand()`",
         "`rand()` cannot generate integers"],
        "Better statistical quality, explicit engines/distributions and no modulo bias",
        "`std::uniform_int_distribution<int> d(1, 6); d(engine)` gives unbiased dice rolls; `rand() % 6 + 1` is slightly biased.",
        "standard_library", 4,
    )

    # ═════════════════════════ FLOWCHARTS ═════════════════════════
    mcq(
        "In a standard flowchart, which shape represents a decision (a yes/no or true/false question)?",
        ["Diamond", "Rectangle", "Oval (rounded)", "Parallelogram"],
        "Diamond",
        "Diamond = decision (two outgoing arrows, e.g. Yes/No), rectangle = process/assignment, "
        "oval = start/end, parallelogram = input/output.",
        "flowcharts", 1,
    )
    mcq(
        "Which flowchart shape is used for input and output such as `std::cin >> n` or `std::cout << sum`?",
        ["Parallelogram", "Diamond", "Rectangle", "Circle"],
        "Parallelogram",
        "Rectangles hold computations like `sum = sum + i`; parallelograms hold reading/printing.",
        "flowcharts", 1,
    )
    mcq(
        "Which flowchart shape marks the Start and End of a program?",
        ["Oval (terminator)", "Diamond", "Parallelogram", "Hexagon"],
        "Oval (terminator)",
        "Every flowchart should have exactly one Start and at least one End terminator.",
        "flowcharts", 1,
    )
    mcq(
        "Trace the flowchart (integer division). What does it print?",
        ["3", "4", "5", "10"],
        "3",
        "x: 10 → 5 (count 1) → 2 (count 2) → 1 (count 3). Now `x > 1` is false, so it prints 3. "
        "This computes ⌊log₂ 10⌋.",
        "flowcharts", 3,
        flowchart=_HALVING_FLOW,
    )
    mcq(
        "What does this flowchart compute and print for an input `x`?",
        ["The absolute value |x|", "The square x²", "Always −x", "Always x"],
        "The absolute value |x|",
        "For negative `x` the 'Yes' branch sets `y = -x` (positive); otherwise `y = x`. That is |x|.",
        "flowcharts", 2,
        flowchart=_ABS_FLOW,
    )
    visual_mcq(
        "Which C++ code implements the flowchart above?",
        [
            "int y;\nif (x < 0) y = -x;\nelse y = x;\nstd::cout << y;",
            "int y;\nif (x > 0) y = -x;\nelse y = x;\nstd::cout << y;",
            "int y;\nif (x < 0) y = x;\nelse y = -x;\nstd::cout << y;",
            "int y = x * x;\nstd::cout << y;",
        ],
        "The diamond `x < 0 ?` becomes the `if` condition, 'Yes' is the `if` branch, 'No' the `else` branch, "
        "and the parallelogram is the `std::cout`.",
        "flowcharts", 2,
        kind="cpp",
        flowchart=_ABS_FLOW,
    )
    visual_mcq(
        "Procedural exercise: *Read n and print 1 + 2 + … + n.* Which flowchart is correct?",
        [
            _sum_flow(),
            _sum_flow(init="i = 1", reset_in_loop=True),
            _sum_flow(increment=False),
            _sum_flow(cond="i < n ?"),
        ],
        "The correct chart initializes `sum` and `i` **before** the loop, tests `i <= n`, adds `i`, then increments `i`. "
        "Resetting `sum` inside the loop only leaves the last term; a missing `i = i + 1` never terminates; "
        "`i < n` misses the term `n`.",
        "flowcharts", 3,
    )
    visual_mcq(
        "Procedural exercise: *Read an integer n and print \"even\" or \"odd\".* Which flowchart is correct?",
        [
            _even_odd_flow("ok"),
            _even_odd_flow("swapped"),
            _even_odd_flow("wrong_cond"),
            _even_odd_flow("fallthrough"),
        ],
        "Evenness is tested with `n % 2 == 0`, whose 'Yes' branch prints even and 'No' prints odd. "
        "Swapped branches invert the answer, `n / 2 == 0` is true only for 0 and 1, and a missing branch "
        "separation prints both words for even numbers.",
        "flowcharts", 2,
    )
    visual_mcq(
        "Procedural exercise: *Decide whether n ≥ 2 is prime by trial division up to √n.* Which flowchart is correct?",
        [
            _prime_flow(),
            _prime_flow(init="isPrime = true\ni = 1"),
            _prime_flow(init="isPrime = false\ni = 2"),
            _prime_flow(increment_when_divisible=False),
        ],
        "Start with `isPrime = true` and the first candidate divisor `i = 2`. Starting at `i = 1` makes every n 'divisible' "
        "(n % 1 == 0), starting with `false` can never print 'prime', and skipping `i = i + 1` after a divisor is "
        "found loops forever.",
        "flowcharts", 5,
    )
    visual_mcq(
        "Procedural exercise: *Find the maximum of an array a[0..n-1] that may contain negative numbers.* "
        "Which flowchart is correct?",
        [
            _max_flow(),
            _max_flow(init="max = 0\ni = 0"),
            _max_flow(cond="i <= n ?"),
            _max_flow(cmp="a[i] < max ?"),
        ],
        "Initialize `max` with the first element, then scan the rest with `i < n`, updating when `a[i] > max`. "
        "`max = 0` is wrong if all values are negative, `i <= n` reads the invalid element `a[n]`, "
        "and `<` computes the minimum.",
        "flowcharts", 4,
    )
    visual_mcq(
        "Which flowchart represents a **do-while** loop (the body always runs at least once)?",
        [
            _loop_shape_flow("do_while"),
            _loop_shape_flow("while"),
            _loop_shape_flow("if"),
            _loop_shape_flow("no_loop"),
        ],
        "In a do-while the body comes first and the condition is tested afterwards; 'Yes' returns to the body. "
        "In a `while` loop the test happens before the body; in the `if` chart and the last chart nothing loops back.",
        "flowcharts", 3,
    )

    # ── Multi-part procedural exercise: average until the sentinel 0 ──
    visual_mcq(
        "Exercise part 1/4 — *Read integers until the user enters 0 (the sentinel, which is not data). Print the "
        "average of the numbers read, or \"No data\" if there were none.* Which flowchart is correct?",
        [
            _avg_flow("ok"),
            _avg_flow("no_reread"),
            _avg_flow("no_guard"),
            _avg_flow("sentinel_counted"),
        ],
        "A correct design reads once before the loop, processes `x`, then reads again at the end of every iteration; "
        "after the loop it guards the division with `count > 0`. Without re-reading the loop never ends; "
        "without the guard an immediate 0 divides by zero; and processing before testing counts the sentinel.",
        "flowcharts", 4,
    )
    visual_mcq(
        "Exercise part 2/4 — Which C++ code matches the correct flowchart from part 1?",
        [
            "int sum = 0, count = 0, x;\nstd::cin >> x;\nwhile (x != 0) {\n    sum += x;\n    ++count;\n"
            "    std::cin >> x;\n}\nif (count > 0) std::cout << static_cast<double>(sum) / count;\n"
            "else std::cout << \"No data\";",
            "int sum = 0, count = 0, x;\nstd::cin >> x;\nwhile (x != 0) {\n    sum += x;\n    ++count;\n"
            "    std::cin >> x;\n}\nif (count > 0) std::cout << sum / count;\nelse std::cout << \"No data\";",
            "int sum = 0, count = 0, x;\ndo {\n    std::cin >> x;\n    sum += x;\n    ++count;\n} while (x != 0);\n"
            "if (count > 0) std::cout << static_cast<double>(sum) / count;\nelse std::cout << \"No data\";",
            "int sum = 0, count = 0, x;\nstd::cin >> x;\nwhile (x = 0) {\n    sum += x;\n    ++count;\n"
            "    std::cin >> x;\n}\nif (count > 0) std::cout << static_cast<double>(sum) / count;\n"
            "else std::cout << \"No data\";",
        ],
        "The first listing is the only one that tests `x != 0` before processing, re-reads inside the loop, and divides "
        "as `double`. The second truncates (integer division), the third counts the sentinel (do-while), "
        "the fourth assigns (`=`) instead of comparing (`!=`).",
        "flowcharts", 4,
        kind="cpp",
    )
    mcq(
        "Exercise part 3/4 — What does the correct program print for the input `3 4 0`?",
        ["3.5", "3", "2.33333", "7"],
        "3.5",
        "sum = 7, count = 2, and the division is done in `double`: 7 / 2 = 3.5. (Integer division would print 3; "
        "counting the sentinel would give 7/3 ≈ 2.33333.)",
        "flowcharts", 3,
    )
    mcq(
        "Exercise part 4/4 — What does the correct program print if the very first input is `0`?",
        ["No data", "0", "nan / a crash from dividing by zero", "Nothing; it waits for more input"],
        "No data",
        "The loop body never runs, so `count == 0`. The `count > 0` decision sends the flow to the 'No data' branch "
        "and avoids the division by zero (integer `0/0` is undefined behavior, floating-point `0.0/0` gives NaN).",
        "flowcharts", 3,
    )

    return q
