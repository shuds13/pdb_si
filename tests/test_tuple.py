import pdb_si
from calculator import Calculator

print(f"\n*** Test with tuples - si should NOT work on tuple lines ***\n")
import pdb;pdb.set_trace()

# Test a static method or different class function - currently doesn't work
# test_result = Calculator.test_static_method(5, 10)

# This should NOT trigger si
my_tuple = (1, 2, 3, 4, 5)

# This should work with si (it's a function call)
calc = Calculator("TestCalc")
res = calc.calculate(
    10,
    20,
    30,
    40,
    e=50,
    f=60,
)

# Test a different class method call
complex_res = calc.complex_calc(
    100,
    200,
    300
)



print("Tuple:", my_tuple)
print("Result:", res)
print("Complex result:", complex_res)
print("Test result:", test_result)
