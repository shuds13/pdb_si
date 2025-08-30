import pdb_si
def target_func(a, b, c, d, e=0, f=1):
    s1 = a + b
    s2 = c + d
    s3 = e + f
    prod = s1 * s2
    return prod + s3

print(f"\n*** Press si and hit enter to step into the function ***\n")
import pdb;pdb.set_trace()
res = target_func(
    1,
    2,
    3,
    4,
    e=5,
    f=6,
)
print("Result:", res)
