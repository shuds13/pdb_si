import pdb_si
from calculator import Calculator

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
