import pdb_si
from func2 import target_func2

class Calculator:
    def __init__(self, name):
        self.name = name
    
    def calculate(self, a, b, c, d, e=0, f=1):
        s1 = a + b
        s2 = c + d
        s3 = e + f
        prod = s1 * s2
        return prod + s3
    
    def complex_calc(self, x, y, z):
        result = self.calculate(
            x,
            y,
            z,
            x + y,
            e=y + z,
            f=z + x
        )
        return result * 2

print(f"\n*** Press si and hit enter to step into the class method ***\n")
import pdb;pdb.set_trace()

calc = Calculator("TestCalc")
res = calc.calculate(
    1,
    2,
    3,
    4,
    e=5,
    f=6,
)
print("Result:", res)

# Test the complex method too
complex_res = calc.complex_calc(
    10,
    20,
    30
)
print("Complex result:", complex_res)
