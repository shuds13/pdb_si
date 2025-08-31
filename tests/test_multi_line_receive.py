import pdb_si

# Test 1: Function with trailing comma on last parameter
def func_with_trailing_comma(
    a,
    b,
    c,
    d,
    e=0,
    f=1,
):
    s1 = a + b
    s2 = c + d
    s3 = e + f
    prod = s1 * s2
    return prod + s3

# Test 2: Function with no trailing comma, last param ends with )
def func_no_trailing_comma(
    a,
    b,
    c,
    d,
    e=0,
    f=1
):
    s1 = a + b
    s2 = c + d
    s3 = e + f
    prod = s1 * s2
    return prod + s3

# Test 3: Function with last param ending with )
def func_last_param_ends_with_paren(
    a,
    b,
    c,
    d,
    e=0,
    f=1):
    s1 = a + b
    s2 = c + d
    s3 = e + f
    prod = s1 * s2
    return prod + s3

# Test 4: Function with first param on same line as def
def func_first_param_same_line(a,
    b,
    c,
    d,
    e=0,
    f=1):
    s1 = a + b
    s2 = c + d
    s3 = e + f
    prod = s1 * s2
    return prod + s3


# Test 3: Function with type hints
def func_with_type_hints(
    x: int,
    y: str,
    z: bool
) -> str:
    return f"{x} {y} {z}"

print(f"\n*** Test different multi-line function signature patterns ***\n")

# Test 1: Function with trailing comma
import pdb; pdb.set_trace()  # Test func_with_trailing_comma
res1 = func_with_trailing_comma(
    1,
    2,
    3,
    4,
    e=5,
    f=6,
)

# Test 2: Function with no trailing comma  
import pdb; pdb.set_trace()  # Test func_no_trailing_comma
res2 = func_no_trailing_comma(
    10,
    20,
    30,
    40
)

# Test 3: Function with type hints
import pdb; pdb.set_trace()  # Test func_with_type_hints
res3 = func_with_type_hints(
    100,
    "hello",
    True
)

# Test 4: Function with last param ending with )
import pdb; pdb.set_trace()  # Test func_last_param_ends_with_paren
res4 = func_last_param_ends_with_paren(
    200,
    300,
    400,
    500,
    e=600,
    f=700
)

# Test 5: Function with first param on same line as def
import pdb; pdb.set_trace()  # Test func_first_param_same_line
res5 = func_first_param_same_line(
    800,
    900,
    1000,
    1100,
    e=1200,
    f=1300
)

print("Result 1:", res1)
print("Result 2:", res2)
print("Result 3:", res3)
print("Result 4:", res4)
print("Result 5:", res5)
