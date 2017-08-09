import math

class EquationGenerator:
    def __init__(self, data, velocity):

        self.data = data
        self.result = 0.0
        self.a = float(self.data["a"])
        self.b = float(self.data["b"])
        self.c = float(self.data["c"])
        self.d = float(self.data["d"])
        self.e = float(self.data["e"])
        self.f = float(self.data["f"])
        self.g = float(self.data["a"])
        self.R2 = float(self.data["R2"])
        self.vmin = int(self.data["Vmin"])
        self.vmax = int(self.data["Vmax"])
        self.function_id = int(self.data["Function_ID"])
        self.velocity = velocity

        self.calculate(self.function_id)

    def calculate(self, model):

        # 1: ((a * (b ^ x)) * (x ^ c))
        # 2: ((a * (x ^ b)) + (c * (x ^ d)))
        # 3: ((a + (b * x)) ^ ((-1) / c))
        # 4: ((a + (b * x)) + (((c - b) * (1 - exp(((-1) * d) * x))) / d))
        # 5: ((e + (a * exp(((-1) * b) * x))) + (c * exp(((-1) * d) * x)))
        # 6: (1 / (((c * (x ^ 2)) + (b * x)) + a))
        # 7: (1 / (a + (b * (x ^ c))))
        # 8: (1 / (a + (b * x)))
        # 9: (a-(b*exp(((-1)*c)*(x^d))))
        # 10: a / (1 + (b * exp(((-1) * c) * x)))
        # 11: (a + (b / (1 + exp((((-1) * c) + (d * ln(x))) + (e * x)))))
        # 12: (c + (a * exp(((-1) * b) * x)))
        # 13: (c + (a * exp(b * x)))
        # 14: exp((a+(b/x))+(c*ln(x)))
        # 15: (((a * (x ^ 3)) + (b * (x ^ 2)) + (c * x)) + d)
        # 16: (((a * (x ^ 2)) + (b * x)) + c)

        equation_dict = {0: lambda a,b,c,d,e,f,vel: ((a * (b ** vel)) * (vel ** c)),
                        1: lambda a,b,c,d,e,f,vel: ((a * (vel ** b)) + (c * (vel ** d))),
                        2: lambda a,b,c,d,e,f,vel: ((a + (b * vel)) ** ((-1) / c)),
                        3: lambda a,b,c,d,e,f,vel: ((a + (b * vel)) + (((c - b) * (1 - math.exp(((-1) * d) * vel))) / d)),
                        4: lambda a,b,c,d,e,f,vel: ((e + (a * math.exp(((-1) * b) * vel))) + (c * math.exp(((-1) * d) * vel))),
                        5: lambda a,b,c,d,e,f,vel: (1 / (((c * (vel ** 2)) + (b * vel)) + a)),
                        6: lambda a,b,c,d,e,f,vel: (1 / (a + (b * (vel ** c)))),
                        7: lambda a,b,c,d,e,f,vel: (1 / (a + (b * vel))),
                        8: lambda a,b,c,d,e,f,vel: a - (b * math.exp(((-1) * c) * (vel ** d))),
                        9: lambda a,b,c,d,e,f,vel: a / (1 + (b * math.exp(((-1) * c) * vel))),
                        10: lambda a,b,c,d,e,f,vel: (a + (b / (1 + math.exp((((-1) * c) + (d * math.log(vel))) + (e * vel))))),
                        11: lambda a,b,c,d,e,f,vel: (c + (a * math.exp(((-1) * b) * vel))),
                        12: lambda a,b,c,d,e,f,vel: (c + (a * math.exp(b * vel))),
                        13: lambda a,b,c,d,e,f,vel: math.exp((a + (b / vel)) + c * math.log(vel)),
                        14: lambda a,b,c,d,e,f,vel: (((a * (vel ** 3)) + (b * (vel ** 2)) + (c * vel)) + d),
                        15: lambda a,b,c,d,e,f,vel: (((a * (vel ** 2)) + (b * vel)) + c),
                        -1: lambda a,b,c,d,e,f,vel: 0.0
                        }

        self.result = equation_dict[model](self.a, self.b, self.c, self.d, self.e, self.f, self.velocity)

    def get_result(self):
        return self.result