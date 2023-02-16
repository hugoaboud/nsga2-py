import numpy as np
from src.nsga2 import Individual


"""
    Util class for randomizing parameters.
"""
class Genetics:

    @staticmethod
    def random_int(min: int, max: int):
        return np.random.randint(min, max)

    @staticmethod
    def random_int_list(ranges: [(int,int)]):        
        return [Genetics.random_int(min, max) for min, max in ranges]

    @staticmethod
    def random_float(min: int, max: int):
        return np.random.rand() * (max-min) + min
    
    @staticmethod
    def random_int_list(ranges: [(int,int)]):        
        return [Genetics.random_int(min, max) for min, max in ranges]

    @staticmethod
    def random_float_list(ranges: [(int,int)]):        
        return [Genetics.random_float(min, max) for min, max in ranges]

    @staticmethod
    def crossover(param: str, a, b, prob_a=0.5):
        if (isinstance(a, list)):
            param_a = a[param]
        else:
            param_a = getattr(a, param)
        if (isinstance(b, list)):
            param_b = b[param]
        else:
            param_b = getattr(b, param)
        if (np.random.rand() < prob_a):
            return param_a
        return param_b
    
    @staticmethod
    def crossover_list(param: str, a, b, prob_a=0.5):
        if (isinstance(a, list)):
            param_a = a[param]
        else:
            param_a = getattr(a, param)
        if (isinstance(b, list)):
            param_b = b[param]
        else:
            param_b = getattr(b, param)
        return [Genetics.crossover(p, param_a, param_b, prob_a=prob_a) for p in range(len(param_a))]

    @staticmethod
    def mutate_int(val: int, prob, amp, prob_reset, range):
        if (np.random.rand() < prob_reset):
            return Genetics.random_int(*range)
        if (np.random.rand() < prob):
            val += np.random.randint(-amp,amp)
            if (val < range[0]):
                val = range[0]
            if (val > range[1]):
                val = range[1]
        return val

    @staticmethod
    def mutate_int_list(params: [(int)]):
        return [Genetics.mutate_int(*param) for param in params]

    @staticmethod
    def mutate_float(val: float, prob: float, amp: float, prob_reset: float, range: float):
        if (np.random.rand() < prob_reset):
            return Genetics.random_float(*range)
        if (np.random.rand() < prob):
            val += (np.random.rand()*2-1)*amp
            if (val < range[0]):
                val = range[0]
            if (val > range[1]):
                val = range[1]
        return val

    @staticmethod
    def mutate_float_list(params: [(float)]):
        return [Genetics.mutate_float(*param) for param in params]