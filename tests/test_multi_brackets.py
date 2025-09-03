import pdb_si

def funca(a):
    return a

print(f"\n*** Press si and hit enter to step into the function ***\n")
import pdb;pdb.set_trace()

ans = funca(a=(1,2,3))

print(ans)
