import sys
sys.path.append('.')

import numpy as np
import matplotlib.pyplot as plt

from src.nsga2 import Individual, NSGA2
from src.util.genetics import Genetics
from src.util.plot import Plot
from src.util.log import Log


"""
    [nsga2-py] "2D Cluster" Example

    This is a barebones example of how to optimize two variables
    using nsga2-py with a custom fitness function.

    The challenge is:
        - Given a 100x100 field with 500 points
        - Each point has an (x,y) coordinate, mass and monetary value
        - You must pick a circular area with radius in [1,20]
        - This area should have the greatest monetary value with the lowest mass
"""


"""
    A circle is an individual solution for the problem.
"""
class Circle(Individual):

    def _init_random(self):
        self.x = Genetics.random_int(0, 200)
        self.y = Genetics.random_int(0, 200)
        self.r = Genetics.random_float(1, 20)

    def _init_from_parents(self, a, b):
        self.x = Genetics.random_select('x', a, b)
        self.y = Genetics.random_select('y', a, b)
        self.r = Genetics.random_select('r', a, b)

    def mutate(self):
        self.x = Genetics.mutate_int(self.x, 0.1, 5, 0.01, (0,200))
        self.y = Genetics.mutate_int(self.y, 0.1, 5, 0.01, (0,200))
        self.r = Genetics.mutate_float(self.r, 0.1, 0.1, 0.01, (1,20))

    def fitness(self):
        mass = 0
        value = 0
        for p in self.field.points:
            dist = np.sqrt((p[0] - self.x) ** 2 + (p[1] - self.y) ** 2)
            if (dist < self.r):
                mass += p[2]
                value += p[3]
        return (-mass, value)

    def plot(self, ax):
        patch = plt.Circle((self.x, self.y), self.r, color='r', lw=0.5, fill=False)
        ax.add_patch(patch)


"""
    The field of points which will be used for training.
"""
class Field:

    def __init__(self, n, range, depth=2):
        self.points = np.random.randint(range[0], range[1], size=(n, 2+depth))

    def plot(self, nsga2):
        fig, ax = plt.subplots()

        scatter = ax.scatter(
            self.points[:,0],
            self.points[:,1],
            c=self.points[:,2],
            s=self.points[:,3],
            cmap='summer'
        )
        cbar = fig.colorbar(scatter)

        for circle in nsga2.population.values():
            circle.plot(ax)

        plt.show()


"""
    Training routine.
"""
def main():
    Log.setup('example/2d_cluster.log')
    field = Field(500, (0, 100))
    
    nsga2 = NSGA2(Circle, 100, field=field)
    nsga2.train(epochs=100)

    field.plot(nsga2)
    Plot.fitnesses(nsga2)

if __name__ == "__main__":
    main()
