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
