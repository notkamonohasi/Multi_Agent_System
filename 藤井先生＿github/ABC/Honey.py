import numpy as np
import random

class Honey : 
    def __init__(self, f, N, min_field, max_field, limit_harvest) : 
        self.f = f
        self.N = N
        self.min_field = min_field
        self.max_field = max_field
        self.limit_harvest = limit_harvest

        self.place = np.array([random.uniform(min_field, max_field) for _ in range(N)])
        self.score = f(self.place)
        self.count = 0