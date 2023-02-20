import numpy as np
import uuid
import pickle
import os
import copy
from tqdm import tqdm
from typing import Type
from src.select import select_n_best
from src.sort import non_dominated_sort
from src.util.log import Log
from src.util.monitor.server import MonitorServer
from multiprocessing import Process, Queue


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
        self.parents = None
        for name, val in kwargs.items():
            setattr(self, name, val)
        if (parents):
            if (len(parents) == 2):
                self.parents = (parents[0].id, parents[1].id)
                self.crossover(*parents)
            else:
                self.parents = (parents[0].id)
                self._clone(parents[0], kwargs)
        else:
            self.create()

    def _clone(self, original, kwargs):
        for key, val in vars(original).items():
            if (key in kwargs): continue
            if (key == 'id'): continue
            if (key == 'parents'): continue
            if isinstance(val, list):
                setattr(self, key, list(val))
            else:
                setattr(self, key, val)
        self.id = NSGA2._new_id()

    def create(self):
        raise NotImplementedError()

    def crossover(self, a, b):
        raise NotImplementedError()

    def mutate(self):
        raise NotImplementedError()

    def fitness(self):
        raise NotImplementedError()


"""
    A set of individuals and fitnesses of an epoch.
"""
class Generation:
    
    def __init__(self, population, fitnesses, sorted_ids):
        self.id = NSGA2._new_id()
        self.population = population
        self.fitnesses = fitnesses
        self.sorted_ids = sorted_ids

    def get_fitness_dims(self):
        return len(list(self.fitnesses.values())[0])

    def report(self):
        dims = self.get_fitness_dims()
        n = len(self.fitnesses)
        
        fits = [[f[d] for f in self.fitnesses.values()] for d in range(dims)]
        max_fits = [np.max(fit_d) for fit_d in fits]
        avg_fits = [np.average(fit_d) for fit_d in fits]

        Log.logger.info(f'Generation {self.id}:')
        Log.logger.info(f'\tmax fitness: {max_fits}')
        Log.logger.info(f'\tavg fitness: {avg_fits}')
        Log.logger.info(f'\ttop 5:')
        for id in self.sorted_ids[:5]:
            Log.logger.info(f'\t\t{id}: {self.fitnesses[id]}')


"""
    Config object, used to tune training parameters.
"""
class NSGA2Config:
    def __init__(self,
        pop_size: int = 100,
        crossover_ratio = 0.7,
        gen_out_path: str = None,
        run_monitor_server = True
    ):
        self.pop_size = pop_size
        self.crossover_ratio = crossover_ratio
        self.gen_out_path = gen_out_path
        self.run_monitor_server = run_monitor_server


"""
    Non-Sorting Genetic Algorithm II
    Optimizes parameters for multi-objective problems.
"""
class NSGA2:

    @staticmethod
    def _new_id():
        return str(uuid.uuid4())[:8]

    def __init__(self, individual_class: Type[Individual], config = NSGA2Config(), **kwargs):
        self.individual_class = individual_class
        self.config = config
        self.individual_kwargs = kwargs
        self.population = {}
        self.generations = []
        if (self.config.run_monitor_server):
            self._run_monitor_server()

    def load(self, path):
        with open(path, 'rb') as file:
            last_generation = pickle.load(file)
        self.population = last_generation.population
        self.generations = [last_generation]

    def _run_monitor_server(self):
        self.monitor_queue = Queue()
        Process(target=MonitorServer.process, args=(self.monitor_queue,)).start()

    def _random_population(self, n: int):
        population = {}
        for _ in range(n):
            ind = self.individual_class(**self.individual_kwargs)
            population[ind.id] = ind
        return population
    
    def _get_fitness(self, population):
        items = tqdm(list(population.items()))
        fitnesses = {
            id: ind.fitness() for id, ind in items
        }
        return fitnesses

    def _select_best_ids(self, population, fitnesses):
        fronts = non_dominated_sort(fitnesses)
        sorted_ids = select_n_best(fronts, self.config.pop_size)
        return sorted_ids
    
    def _binary_tournament(self, parents, sorted_ids):
        sorted_ids = list(enumerate(sorted_ids))
        np.random.shuffle(sorted_ids)
        middle = len(sorted_ids)//2
        parents_a = sorted_ids[:middle]
        parents_b = sorted_ids[middle:2*middle]
        best_parents = []
        for a, b in zip(parents_a, parents_b):
            if (a[0] < b[0]):
                best_parents.append(parents[a[1]])
            else:
                best_parents.append(parents[b[1]])
        return best_parents
    
    def _crossover(self, best_parents):
        n_best = int(len(best_parents) * (1-self.config.crossover_ratio))
        children = {}
        for parent in best_parents[:n_best]:
            child = self.individual_class(parents=(parent,), **self.individual_kwargs)
            children[child.id] = child
        while (len(children) < self.config.pop_size):
            a, b = np.random.choice(best_parents, 2)
            child = self.individual_class(parents=(a,b), **self.individual_kwargs)
            children[child.id] = child
        return children

    def _mutate(self, population):
        for individual in population.values():
            individual.mutate()

    def _evolve(self, parents, sorted_ids):
        best_parents = self._binary_tournament(parents, sorted_ids)
        children = self._crossover(best_parents)
        self._mutate(children)
        return children

    def _save_gen(self, population, fitnesses, sorted_ids):
        generation = Generation(population, fitnesses, sorted_ids)
        generation.report()
        self.generations.append(generation)

        if (self.config.gen_out_path):
            filename = f'{generation.id}.gen'
            path = os.path.join(self.config.gen_out_path,filename)
            with open(path, 'wb') as file:
                pickle.dump(generation, file)

        if (self.config.run_monitor_server):
            dump = pickle.dumps(fitnesses)
            self.monitor_queue.put(dump)

    def train(self, epochs: int):
        # initial generation
        if (len(self.population) == 0):
            Log.logger.info(f'Epoch 0/{epochs}')

            population = self._random_population(self.config.pop_size)
            fitnesses = self._get_fitness(population)

            sorted_ids = self._select_best_ids(population, fitnesses)
            self._save_gen(population, fitnesses, sorted_ids)
            
            self.population = self._evolve(population, sorted_ids)

        # t-th generation
        for epoch in range(1,epochs+1):
            Log.logger.info(f'Epoch {epoch}/{epochs}')

            fitnesses = self._get_fitness(self.population)
            fitnesses = { **fitnesses, **self.generations[-1].fitnesses }
            population = { **self.population, **self.generations[-1].population }
    
            sorted_ids = self._select_best_ids(population, fitnesses)
            population = { id: ind for id, ind in population.items() if id in sorted_ids }
            fitnesses = { id: ind for id, ind in fitnesses.items() if id in sorted_ids }
            self._save_gen(population, fitnesses, sorted_ids)
            
            self.population = self._evolve(population, sorted_ids)

    def get_fitness_dims(self):
        if (len(self.generations) == 0):
            return None
        return self.generations[0].get_fitness_dims()
