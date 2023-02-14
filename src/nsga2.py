import logging
import numpy as np
import uuid
from tqdm import tqdm
from typing import Type
from src.select import select_n_best
from src.sort import non_dominated_sort


"""
    An individual of the Genetic Algorithm.
    It contains mutable parameters and should be able to 
    be initialized from two parents.
    It should also calculate a fitness for such parameters
    to be maximized, which consists of a list of numbers.
"""
class Individual:

    def __init__(self, parents = None, **kwargs):
        self.id = NSGA2._new_id()
        self.parents = parents
        for name, val in kwargs.items():
            setattr(self, name, val)
        if (parents):
            self._init_from_parents(*parents)
        else:
            self._init_random()

    def _init_random(self):
        raise NotImplementedError()

    def _init_from_parents(self, a, b):
        raise NotImplementedError()

    def mutate(self):
        raise NotImplementedError()

    def fitness(self):
        raise NotImplementedError()


"""
    A set of individuals and fitnesses of an epoch.
"""
class Generation:
    
    def __init__(self, population, fitnesses):
        self.id = NSGA2._new_id()
        self.population = population
        self.fitnesses = fitnesses

    def get_fitness_dims(self):
        return len(list(self.fitnesses.values())[0])

    def report(self):
        dims = self.get_fitness_dims()
        n = len(self.fitnesses)
        
        fits = [[f[d] for f in self.fitnesses.values()] for d in range(dims)]
        max_fits = [np.max(fit_d) for fit_d in fits]
        avg_fits = [np.average(fit_d) for fit_d in fits]

        logging.info(f'Generation {self.id}:')
        logging.info(f'\tmax fitness: {max_fits}')
        logging.info(f'\tavg fitness: {avg_fits}')


"""
    Non-Sorting Genetic Algorithm II
    Optimizes parameters for multi-objective problems.
"""
class NSGA2:

    @staticmethod
    def _new_id():
        return str(uuid.uuid4())[:8]

    def __init__(self, individual_class: Type[Individual], pop_size: int = 100, **kwargs):
        self.individual_class = individual_class
        self.individual_kwargs = kwargs
        self.population = {}
        self.generations = []
        self._populate(pop_size)

    def _populate(self, n: int):
        for _ in range(n):
            ind = self.individual_class(**self.individual_kwargs)
            self.population[ind.id] = ind
    
    def _select_best_individuals(self, fitnesses):
        if (len(self.generations) == 0):
            return self.population.values()

        all_fitnesses = {**self.generations[-1].fitnesses, **fitnesses}
        all_individuals = {**self.generations[-1].population, **self.population}

        fronts = non_dominated_sort(all_fitnesses)
        best = select_n_best(fronts, len(self.population))
        
        return [ind for id, ind in all_individuals.items() if id in best]

    def _save_generation(self, fitnesses):
        generation = Generation(self.population, fitnesses)
        generation.report()
        self.generations.append(generation)

    def _make_offspring(self, parents):
        parents_a = list(parents)
        parents_b = list(parents)
        np.random.shuffle(parents_a)
        np.random.shuffle(parents_b)
        offspring = {}
        for a, b in zip(parents_a, parents_b):
            newborn = self.individual_class(parents=(a,b), **self.individual_kwargs)
            newborn.mutate()
            offspring[newborn.id] = newborn
        return offspring

    def _epoch(self, epoch):
        fitnesses = { id: ind.fitness() for id, ind in tqdm(list(self.population.items())) }
        parents = self._select_best_individuals(fitnesses)
        self._save_generation(fitnesses)
        self.population = self._make_offspring(parents)

    def train(self, epochs: int):  
        for epoch in range(1,epochs+1):
            logging.info(f'Epoch {epoch}/{epochs}')
            self._epoch(epoch)

    def get_fitness_dims(self):
        if (len(self.generations) == 0):
            return None
        return self.generations[0].get_fitness_dims()
