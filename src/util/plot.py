import numpy as np
import matplotlib.pyplot as plt
from src.nsga2 import NSGA2

"""
    Utility class for plotting fitnesses. 
"""
class Plot:

    @staticmethod
    def _gen_results2d(gen):
        x = [r[0] for r in gen.fitnesses.values()]
        y = [r[1] for r in gen.fitnesses.values()]
        plt.scatter(x, y, s=5)

    """
        Plot all generations fitnesses.
    """
    @staticmethod
    def fitnesses(nsga2: NSGA2):
        dims = nsga2.get_fitness_dims()
        if (dims == 0):
            raise Exception('No generation found. Did you train it?')
        if (dims > 3):
            raise Exception('Hyperdimensional plots currently not supported. Fitnesses must have up to 3 variables to be plotted.')
        if (dims == 2):
            for gen in nsga2.generations:
                Plot._gen_results2d(gen)
        plt.show()