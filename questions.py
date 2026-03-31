from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

QuestionType = Literal["mcq", "short"]


@dataclass(frozen=True)
class Question:
    id: int
    type: QuestionType
    prompt: str
    options: list[str] | None
    answer: str
    explanation: str
    topic: str
    difficulty: int  # 1..5
    code_snippet: str | None = None  # optional C++ code block shown with the prompt


def get_questions() -> list[Question]:
    """
    150 C++ questions ordered from basics -> advanced OOP / modern C++.

    Topics covered:
      - variables, types, literals, operators, IO           (1-25)
      - control flow, loops                                 (26-45)
      - functions, overloading, default args                (46-60)
      - arrays, pointers, references                        (61-80)
      - strings, vectors, STL containers & algorithms       (81-100)
      - structs, classes, access, constructors, destructors (101-125)
      - inheritance, polymorphism, virtual, abstract        (126-140)
      - modern C++: auto, constexpr, smart ptrs, move, templates, exceptions (141-150)
    """
    q: list[Question] = []

    def mcq(
        prompt: str,
        options: list[str],
        answer: str,
        explanation: str,
        topic: str,
        difficulty: int,
        code_snippet: str | None = None,
    ) -> None:
        q.append(
            Question(
                id=len(q) + 1,
                type="mcq",
                prompt=prompt,
                options=options,
                answer=answer,
                explanation=explanation,
                topic=topic,
                difficulty=difficulty,
                code_snippet=code_snippet,
            )
        )

    def short(
        prompt: str,
        answer: str,
        explanation: str,
        topic: str,
        difficulty: int,
        code_snippet: str | None = None,
    ) -> None:
        q.append(
            Question(
                id=len(q) + 1,
                type="short",
                prompt=prompt,
                options=None,
                answer=answer,
                explanation=explanation,
                topic=topic,
                difficulty=difficulty,
                code_snippet=code_snippet,
            )
        )

    # ── 1-25: Variables, types, literals, operators, IO ──────────────────

    mcq(
        "Which line correctly declares and initializes an integer variable to 10?",
        ["int x = 10;", "int x == 10;", "integer x = 10;", "int x := 10;"],
        "int x = 10;",
        "In C++ you declare a variable with `type name = value;`. "
        "The `==` operator tests equality, `:=` is not valid C++, and `integer` is not a built-in type.",
        "variables",
        1,
    )
    mcq(
        "What does this statement do?",
        [
            "Prints 42 to standard output",
            "Reads 42 from standard input",
            "Writes 42 to a file",
            "Allocates 42 bytes of memory",
        ],
        "Prints 42 to standard output",
        "`std::cout` is the standard character-output stream. The `<<` operator inserts values into the stream.",
        "io",
        1,
        code_snippet="std::cout << 42;",
    )
    mcq(
        "Which header is needed for `std::cout` and `std::cin`?",
        ["<iostream>", "<stdio.h>", "<stream>", "<inputoutput>"],
        "<iostream>",
        "`<iostream>` declares `std::cin`, `std::cout`, `std::cerr`, and `std::clog`.",
        "io",
        1,
    )
    mcq(
        "Which keyword makes a variable's value unchangeable after initialization?",
        ["const", "static", "mutable", "volatile"],
        "const",
        "`const` prevents modification. `static` controls storage duration/linkage; "
        "`mutable` allows modification even in const objects; `volatile` prevents compiler optimization on reads.",
        "const",
        1,
    )
    mcq(
        "What is the value of `x` after this code runs?",
        ["8", "2", "15", "53"],
        "8",
        "`x += 3` is equivalent to `x = x + 3`, so 5 + 3 = 8.",
        "operators",
        1,
        code_snippet="int x = 5;\nx += 3;",
    )
    mcq(
        "Which type stores a single character (typically 1 byte)?",
        ["char", "string", "bool", "int8"],
        "char",
        "`char` is the fundamental character type. "
        "`string` holds sequences of characters; `bool` holds true/false; `int8` is not standard (use `int8_t` from `<cstdint>`).",
        "types",
        1,
    )
    mcq(
        "Which of these is a valid C++ boolean literal?",
        ["true", "True", "TRUE", "yes"],
        "true",
        "C++ boolean literals are exactly `true` and `false` (all lowercase). "
        "`True`, `TRUE`, `yes` are not keywords.",
        "types",
        1,
    )
    mcq(
        "What does `sizeof(int)` return?",
        [
            "The size of int in bytes",
            "The number of digits in an int",
            "Always 4",
            "The size of int in bits",
        ],
        "The size of int in bytes",
        "`sizeof` yields the size in bytes. The standard guarantees `sizeof(int) >= 2`, "
        "but the exact value is implementation-defined (commonly 4 on modern platforms).",
        "types",
        1,
    )
    mcq(
        "Which operator computes the integer remainder (modulo)?",
        ["%", "/", "//", "mod"],
        "%",
        "`%` gives the remainder of integer division. `/` performs division; "
        "`//` is a comment; `mod` is not a C++ operator.",
        "operators",
        1,
    )
    mcq(
        "What does this expression evaluate to?",
        ["2", "2.5", "3", "0"],
        "2",
        "Both operands are `int`, so integer division is performed and the fractional part is truncated: 5 / 2 = 2.",
        "operators",
        1,
        code_snippet="int a = 5, b = 2;\nint result = a / b;  // result = ?",
    )
    mcq(
        "Which statement reads an integer into variable `x` from the keyboard?",
        ["std::cin >> x;", "std::cout >> x;", "std::cin << x;", "read(x);"],
        "std::cin >> x;",
        "`std::cin` is the standard input stream. The extraction operator `>>` reads into the variable on the right.",
        "io",
        1,
    )
    mcq(
        "Without `using namespace std;`, how do you qualify the string type?",
        ["std::string", "iostream::string", "string::std", "std::String"],
        "std::string",
        "All standard library names live in namespace `std`. C++ is case-sensitive, so `String` is wrong.",
        "types",
        1,
    )
    mcq(
        "Which header provides `std::string`?",
        ["<string>", "<strings>", "<cstring>", "<text>"],
        "<string>",
        "`<string>` defines `std::string` and `std::wstring`. "
        "`<cstring>` wraps C's `<string.h>` (C-style string functions like `strlen`).",
        "types",
        1,
    )
    mcq(
        "Which is a valid single-line comment?",
        ["// comment", "/* comment", "<!-- comment -->", "# comment"],
        "// comment",
        "`//` starts a comment that extends to the end of the line. "
        "`/* */` is a block comment (missing closing `*/` here); `#` is a preprocessor prefix, not a comment.",
        "syntax",
        1,
    )
    mcq(
        "What does `\\n` represent inside a string literal?",
        ["Newline (line feed)", "Tab", "Null terminator", "A literal backslash followed by n"],
        "Newline (line feed)",
        "`\\n` is the newline escape sequence. `\\t` is tab; `\\0` is null; `\\\\n` would be backslash + n.",
        "strings",
        1,
    )
    mcq(
        "Which is a valid C++ identifier?",
        ["my_var", "2cool", "class", "my-var"],
        "my_var",
        "Identifiers consist of letters, digits, and underscores, and must not start with a digit. "
        "Reserved keywords (`class`) and hyphens (`my-var`) are not allowed.",
        "syntax",
        1,
    )
    mcq(
        "What is the result of the expression `7 % 3`?",
        ["1", "2", "3", "0"],
        "1",
        "7 divided by 3 is 2 with remainder 1. The `%` operator returns the remainder.",
        "operators",
        1,
    )
    mcq(
        "Which type is used for floating-point numbers with double precision?",
        ["double", "float", "long", "decimal"],
        "double",
        "`double` provides (at least) 64-bit IEEE 754 double-precision. "
        "`float` is single-precision; `decimal` is not a C++ type.",
        "types",
        1,
    )
    mcq(
        "What does the pre-increment operator `++x` do?",
        [
            "Increments x by 1 and returns the new value",
            "Increments x by 1 and returns the old value",
            "Multiplies x by 2",
            "Does nothing",
        ],
        "Increments x by 1 and returns the new value",
        "Pre-increment increments first, then yields the result. "
        "Post-increment (`x++`) yields the old value, then increments.",
        "operators",
        2,
    )
    mcq(
        "Which suffix makes an integer literal `unsigned long long`?",
        ["ULL", "UL", "LL", "U"],
        "ULL",
        "`ULL` (or `ull`) specifies unsigned long long. `UL` is unsigned long; `LL` is signed long long.",
        "types",
        2,
    )
    short(
        "Write a C++ statement that declares a `double` named `price` initialized to 9.99.",
        "double price = 9.99;",
        "`double name = value;` declares and initializes a floating-point variable.",
        "variables",
        1,
    )
    short(
        "Write the `#include` directive needed to use `std::vector`.",
        "#include <vector>",
        "`std::vector` is declared in the `<vector>` header.",
        "stl",
        1,
    )
    short(
        "Write a statement to output `\"Hello\"` followed by a newline using `std::cout`.",
        'std::cout << "Hello" << std::endl;',
        '`std::endl` outputs a newline and flushes the buffer. `"\\n"` is also valid (and often preferred for performance).',
        "io",
        1,
    )
    mcq(
        "What is the value of `x`?",
        ["1", "0", "true", "Undefined"],
        "1",
        "The ternary operator `? :` evaluates the condition first. `5 > 3` is true, so `x = 1`.",
        "operators",
        2,
        code_snippet="int x = (5 > 3) ? 1 : 0;",
    )
    mcq(
        "Which of these correctly uses `auto` to declare a variable?",
        [
            "auto x = 42;",
            "auto x;",
            "auto int x = 42;",
            "x = auto(42);",
        ],
        "auto x = 42;",
        "`auto` deduces the type from the initializer, so an initializer is required. "
        "`auto x;` without an initializer is ill-formed.",
        "modern_cpp",
        2,
    )

    # ── 26-45: Control flow, loops ───────────────────────────────────────

    mcq(
        "Which keyword begins a conditional branch?",
        ["if", "when", "cond", "branch"],
        "if",
        "`if (condition) { ... }` is the fundamental conditional in C++.",
        "control_flow",
        1,
    )
    mcq(
        "Which loop is guaranteed to execute its body at least once?",
        ["do-while", "while", "for", "range-based for"],
        "do-while",
        "`do { body } while (condition);` executes the body before checking the condition.",
        "loops",
        2,
    )
    mcq(
        "What does this code print?",
        ["B", "A", "AB", "Nothing"],
        "B",
        "`0` is falsy in C++. The `if` condition fails, so the `else` branch executes.",
        "control_flow",
        2,
        code_snippet='int x = 0;\nif (x)\n    std::cout << "A";\nelse\n    std::cout << "B";',
    )
    mcq(
        "Which is the correct syntax for a C++ `for` loop?",
        [
            "for (init; condition; increment) { }",
            "for init; condition; increment { }",
            "for (condition; init; increment) { }",
            "loop (init; condition; increment) { }",
        ],
        "for (init; condition; increment) { }",
        "The three clauses (initialization, condition, iteration expression) are separated by semicolons inside parentheses.",
        "loops",
        1,
    )
    mcq(
        "What does `break;` do inside a loop?",
        [
            "Exits the innermost enclosing loop immediately",
            "Skips to the next iteration",
            "Terminates the entire program",
            "Restarts the loop from the beginning",
        ],
        "Exits the innermost enclosing loop immediately",
        "`break` transfers control past the end of the nearest enclosing `for`, `while`, `do`, or `switch`.",
        "loops",
        2,
    )
    mcq(
        "What does `continue;` do inside a loop?",
        [
            "Skips the rest of the loop body and jumps to the next iteration",
            "Exits the loop",
            "Ends the function",
            "Does nothing",
        ],
        "Skips the rest of the loop body and jumps to the next iteration",
        "`continue` jumps to the loop's update expression (for) or condition check (while/do-while).",
        "loops",
        2,
    )
    mcq(
        "Which statement prevents fallthrough in a `switch` case?",
        ["break;", "stop;", "case:", "return;"],
        "break;",
        "Without `break`, execution falls through to the next `case`. "
        "`return` also prevents fallthrough but exits the entire function.",
        "control_flow",
        2,
    )
    mcq(
        "What is the type of the expression `(3 < 5)`?",
        ["bool", "int", "char", "void"],
        "bool",
        "Relational operators produce `bool`. In C (but not idiomatic C++) the result was `int`.",
        "operators",
        2,
    )
    mcq(
        "Which operator tests equality?",
        ["==", "=", "===", "!="],
        "==",
        "`==` compares; `=` assigns. A common bug is writing `if (x = 5)` (assignment, always true for non-zero) instead of `if (x == 5)`.",
        "operators",
        1,
    )
    mcq(
        "What does this loop print?",
        ["012", "0123", "123", "01234"],
        "012",
        "The loop runs for `i = 0, 1, 2`. When `i` reaches 3 the condition `i < 3` is false and the loop ends.",
        "loops",
        2,
        code_snippet="for (int i = 0; i < 3; ++i)\n    std::cout << i;",
    )
    mcq(
        "What is printed by this code?",
        ["024", "0123", "02", "01234"],
        "024",
        "When `i` is odd, `continue` skips the `cout`. So only even values (0, 2, 4) are printed.",
        "loops",
        3,
        code_snippet="for (int i = 0; i < 5; ++i) {\n    if (i % 2 != 0) continue;\n    std::cout << i;\n}",
    )
    mcq(
        "How many times does this loop execute?",
        ["0 times", "1 time", "Infinite loop", "5 times"],
        "0 times",
        "The condition `10 < 5` is immediately false, so the `while` body never executes.",
        "loops",
        2,
        code_snippet="int x = 10;\nwhile (x < 5) {\n    std::cout << x;\n    ++x;\n}",
    )
    mcq(
        "What is the output?",
        ["10", "Nothing", "Infinite loop", "Compilation error"],
        "10",
        "`do-while` always executes the body first. After printing `x` (10), the condition `10 < 5` is false and the loop ends.",
        "loops",
        2,
        code_snippet="int x = 10;\ndo {\n    std::cout << x;\n} while (x < 5);",
    )
    mcq(
        "Which `if` form correctly uses an initializer statement (C++17)?",
        [
            "if (int n = getValue(); n > 0) { }",
            "if (int n > 0 = getValue()) { }",
            "if int n = getValue(); n > 0 { }",
            "if (n = getValue() > 0) { }",
        ],
        "if (int n = getValue(); n > 0) { }",
        "C++17 `if` with initializer: `if (init; condition)`. The variable `n` is scoped to the `if`/`else` block.",
        "control_flow",
        4,
    )
    short(
        "Write a `while` loop that prints numbers 1 to 3 using `std::cout`.",
        "int i = 1; while (i <= 3) { std::cout << i; ++i; }",
        "Initialize before the loop, check the condition, print, then increment.",
        "loops",
        2,
    )
    short(
        "Write a `for` loop header that iterates `i` from 0 to 9 (inclusive).",
        "for (int i = 0; i <= 9; ++i) {",
        "Use `<=` for an inclusive upper bound.",
        "loops",
        1,
    )
    short(
        "Write a `switch` statement header that switches on variable `choice`.",
        "switch (choice) {",
        "Syntax: `switch (expression) {` followed by `case` labels.",
        "control_flow",
        2,
    )
    mcq(
        "What does `else if` allow you to do?",
        [
            "Chain additional conditions after the first `if`",
            "Create a loop",
            "Define a function",
            "Nothing — `else if` is not valid C++",
        ],
        "Chain additional conditions after the first `if`",
        "`else if` is simply an `else` followed by another `if`, allowing multi-way branching.",
        "control_flow",
        1,
    )
    mcq(
        "What value does `x` hold after this code?",
        ["6", "120", "24", "5"],
        "120",
        "The loop computes 5! = 5 × 4 × 3 × 2 × 1 = 120.",
        "loops",
        3,
        code_snippet="int x = 1;\nfor (int i = 1; i <= 5; ++i)\n    x *= i;",
    )

    # ── 46-60: Functions, overloading, default arguments ─────────────────

    mcq(
        "Which is a correct function prototype for a function returning `int` and taking two `int` parameters?",
        [
            "int add(int a, int b);",
            "add int(int a, int b);",
            "int add(a, b);",
            "int add(int, int) {}",
        ],
        "int add(int a, int b);",
        "A prototype declares return type, name, and parameters, ending with `;` (no body).",
        "functions",
        2,
    )
    mcq(
        "What keyword returns a value from a function?",
        ["return", "yield", "break", "give"],
        "return",
        "`return expr;` sends a value back to the caller. `break` exits loops/switch; `yield` is not standard C++.",
        "functions",
        1,
    )
    mcq(
        "Which header provides `std::sqrt`?",
        ["<cmath>", "<math>", "<numbers>", "<calc>"],
        "<cmath>",
        "`<cmath>` is the C++ wrapper for `<math.h>`. It declares `std::sqrt`, `std::pow`, `std::sin`, etc.",
        "standard_library",
        2,
    )
    mcq(
        "What does `&` mean in a parameter declaration like `void f(int& x)`?",
        [
            "x is a reference to the caller's argument",
            "x is a pointer",
            "x is passed by value",
            "It takes the address of x",
        ],
        "x is a reference to the caller's argument",
        "A reference parameter binds directly to the caller's variable — changes inside `f` are visible outside.",
        "functions",
        2,
    )
    mcq(
        "Which best describes pass-by-value?",
        [
            "A copy of the argument is made; the original is unchanged",
            "The function modifies the caller's variable",
            "The argument is always a pointer",
            "No memory is used",
        ],
        "A copy of the argument is made; the original is unchanged",
        "Pass-by-value copies the argument. Modifications to the copy do not affect the caller.",
        "functions",
        2,
    )
    mcq(
        "What is printed?",
        ["15", "5", "10", "Compilation error"],
        "15",
        "The function takes its parameters by value. It returns `a + b` = 5 + 10 = 15.",
        "functions",
        2,
        code_snippet="int add(int a, int b) { return a + b; }\nint main() {\n    std::cout << add(5, 10);\n}",
    )
    mcq(
        "What is the value of `x` after calling `doubleIt`?",
        ["20", "10", "0", "Compilation error"],
        "20",
        "The parameter is a reference (`int& v`), so `v *= 2` modifies the caller's variable directly.",
        "functions",
        3,
        code_snippet="void doubleIt(int& v) { v *= 2; }\nint main() {\n    int x = 10;\n    doubleIt(x);\n}",
    )
    mcq(
        "Which C++ feature allows multiple functions with the same name but different parameter lists?",
        ["Function overloading", "Function overriding", "Templates", "Macros"],
        "Function overloading",
        "Overloading resolves at compile time based on the number and types of arguments.",
        "functions",
        3,
    )
    mcq(
        "What is wrong with this default-argument declaration?",
        [
            "Default arguments must be rightmost — a cannot have a default while b does not",
            "Nothing is wrong",
            "Default arguments must be leftmost",
            "You cannot use default arguments in C++",
        ],
        "Default arguments must be rightmost — a cannot have a default while b does not",
        "In C++, once a parameter has a default value, all subsequent parameters must also have defaults.",
        "functions",
        3,
        code_snippet="int f(int a = 1, int b);",
    )
    mcq(
        "What does `inline` suggest to the compiler?",
        [
            "That the function body may be substituted at the call site",
            "That the function must run on a single line",
            "That the function cannot be recursive",
            "That the function is virtual",
        ],
        "That the function body may be substituted at the call site",
        "`inline` is a hint (the compiler may ignore it). It also allows multiple identical definitions across translation units.",
        "functions",
        3,
    )
    short(
        "Write a function prototype for `void greet()` (no parameters).",
        "void greet();",
        "Prototype = return type + name + `()` + `;`.",
        "functions",
        1,
    )
    short(
        "Write the first line (header) of a function definition for `int max2(int a, int b)`.",
        "int max2(int a, int b) {",
        "Function header: return-type name(params) `{`.",
        "functions",
        2,
    )
    mcq(
        "What does a `void` return type mean?",
        [
            "The function does not return a value",
            "The function returns 0",
            "The function returns a pointer",
            "The function is not callable",
        ],
        "The function does not return a value",
        "`void` means no value is returned. Using `return expr;` in a `void` function is a compilation error.",
        "functions",
        1,
    )
    mcq(
        "Which is true about recursion in C++?",
        [
            "A function can call itself",
            "Recursion is not allowed in C++",
            "Recursive functions cannot have parameters",
            "Recursion always causes a stack overflow",
        ],
        "A function can call itself",
        "Recursion is legal but requires a base case to avoid infinite recursion and eventual stack overflow.",
        "functions",
        2,
    )
    mcq(
        "What does `const` in the parameter `void print(const std::string& s)` prevent?",
        [
            "Modification of `s` inside the function",
            "Calling the function",
            "Passing a string literal",
            "Using `s` at all",
        ],
        "Modification of `s` inside the function",
        "`const T&` passes by reference (no copy) and prevents modification — best practice for large read-only parameters.",
        "functions",
        3,
    )

    # ── 61-80: Arrays, pointers, references ──────────────────────────────

    mcq(
        "What is the index of the first element of a C++ array?",
        ["0", "1", "-1", "It depends on the compiler"],
        "0",
        "C++ arrays are always 0-indexed.",
        "arrays",
        1,
    )
    mcq(
        "Which declares a C-style array of 5 integers named `a`?",
        ["int a[5];", "int a(5);", "array<int> a;", "int[5] a;"],
        "int a[5];",
        "C-style array syntax: `type name[size];`. "
        "`std::array<int, 5> a;` (from `<array>`) is the modern alternative.",
        "arrays",
        2,
    )
    mcq(
        "What does `&x` evaluate to (when `x` is a variable)?",
        ["The memory address of x", "The value of x", "A reference to x", "Bitwise AND of x"],
        "The memory address of x",
        "The unary `&` operator yields the address of its operand, producing a pointer.",
        "pointers",
        2,
    )
    mcq(
        "What does `*p` do when `p` is a pointer?",
        [
            "Dereferences the pointer to access the pointed-to object",
            "Takes the address of p",
            "Multiplies p by something",
            "Deletes p",
        ],
        "Dereferences the pointer to access the pointed-to object",
        "Dereferencing yields an lvalue referring to the object at the address stored in `p`.",
        "pointers",
        2,
    )
    mcq(
        "Which declares a pointer to `int`?",
        ["int* p;", "int &p;", "ptr<int> p;", "pointer int p;"],
        "int* p;",
        "`int* p;`, `int *p;`, and `int * p;` are all equivalent styles.",
        "pointers",
        2,
    )
    mcq(
        "Which is the modern C++ null pointer literal (C++11)?",
        ["nullptr", "0", "NULL", "void"],
        "nullptr",
        "`nullptr` is type-safe (`std::nullptr_t`). `NULL` is a macro (often `0` or `(void*)0`) and can cause ambiguity with overloads.",
        "pointers",
        2,
    )
    mcq(
        "What is a reference in C++?",
        [
            "An alias to an existing object that cannot be reseated",
            "A pointer that must be deleted",
            "A copy of an object",
            "A new object on the heap",
        ],
        "An alias to an existing object that cannot be reseated",
        "Once bound, a reference always refers to the same object. References cannot be null and must be initialized.",
        "references",
        2,
    )
    mcq(
        "Which creates a reference `r` bound to `int x`?",
        ["int& r = x;", "int* r = x;", "int& r;", "ref int r = x;"],
        "int& r = x;",
        "A reference must be initialized at the point of declaration. `int& r;` is ill-formed.",
        "references",
        2,
    )
    mcq(
        "What is the value of `*p` after this code?",
        ["20", "10", "Undefined", "Compilation error"],
        "20",
        "`p` points to `x`. Modifying `*p` modifies `x`, so `*p` (= `x`) is 20.",
        "pointers",
        3,
        code_snippet="int x = 10;\nint* p = &x;\n*p = 20;",
    )
    mcq(
        "What does pointer arithmetic `p + 1` mean for `int* p`?",
        [
            "The address of the next int (p's address + sizeof(int) bytes)",
            "The value pointed to by p plus 1",
            "An error",
            "The address p + 1 byte",
        ],
        "The address of the next int (p's address + sizeof(int) bytes)",
        "Pointer arithmetic scales by the size of the pointed-to type.",
        "pointers",
        3,
    )
    mcq(
        "Which allocates a single `int` on the heap initialized to 5?",
        [
            "int* p = new int(5);",
            "int* p = alloc int(5);",
            "int p = new int(5);",
            "int* p = malloc(5);",
        ],
        "int* p = new int(5);",
        "`new int(5)` allocates, constructs, and returns an `int*`. "
        "`malloc` returns `void*` (C-style, no constructor call).",
        "memory",
        3,
    )
    mcq(
        "How do you free memory allocated with `new int(5)`?",
        ["delete p;", "free(p);", "delete[] p;", "remove p;"],
        "delete p;",
        "`delete` matches `new` (single object). `delete[]` matches `new[]` (arrays). Mixing them is undefined behavior.",
        "memory",
        3,
    )
    mcq(
        "What is a dangling pointer?",
        [
            "A pointer that refers to memory that has been freed",
            "A pointer set to nullptr",
            "A pointer that points to the stack",
            "A pointer to a const object",
        ],
        "A pointer that refers to memory that has been freed",
        "Using a dangling pointer is undefined behavior. After `delete p;`, set `p = nullptr;` as a safety measure.",
        "pointers",
        3,
    )
    mcq(
        "What is the output?",
        ["10 20", "20 20", "10 10", "20 10"],
        "10 20",
        "`p` and `q` point to different variables. Modifying `*q` changes `b` but not `a`.",
        "pointers",
        3,
        code_snippet="int a = 10, b = 10;\nint* p = &a;\nint* q = &b;\n*q = 20;\nstd::cout << *p << \" \" << *q;",
    )
    short(
        "Write an expression that dereferences pointer `p` (pointer to `int`).",
        "*p",
        "`*p` yields the `int` lvalue that `p` points to.",
        "pointers",
        2,
    )
    short(
        "Write a statement that declares a C-style array of 10 doubles named `data`.",
        "double data[10];",
        "C-style array syntax: `type name[size];`.",
        "arrays",
        1,
    )
    mcq(
        "What is the difference between `const int*` and `int* const`?",
        [
            "`const int*` = pointer to const int; `int* const` = const pointer to int",
            "They are the same",
            "`const int*` = const pointer; `int* const` = pointer to const",
            "Neither is valid C++",
        ],
        "`const int*` = pointer to const int; `int* const` = const pointer to int",
        "Read right to left: `const int*` → pointer to (const int); `int* const` → const pointer to (int).",
        "pointers",
        4,
    )
    mcq(
        "What happens if you access an array out of bounds in C++?",
        [
            "Undefined behavior — anything can happen",
            "The program always crashes",
            "An exception is thrown",
            "The compiler prevents it",
        ],
        "Undefined behavior — anything can happen",
        "C++ does not perform bounds checking on raw arrays. Use `std::vector::at()` or `std::array::at()` for checked access.",
        "arrays",
        3,
    )
    short(
        "Write the C++ keyword used for dynamic heap allocation.",
        "new",
        "`new` allocates on the free store and calls the constructor.",
        "memory",
        2,
    )
    short(
        "Write a statement that creates a `new` array of 10 ints on the heap, assigned to `int* arr`.",
        "int* arr = new int[10];",
        "Use `new type[size]` for dynamic arrays. Free with `delete[] arr;`.",
        "memory",
        3,
    )

    # ── 81-100: Strings, vectors, STL containers & algorithms ────────────

    mcq(
        "Which `std::string` operation appends text to the end?",
        ['s += "!";', 's << "!";', 'append(s, "!");', 's.add("!");'],
        's += "!";',
        "`operator+=` appends to a string. Alternatively, `s.append(\"!\")` or `s.push_back('!')` for a single char.",
        "strings",
        2,
    )
    mcq(
        "How do you get the length of `std::string s`?",
        ["s.size() or s.length()", "strlen(s)", "s.len()", "length(s)"],
        "s.size() or s.length()",
        "Both `size()` and `length()` return the number of characters. `strlen` works on C-strings (`const char*`), not `std::string`.",
        "strings",
        2,
    )
    mcq(
        "What does `v.push_back(7)` do for `std::vector<int> v`?",
        [
            "Appends 7 to the end of v",
            "Inserts 7 at the beginning",
            "Replaces all elements with 7",
            "Sorts v",
        ],
        "Appends 7 to the end of v",
        "`push_back` adds an element at the back. The vector resizes if needed.",
        "stl",
        2,
    )
    mcq(
        "Which expression returns the number of elements in `std::vector<int> v`?",
        ["v.size()", "v.length()", "size(v)", "v.count()"],
        "v.size()",
        "`size()` returns the element count. (C++17 also provides `std::size(v)`.)",
        "stl",
        2,
    )
    mcq(
        "How do you access the first element of a non-empty `std::vector<int> v`?",
        ["v[0] or v.front()", "v(0)", "v{0}", "first(v)"],
        "v[0] or v.front()",
        "`operator[]` and `front()` both access the first element. `at(0)` adds bounds checking.",
        "stl",
        2,
    )
    mcq(
        "What is a key difference between `v.at(i)` and `v[i]`?",
        [
            "`at(i)` throws std::out_of_range on invalid index; `v[i]` is undefined behavior",
            "`v[i]` throws; `at(i)` is undefined behavior",
            "No difference",
            "`at(i)` is faster",
        ],
        "`at(i)` throws std::out_of_range on invalid index; `v[i]` is undefined behavior",
        "`at()` performs bounds checking. `operator[]` does not, for performance reasons.",
        "stl",
        3,
    )
    mcq(
        "Which loop iterates over all elements `x` in vector `v`?",
        [
            "for (int x : v) { }",
            "for (x in v) { }",
            "foreach (int x in v) { }",
            "for (int x = v) { }",
        ],
        "for (int x : v) { }",
        "Range-based for: `for (auto& x : container)` (use `auto&` to avoid copies).",
        "loops",
        2,
    )
    mcq(
        "Which STL container stores key-value pairs with unique keys and O(log n) lookup?",
        ["std::map", "std::vector", "std::set", "std::list"],
        "std::map",
        "`std::map` is an ordered associative container (red-black tree). "
        "For O(1) average lookup, use `std::unordered_map`.",
        "stl",
        3,
    )
    mcq(
        "Which algorithm sorts a range in-place?",
        ["std::sort", "std::find", "std::transform", "std::accumulate"],
        "std::sort",
        "`std::sort(begin, end)` sorts in ascending order by default (from `<algorithm>`).",
        "stl",
        3,
    )
    mcq(
        "What does `std::vector<int> v(5, 0);` create?",
        [
            "A vector of 5 ints, each initialized to 0",
            "A vector containing {5, 0}",
            "An empty vector of capacity 5",
            "A compilation error",
        ],
        "A vector of 5 ints, each initialized to 0",
        "The constructor `vector(count, value)` fills `count` elements with `value`.",
        "stl",
        2,
    )
    mcq(
        "Which removes the last element of a `std::vector`?",
        ["v.pop_back()", "v.remove_back()", "v.erase_last()", "v.delete_back()"],
        "v.pop_back()",
        "`pop_back()` removes (and destroys) the last element. Calling it on an empty vector is undefined behavior.",
        "stl",
        2,
    )
    mcq(
        "What does `std::find(v.begin(), v.end(), 42)` return if 42 is not found?",
        ["v.end()", "v.begin()", "nullptr", "-1"],
        "v.end()",
        "STL algorithms return the past-the-end iterator to signal 'not found'.",
        "stl",
        3,
    )
    mcq(
        "Which header provides `std::sort` and `std::find`?",
        ["<algorithm>", "<sort>", "<functional>", "<iterator>"],
        "<algorithm>",
        "Most non-numeric algorithms (`sort`, `find`, `copy`, `transform`, etc.) live in `<algorithm>`.",
        "stl",
        2,
    )
    short(
        "Write a statement that creates a `std::vector<int>` named `nums` containing 1, 2, 3.",
        "std::vector<int> nums = {1, 2, 3};",
        "Brace initialization: `std::vector<int> nums{1, 2, 3};` also works.",
        "stl",
        2,
    )
    mcq(
        "What is the output?",
        ["3", "4", "2", "Compilation error"],
        "3",
        "After the loop, `v` contains {10, 20, 30}. `v.size()` returns 3.",
        "stl",
        2,
        code_snippet="std::vector<int> v;\nv.push_back(10);\nv.push_back(20);\nv.push_back(30);\nstd::cout << v.size();",
    )
    mcq(
        "Which correctly inserts a key-value pair into `std::map<std::string, int> m`?",
        [
            'm["age"] = 25;',
            'm.add("age", 25);',
            'm.push_back("age", 25);',
            'm.insert("age", 25);',
        ],
        'm["age"] = 25;',
        "`operator[]` inserts or updates. `m.insert({\"age\", 25})` also works but does not overwrite existing keys.",
        "stl",
        3,
    )
    mcq(
        "Which container stores elements in FIFO (first-in, first-out) order?",
        ["std::queue", "std::stack", "std::vector", "std::set"],
        "std::queue",
        "`std::queue` is a container adaptor providing FIFO semantics (from `<queue>`).",
        "stl",
        2,
    )
    mcq(
        "What does `std::array<int, 5>` provide over a C-style array?",
        [
            "Bounds-checked `.at()`, `.size()`, iterators, and value semantics",
            "Dynamic resizing",
            "Automatic heap allocation",
            "Nothing — they are identical",
        ],
        "Bounds-checked `.at()`, `.size()`, iterators, and value semantics",
        "`std::array` is a fixed-size container that wraps a C array with a safer, richer interface.",
        "stl",
        3,
    )
    short(
        "Write a statement that sorts vector `v` in ascending order.",
        "std::sort(v.begin(), v.end());",
        "Pass iterator range to `std::sort`. Include `<algorithm>`.",
        "stl",
        3,
    )
    short(
        "Write the `#include` needed for `std::map`.",
        "#include <map>",
        "`std::map` is declared in `<map>`.",
        "stl",
        2,
    )

    # ── 101-125: Structs, classes, access, constructors, destructors ─────

    mcq(
        "In a `class`, what is the default member access?",
        ["private", "public", "protected", "friend"],
        "private",
        "Class members are `private` by default. Use `struct` if you want `public` by default.",
        "oop",
        3,
    )
    mcq(
        "In a `struct`, what is the default member access?",
        ["public", "private", "protected", "internal"],
        "public",
        "`struct` members are `public` by default — the only difference from `class`.",
        "oop",
        2,
    )
    mcq(
        "Which keyword defines a class type?",
        ["class", "type", "object", "record"],
        "class",
        "`class ClassName { ... };` defines a new type with data and behavior.",
        "oop",
        2,
    )
    mcq(
        "What does a constructor do?",
        [
            "Initializes a newly created object",
            "Destroys an object",
            "Copies an object to a file",
            "Allocates stack memory only",
        ],
        "Initializes a newly created object",
        "A constructor runs automatically when an object is created, setting up its initial state.",
        "oop",
        3,
    )
    mcq(
        "What is the constructor name for class `Point`?",
        ["Point", "~Point", "constructor", "Point() const"],
        "Point",
        "The constructor has the same name as the class and no return type (not even `void`).",
        "oop",
        3,
    )
    mcq(
        "What is the destructor name for class `Point`?",
        ["~Point", "Point~", "delete Point", "destructor Point"],
        "~Point",
        "Prefix `~` + class name. The destructor is called when the object's lifetime ends.",
        "oop",
        3,
    )
    mcq(
        "How do you declare a `private` data member `int x;` inside a class?",
        ["private: int x;", "int private x;", "private int x;", "hidden: int x;"],
        "private: int x;",
        "C++ uses access labels (`private:`, `public:`, `protected:`) followed by member declarations.",
        "oop",
        3,
    )
    mcq(
        "How do you access public member `x` of object `p` (not a pointer)?",
        ["p.x", "p->x", "p::x", "x.p"],
        "p.x",
        "Use `.` (dot) for objects and references. `->` is for pointers.",
        "oop",
        2,
    )
    mcq(
        "How do you access member `x` through a pointer `ptr` to an object?",
        [
            "Both ptr->x and (*ptr).x are correct",
            "ptr.x only",
            "(*ptr).x only",
            "ptr::x",
        ],
        "Both ptr->x and (*ptr).x are correct",
        "`ptr->x` is syntactic sugar for `(*ptr).x`.",
        "oop",
        3,
    )
    mcq(
        "What is the purpose of getter/setter methods?",
        [
            "Control and validate access to private data members",
            "Speed up compilation",
            "Avoid constructors",
            "Replace data members with globals",
        ],
        "Control and validate access to private data members",
        "Getters/setters let you enforce invariants (e.g., range checks) while keeping data private.",
        "oop",
        3,
    )
    mcq(
        "What is `this` inside a member function?",
        [
            "A pointer to the current object",
            "A reference to the current object",
            "A copy of the current object",
            "A static variable",
        ],
        "A pointer to the current object",
        "`this` has type `ClassName*` (or `const ClassName*` in a const member function).",
        "oop",
        3,
    )
    mcq(
        "What is a member initializer list?",
        [
            "A way to initialize data members before the constructor body runs",
            "A list of all class members printed at compile time",
            "A dynamic array inside a class",
            "A Python concept not available in C++",
        ],
        "A way to initialize data members before the constructor body runs",
        "Syntax: `Constructor(int v) : member(v) { }`. Preferred because it directly initializes rather than default-constructs then assigns.",
        "oop",
        4,
    )
    mcq(
        "What does `static` mean for a data member?",
        [
            "The member is shared by all instances of the class",
            "The member cannot be modified",
            "The member is allocated on the heap",
            "The member is virtual",
        ],
        "The member is shared by all instances of the class",
        "A `static` member exists once per class, not per object. Access it via `ClassName::member`.",
        "oop",
        4,
    )
    mcq(
        "What does `const` after a member function signature mean?",
        [
            "The function does not modify the object's observable state",
            "The function cannot be called",
            "The function always returns a constant",
            "The function runs at compile time",
        ],
        "The function does not modify the object's observable state",
        "`const` member functions cannot modify non-mutable data members. They can be called on const objects.",
        "oop",
        4,
    )
    mcq(
        "What is printed?",
        ["Alice 30", "Compilation error", "Nothing", "Alice 0"],
        "Alice 30",
        "The constructor uses a member initializer list to set `name` and `age`. The public `print` method accesses them.",
        "oop",
        3,
        code_snippet='class Person {\n    std::string name;\n    int age;\npublic:\n    Person(std::string n, int a) : name(n), age(a) {}\n    void print() { std::cout << name << " " << age; }\n};\nPerson p("Alice", 30);\np.print();',
    )
    mcq(
        "What is an enum class (scoped enumeration)?",
        [
            "A type-safe enumeration whose values don't leak into the enclosing scope",
            "A class that contains only enums",
            "An enum that can be inherited",
            "An enum that is always stored as a char",
        ],
        "A type-safe enumeration whose values don't leak into the enclosing scope",
        "`enum class Color { Red, Green, Blue };` — access values as `Color::Red`. No implicit conversion to int.",
        "types",
        3,
    )
    mcq(
        "Which operator is typically overloaded for outputting a custom type with `std::cout`?",
        ["operator<<", "operator>>", "operator()", "operator[]"],
        "operator<<",
        "Overload `std::ostream& operator<<(std::ostream&, const YourType&)` as a free function (often a friend).",
        "oop",
        4,
    )
    short(
        "Write the class definition header for a class named `Car`.",
        "class Car {",
        "`class Name {` starts the definition. Don't forget `};` at the end.",
        "oop",
        2,
    )
    short(
        "Inside a class, write the line that starts the `public` section.",
        "public:",
        "Access labels end with a colon and affect all subsequent declarations until the next label.",
        "oop",
        2,
    )
    short(
        "Write a constructor header for class `Car` that takes `int year` (with opening brace).",
        "Car(int year) {",
        "Constructor name = class name. No return type.",
        "oop",
        3,
    )
    short(
        "Write the arrow operator used to access members through a pointer.",
        "->",
        "`ptr->member` is equivalent to `(*ptr).member`.",
        "oop",
        2,
    )
    mcq(
        "When is the destructor called for a local (stack) object?",
        [
            "When the object goes out of scope",
            "When `delete` is called",
            "Never — only heap objects have destructors",
            "At program startup",
        ],
        "When the object goes out of scope",
        "Stack objects are destroyed in reverse order of construction when execution leaves their scope (RAII).",
        "oop",
        3,
    )
    mcq(
        "What does the `friend` keyword allow?",
        [
            "A non-member function or class to access private/protected members",
            "A class to inherit from another",
            "A function to become virtual",
            "A variable to become constant",
        ],
        "A non-member function or class to access private/protected members",
        "`friend` grants access. Use sparingly — it breaks encapsulation boundaries.",
        "oop",
        5,
    )
    mcq(
        "What is the Rule of Three?",
        [
            "If a class needs a custom destructor, copy constructor, or copy assignment operator, it likely needs all three",
            "Every class must have exactly three constructors",
            "Loops should never nest more than three levels",
            "A class can have at most three base classes",
        ],
        "If a class needs a custom destructor, copy constructor, or copy assignment operator, it likely needs all three",
        "If you manage a resource manually, you must handle copying and destruction consistently to avoid leaks or double-free.",
        "oop",
        5,
    )
    mcq(
        "What is the output?",
        ["3", "0", "Compilation error", "Undefined"],
        "3",
        "`count` is `static` — it's shared across all instances. Three objects are created, each incrementing `count`.",
        "oop",
        4,
        code_snippet="class Widget {\npublic:\n    static int count;\n    Widget() { ++count; }\n};\nint Widget::count = 0;\nWidget a, b, c;\nstd::cout << Widget::count;",
    )

    # ── 126-140: Inheritance, polymorphism, virtual, abstract ────────────

    mcq(
        "Which access specifier allows derived classes to access base members but hides them from external code?",
        ["protected", "private", "public", "internal"],
        "protected",
        "`protected` members are accessible inside the class and its derived classes, but not from outside.",
        "oop",
        4,
    )
    mcq(
        "Which syntax declares class `Dog` inheriting publicly from `Animal`?",
        [
            "class Dog : public Animal { };",
            "class Dog inherits Animal { };",
            "class Dog -> Animal { };",
            "class Dog (Animal) { };",
        ],
        "class Dog : public Animal { };",
        "Inheritance: `class Derived : access-specifier Base { };`. Public inheritance preserves the base interface.",
        "oop",
        4,
    )
    mcq(
        "What does `virtual` enable on a base-class member function?",
        [
            "Dynamic dispatch — the correct derived override is called at runtime",
            "Compile-time inlining",
            "Prevents overriding",
            "Makes the function static",
        ],
        "Dynamic dispatch — the correct derived override is called at runtime",
        "Without `virtual`, the base version is called even through a base pointer (static binding).",
        "oop",
        4,
    )
    mcq(
        "What is the purpose of `override` (C++11)?",
        [
            "Compiler-enforced check that the function actually overrides a virtual base function",
            "Makes a function virtual",
            "Makes a function private",
            "Prevents a function from being called",
        ],
        "Compiler-enforced check that the function actually overrides a virtual base function",
        "If you misspell the function name or get the signature wrong, `override` makes the compiler report an error.",
        "oop",
        4,
    )
    mcq(
        "When deleting a derived object via a base pointer, what should the base class have?",
        [
            "A virtual destructor",
            "A private constructor",
            "A static destructor",
            "No destructor",
        ],
        "A virtual destructor",
        "Without a virtual destructor, `delete basePtr;` only calls the base destructor — the derived part leaks.",
        "oop",
        5,
    )
    mcq(
        "What is object slicing?",
        [
            "Assigning a derived object to a base variable by value strips away the derived part",
            "Deleting an object twice",
            "Splitting a vector in half",
            "Removing characters from a string",
        ],
        "Assigning a derived object to a base variable by value strips away the derived part",
        "Use pointers or references to base to avoid slicing when working polymorphically.",
        "oop",
        5,
    )
    mcq(
        "What is a pure virtual function?",
        [
            "A virtual function declared with `= 0`, making the class abstract",
            "A function that always returns 0",
            "A function with no parameters",
            "A static function in a base class",
        ],
        "A virtual function declared with `= 0`, making the class abstract",
        "A class with at least one pure virtual function is abstract and cannot be instantiated directly.",
        "oop",
        5,
    )
    mcq(
        "Which keyword prevents a virtual function from being overridden further?",
        ["final", "stop", "sealed", "nooverride"],
        "final",
        "`final` can be applied to a virtual function or to the class itself (preventing inheritance).",
        "oop",
        5,
    )
    mcq(
        "What is printed?",
        ["Woof", "Generic sound", "Compilation error", "Nothing"],
        "Woof",
        "`speak()` is virtual. `a` points to a `Dog`, so dynamic dispatch calls `Dog::speak()`.",
        "oop",
        4,
        code_snippet='class Animal {\npublic:\n    virtual void speak() { std::cout << "Generic sound"; }\n};\nclass Dog : public Animal {\npublic:\n    void speak() override { std::cout << "Woof"; }\n};\nAnimal* a = new Dog();\na->speak();',
    )
    mcq(
        "What is the difference between `public` and `private` inheritance?",
        [
            "Public inheritance preserves base access levels; private makes all inherited members private in derived",
            "Private inheritance is faster at runtime",
            "Public inheritance prevents overriding",
            "No difference",
        ],
        "Public inheritance preserves base access levels; private makes all inherited members private in derived",
        "Public inheritance models 'is-a'; private inheritance models 'is-implemented-in-terms-of'.",
        "oop",
        5,
    )
    mcq(
        "Which cast is safest for downcasting in a polymorphic hierarchy?",
        ["dynamic_cast", "static_cast", "reinterpret_cast", "C-style cast"],
        "dynamic_cast",
        "`dynamic_cast` checks at runtime (RTTI). It returns `nullptr` (pointers) or throws `std::bad_cast` (references) on failure.",
        "oop",
        5,
    )
    mcq(
        "Which best demonstrates runtime polymorphism?",
        [
            "Calling overridden virtual functions via base pointers/references",
            "Using macros",
            "Writing functions in multiple files",
            "Using `#include`",
        ],
        "Calling overridden virtual functions via base pointers/references",
        "Runtime (dynamic) polymorphism uses the virtual table (vtable) for dispatch.",
        "oop",
        4,
    )
    short(
        "Write a pure virtual function signature for `void speak()` in a base class.",
        "virtual void speak() = 0;",
        "`= 0` makes it pure virtual; the class becomes abstract.",
        "oop",
        5,
    )
    short(
        "Write a virtual destructor declaration for class `Animal` using `= default`.",
        "virtual ~Animal() = default;",
        "A defaulted virtual destructor ensures proper cleanup in derived classes.",
        "oop",
        5,
    )
    short(
        "Write the keyword placed after a member function signature to indicate it overrides a base virtual function.",
        "override",
        "Place `override` after the parameter list (and const/ref qualifiers, if any) to request the compiler check.",
        "oop",
        4,
    )

    # ── 141-150: Modern C++ — auto, constexpr, smart ptrs, move, templates, exceptions ──

    mcq(
        "What does `auto` do in a variable declaration?",
        [
            "Deduces the variable's type from its initializer",
            "Makes the variable automatic (stack-allocated)",
            "Makes the variable mutable",
            "Creates a template variable",
        ],
        "Deduces the variable's type from its initializer",
        "`auto x = 42;` → `int`. `auto s = std::string(\"hi\");` → `std::string`. An initializer is required.",
        "modern_cpp",
        2,
    )
    mcq(
        "What does `constexpr` guarantee (for a variable)?",
        [
            "The value is computed at compile time",
            "The value cannot be read",
            "The value is stored on the heap",
            "The value is a pointer",
        ],
        "The value is computed at compile time",
        "`constexpr int n = 10;` — the compiler evaluates and embeds the value. "
        "`const` alone does not guarantee compile-time evaluation.",
        "modern_cpp",
        3,
    )
    mcq(
        "Which smart pointer expresses exclusive (unique) ownership?",
        ["std::unique_ptr", "std::shared_ptr", "std::weak_ptr", "std::auto_ptr"],
        "std::unique_ptr",
        "`unique_ptr` cannot be copied, only moved. When it goes out of scope, it deletes the managed object.",
        "modern_cpp",
        4,
    )
    mcq(
        "Which smart pointer uses reference counting for shared ownership?",
        ["std::shared_ptr", "std::unique_ptr", "std::weak_ptr", "std::scoped_ptr"],
        "std::shared_ptr",
        "The managed object is deleted when the last `shared_ptr` owning it is destroyed or reset.",
        "modern_cpp",
        4,
    )
    mcq(
        "What does `std::move(x)` do?",
        [
            "Casts x to an rvalue reference, enabling move semantics",
            "Physically moves bytes in memory",
            "Copies x",
            "Deletes x",
        ],
        "Casts x to an rvalue reference, enabling move semantics",
        "`std::move` is just a cast (`static_cast<T&&>`). The actual move happens when a move constructor/assignment accepts it.",
        "modern_cpp",
        5,
    )
    mcq(
        "Which best describes RAII?",
        [
            "Resource acquisition is initialization — tie resource lifetime to object lifetime",
            "A keyword for async I/O",
            "A pointer arithmetic optimization",
            "A macro for header inclusion",
        ],
        "Resource acquisition is initialization — tie resource lifetime to object lifetime",
        "RAII ensures cleanup via destructors: files close, memory frees, locks release — automatically when the object dies.",
        "memory",
        5,
    )
    mcq(
        "Which keyword starts a try block for exception handling?",
        ["try", "catch", "throw", "except"],
        "try",
        "`try { /* code */ } catch (const std::exception& e) { /* handle */ }`. `throw` raises an exception.",
        "exceptions",
        3,
    )
    mcq(
        "What does `throw std::runtime_error(\"oops\");` do?",
        [
            "Throws an exception that can be caught by a catch block",
            "Prints 'oops' and continues",
            "Terminates the program immediately",
            "Logs to a file",
        ],
        "Throws an exception that can be caught by a catch block",
        "If no `catch` block matches, `std::terminate` is called.",
        "exceptions",
        3,
    )
    mcq(
        "What is a basic function template?",
        [
            "A function parameterized by one or more types, instantiated by the compiler for each type used",
            "A function that only works with `int`",
            "A function stored in a template file",
            "A function that cannot be overloaded",
        ],
        "A function parameterized by one or more types, instantiated by the compiler for each type used",
        "`template <typename T> T max(T a, T b) { return (a > b) ? a : b; }` — works for any comparable type.",
        "templates",
        4,
    )
    short(
        "Write the `#include` needed to use `std::unique_ptr`.",
        "#include <memory>",
        "Smart pointers (`unique_ptr`, `shared_ptr`, `weak_ptr`) are all in `<memory>`.",
        "modern_cpp",
        3,
    )
    mcq(
        "What does `noexcept` on a function signature indicate?",
        [
            "The function guarantees it will not throw exceptions",
            "The function ignores all exceptions",
            "The function cannot be called",
            "The function returns void",
        ],
        "The function guarantees it will not throw exceptions",
        "If a `noexcept` function does throw, `std::terminate` is called. "
        "Move constructors/assignment operators should be `noexcept` when possible for optimal performance with STL containers.",
        "modern_cpp",
        4,
    )

    assert len(q) == 150, f"Expected 150 questions, got {len(q)}"
    return q
