from __future__ import annotations


"""
    Data structure that represents the result of an individual.
    Used by the `non_dominated_sort` for cleaner code.
"""
class Result:
    def __init__(self, values: [float]):
        self.values = values
        self.superiors = 0
        self.inferiors = []

    def __gt__(self, other):
        for a, b in zip(self.values, other.values):
            if a <= b: return False
        return True


"""
    Sorts a dict of multi-variate features (lists of numbers) into pareto-fronts (lists of dicts).
    Each pareto-front contains solutions that are equally dominant.
"""
def non_dominated_sort(dict:{int|str:[float]}):

    # Build data structure
    results = { id: Result(val) for id, val in dict.items() }   

    # Initial solution tree and first front
    fronts = [{}]
    for id_a, a in results.items():
        for id_b, b in results.items():
            if (id_a == id_b):
                continue
            if a > b:
                a.inferiors.append(id_b)
            elif b > a:
                a.superiors += 1
        if (a.superiors == 0):
            fronts[-1][id_a] = a

    # Subsequent fronts
    while(len(fronts[-1])):
        fronts.append({})
        for id_a, a in fronts[-2].items():
            for id_b in a.inferiors:
                b = results[id_b]
                b.superiors -= 1
                if (b.superiors == 0):
                    fronts[-1][id_b] = b

    # Rebuild values
    return [{ id: result.values for id, result in front.items() } for front in fronts[:-1]]
