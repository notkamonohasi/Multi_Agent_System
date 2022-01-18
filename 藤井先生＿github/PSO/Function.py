import numpy as np
import math

# 最大値を求めたい関数。classと番号で管理しておくと、かなり一般化できて実装が楽
class Function : 
    def __init__(self, function_number) : 
        self.function_number = function_number

    def __call__(self, x) : 
        if self.function_number == 1 : 
            return sphere(x)
        elif self.function_number == 2 : 
            return rastrigin(x)
        elif self.function_number == 3 : 
            return rosenbrock(x)
        elif self.function_number == 4 : 
            return griewank(x)
        elif self.function_number == 5 : 
            return alpine(x)
        elif self.function_number == 6 : 
            return minima(x)
        else : 
            print()
            print("##############################################")
            print("FUNCTION_NUMBER_ERROR!!!")
            print()



def sphere(x) :
    ret = 0.0
    for i in range(x.size) : 
        ret += x[i] ** 2
    return ret


def rastrigin(x) : 
    ret = 10.0 * x.size
    for i in range(x.size) : 
        ret += (x[i] ** 2) - 10 * math.cos(2 * math.pi * x[i])
    return ret


def rosenbrock(x) : 
    ret = 0.0
    for i in range(x.size - 1) : 
        ret += 100 * ((x[i + 1] - (x[i] ** 2)) ** 2) + ((1 - x[i]) ** 2)
    return ret


def griewank(x) : 
    ret = 1.0
    for i in range(x.size) : 
        ret += (x[i] ** 2) / 4000
    memo = 1.0   # 積の部分
    for i in range(x.size) : 
        memo = memo * math.cos(x[i] / math.sqrt(i + 1))   # 「i+1」要注意ポイント
    ret += memo
    return ret


def alpine(x) : 
    ret = 0.0
    for i in range(x.size) : 
        ret += abs(x[i] * math.sin(x[i]) + 0.1 * x[i])
    return ret


def minima(x) : 
    ret = 0.0
    for i in range(x.size) : 
        ret += (x[i] ** 4 - 16 * (x[i] ** 2) + 5 * x[i])
    return ret

