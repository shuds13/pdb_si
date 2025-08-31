import pdb_si
from func2 import target_func2


class BaseBaseBaseCalculator():
    def __init__(self, name, version="0.0"):
        print(f"BaseBaseBaseCalculator initialized: {name} v{version}")
    
    def calculate(self, a, b, c, d, e=0, f=1):
        pass

class BaseBaseCalculator(BaseBaseBaseCalculator):
    def __init__(self, name, version="0.0"):
        super().__init__(name, version)
        print(f"BaseBaseCalculator initialized: {name} v{version}")
    
    def calculate(self, a, b, c, d, e=0, f=1):
        pass

class BaseCalculator(BaseBaseCalculator):
    def __init__(self, name, version="1.0"):
        super().__init__(name, version)
        self.name = name
        self.version = version
        print(f"BaseCalculator initialized: {name} v{version}")
    
    def calculate(self, a, b, c, d, e=0, f=1):
        print("BaseCalculator.calculate called")
        s1 = a + b
        s2 = c + d
        s3 = e + f
        return s1 + s2 + s3  # Simple addition

class Calculator(BaseCalculator):
    def __init__(self, name):
        ''' on line docstring'''
        """
        more docsring
        
        """

        # Check can si into super() call
        super().__init__(name, "2.0")
        self.operations_count = 0
    
    def calculate(self, a, b, c, d, e=0, f=1):
        # Test super() call to parent's calculate method
        base_result = super().calculate(a, b, c, d, e, f)
        self.operations_count += 1
        # Child version does multiplication instead of addition
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
