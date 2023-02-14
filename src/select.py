from __future__ import annotations


"""
    Selects n best ids from a given front.
"""
def select_n_best_of_front(front:{int|str:[float]}, n:int):
    if (n <= 2):
        return list(front.keys())[:n]

    objectives = len(list(front.values())[0])
    dist = { id: 0 for id in front }

    for o in range(objectives):
        el = sorted([(id,v[o]) for id, v in front.items()], key= lambda v: v[1])
        dist[el[0][0]] = float('inf')
        dist[el[-1][0]] = float('inf')
        scale = (el[-1][1] - el[0][1])
        for i in range(1, len(front)-1):
            dist[el[i][0]] += (el[i+1][1]-el[i-1][1])/scale

    best = sorted([(id, d) for id, d in dist.items()], key= lambda v: -v[1])
    return [b[0] for b in best[:n]]
    

"""
    Selects n best ids from a given list of fronts.
"""
def select_n_best(fronts:[{int|str:[float]}], n:int):

    best = []
    for front in fronts:
        if len(best) + len(front) <= n:
            best += [id for id in front]
        else:
            best += select_n_best_of_front(front, n - len(best))
        if (len(best) == n):
            break
    
    return best