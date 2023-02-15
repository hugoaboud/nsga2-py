# py-nsga2

NSGA-II stands for "Non Sorting Genetic Algorithm II", and it's a fast and elitist multiobjective GA.

This is a simple but very flexible implementation of the algorithm fundamentals.

## Setup

TODO: make it a pip package

## Usage

A complete example is available, you can run it with:
```
python3 example/2d_cluster.py
```

### Training individuals
```python
from nsga2 import Individual, NSGA2

class CustomIndividual(Individual):
    def _init_random(self):
        # ...
    def _init_from_parents(self, a, b):
        # ...
    def mutate(self):
        # ...
    def fitness(self):
        # ...

nsga2 = NSGA2(CustomIndividual, pop_size=100)
nsga2.train(epochs=100)
```

### Genetic Parameter Helpers
```python
from nsga2.util.genetics import Genetics

Genetics.random_int(0,100)
Genetics.random_float(0,100)
```
```python
from nsga2.util.genetics import Genetics

class Obj:
    def __init__(self, param):
        self.param = param

a = Obj(1)
b = Obj(2)

Genetics.random_select('param', a, b, prob_a=0.5)
```
```python
from nsga2.util.genetics import Genetics

val = 10
mutate_int(val, prob=0.3, amp=1, prob_reset=0.01, range=(0,20))
```
```python
from nsga2.util.genetics import Genetics

val = 12.34
mutate_float(val, prob=0.3, amp=1.0, prob_reset=0.01, range=(0,20))
```

### Log & Plot

```python
from nsga2.util.log import Log

Log.setup(logfile='experiment.log', level='INFO')

logging.debug('Some debug message...')
logging.info('Some info message...')
logging.warn('Some warn message...')
logging.error('Some error message...')
```
```python
from nsga2.util.plot import Plot

Plot.fitnesses(nsga2)
```

### Standalone Sorting

```python
from nsga2.sort import non_dominated_sort

data = {
    'id0': [1,2,3],
    'id1': [1,2,3],
    'id2': [1,2,3]
}

non_dominated_sort(data)

# [{'id0':[1,2,3]},{'id1':[1,2,3],'id2':[1,2,3]}]
```

### Selecting from fronts

```python
from nsga2.select import select_n_best_of_front

select_n_best_of_front(front)
```
```python
from nsga2.select import select_n_best

select_n_best(fronts)
```