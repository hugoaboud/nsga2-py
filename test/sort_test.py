import pytest
from src.sort import Solution, non_dominated_sort

@pytest.mark.parametrize('given_a, given_b, expected_dominates', [
    ((5,),(3,),True),
    ((3,),(5,),False),
    ((5,5),(3,3),True),
    ((5,3),(3,3),False),
    ((3,5),(3,3),False),
    ((3,3),(3,3),False),
    ((3,1),(3,3),False),
    ((1,3),(3,3),False),
    ((1,1),(3,3),False),
    ((7,5,3),(1,1,1),True)
])
def test_dominates(given_a, given_b, expected_dominates):
    # given
    sol_a = Solution(given_a)
    sol_b = Solution(given_b)

    # when
    dominates = sol_a > sol_b

    # then
    assert dominates == expected_dominates

@pytest.mark.parametrize('given_data', [
    {
        'id1': ((1,1,1), 2),
        'id2': ((1,1,3), 1),
        'id3': ((1,1,5), 0),
        'id4': ((1,3,1), 1),
        'id5': ((1,3,3), 1),
        'id6': ((1,3,5), 0),
        'id7': ((1,5,1), 0),
        'id8': ((1,5,3), 0),
        'id9': ((1,5,5), 0),
        'id10': ((3,1,1), 1),
        'id11': ((3,1,3), 1),
        'id12': ((3,1,5), 0),
        'id13': ((3,3,1), 1),
        'id14': ((3,3,3), 1),
        'id15': ((3,3,5), 0),
        'id16': ((3,5,1), 0),
        'id17': ((3,5,3), 0),
        'id18': ((3,5,5), 0),
        'id19': ((5,1,1), 0),
        'id20': ((5,1,3), 0),
        'id21': ((5,1,5), 0),
        'id22': ((5,3,1), 0),
        'id23': ((5,3,3), 0),
        'id24': ((5,3,5), 0),
        'id25': ((5,5,1), 0),
        'id26': ((5,5,3), 0),
        'id27': ((5,5,5), 0),
    }
])
def test_non_dominated_sort(given_data):
    # given
    data_dict = { id:v[0] for id, v in given_data.items() }
    data_fronts = { id:v[1] for id, v in given_data.items() }

    # when
    fronts = non_dominated_sort(data_dict)
    
    # then
    assert sum([len(front) for front in fronts]) == len(given_data)
    for id, f in data_fronts.items():
        assert id in fronts[f]