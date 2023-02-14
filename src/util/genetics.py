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
    def random_float(min: int, max: int):
        return np.random.rand() * (max-min) + min

    @staticmethod
    def random_select(param: str, a: Individual, b: Individual, prob_a=0.5):
        param_a = getattr(a, param)
        param_b = getattr(b, param)
        if (np.random.rand() < prob_a):
            return param_a
        return param_b

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
    def mutate_float(val: int, prob, amp, prob_reset, range):
        if (np.random.rand() < prob_reset):
            return Genetics.random_float(*range)
        if (np.random.rand() < prob):
            val += (np.random.rand()*2-1)*amp
            if (val < range[0]):
                val = range[0]
            if (val > range[1]):
                val = range[1]
        return val