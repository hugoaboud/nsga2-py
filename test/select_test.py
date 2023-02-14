import pytest
from src.select import select_n_best, select_n_best_of_front

@pytest.mark.parametrize('given_front, expected_best', [
    (
        {'id0':[1,2,3],'id1':[1,2,3]},
        ['id0']
    ),
    (
        {'id0':[1,2,3],'id1':[1,2,3]},
        ['id0','id1']
    ),
    (
        {'id0':[1,1,5],'id1':[3,1,5],'id2':[5,1,1],'id3':[5,3,5],'id4':[5,5,5]},
        ['id0','id2','id4','id1']
    ),
])
def test_select_n_best_of_front(given_front, expected_best):
    # given
    n = len(expected_best)

    # when
    best = select_n_best_of_front(given_front,n)

    # then
    assert best == expected_best


@pytest.mark.parametrize('given_fronts, expected_best', [
    (
        [{'id0':[1,2,3]},{'id1':[1,2,3]}],
        ['id0']
    ),
    (
        [{'id0':[1,2,3]},{'id1':[1,2,3]}],
        ['id0','id1']
    ),
    (
        [{'id0':[1,1,5],'id1':[3,1,5],'id2':[5,1,1],'id3':[5,3,5],'id4':[5,5,5]},{'id5':[3,3,3], 'id6':[3,1,1], 'id7': [1,3,1], 'id8': [1,1,3]}],
        ['id0','id2','id4','id1']
    ),
    (
        [{'id0':[1,1,5],'id1':[3,1,5],'id2':[5,1,1],'id3':[5,3,5],'id4':[5,5,5]},{'id5':[1,3,1], 'id6':[1,1,3], 'id7': [3,1,1], 'id8': [3,3,3]}],
        ['id0','id1','id2','id3','id4','id5','id6','id8']
    )
])
def test_select_n_best(given_fronts, expected_best):
    # given
    n = len(expected_best)

    # when
    best = select_n_best(given_fronts,n)

    # then
    assert best == expected_best
