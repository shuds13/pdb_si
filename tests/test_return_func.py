import pdb_si
def funca(a):
    return a+1

def funcb():
    print('Press si to step into func on return line')
    return funca(a=1)

print(f"\n*** Press si and hit enter to step into the function ***\n")
import pdb;pdb.set_trace()

funcb()
