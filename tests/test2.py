import pdb_si
from func2 import target_func2

print(f"\n*** Press si and hit enter to step into the function ***\n")
import pdb;pdb.set_trace()
res = target_func2(
    1,
    2,
    3,
    4,
    e=5,
    f=6,
)
print("Result:", res)
