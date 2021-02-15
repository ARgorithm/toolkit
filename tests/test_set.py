"""Test module for ARgorithmToolkit.Set"""

import ARgorithmToolkit
from tests.utils import last_state

algo = ARgorithmToolkit.StateSet()

def test_init():
    """test set declaration"""
    l = [1,2,3]
    t = (1,2,3)
    vec = ARgorithmToolkit.Vector('vec',algo,[1,2,3])
    arr = ARgorithmToolkit.Array('vec',algo,[1,2,3])

    myset = ARgorithmToolkit.Set('myset',algo)
    myset = ARgorithmToolkit.Set('myset',algo,l)
    myset = ARgorithmToolkit.Set('myset',algo,t)
    myset = ARgorithmToolkit.Set('myset',algo,arr)
    myset = ARgorithmToolkit.Set('myset',algo,vec)

    state = last_state(algo)
    assert state['state_type'] == "set_declare"
    assert myset.body == set([1,2,3])

def test_add_remove_find():
    """test internal set operations such as add,find,remove"""
    myset = ARgorithmToolkit.Set('myset',algo)
    myset.add(3)
    myset.add(3)
    myset.add(3.14)
    myset.add('abc')
    myset.add(True)

    assert myset.body == set([3,3.14,'abc',True])

    st = ARgorithmToolkit.String("mystr",algo,"hello")
    myset.add(st,"adding an ARgorithmToolkit.String")
    try:
        myset.add(algo)
        assert False
    except TypeError:
        pass

    state = last_state(algo)
    assert state['state_type'] == "set_add"
    assert state['comments'] == "adding an ARgorithmToolkit.String"

    myset.remove(3,comments="remove 3")
    myset.remove(st,comments="remove ARgorithmToolkit.String object")
    try:
        myset.remove(4)
        assert False
    except ARgorithmToolkit.ARgorithmError:
        pass

    assert myset.body == set([3.14,'abc',True])

    state = last_state(algo)
    assert state['state_type'] == "set_remove"
    assert state['comments'] == "remove ARgorithmToolkit.String object"

    assert myset.find(3.14)
    assert not myset.find(3)

    state = last_state(algo)
    assert state['state_type'] == "set_find"

def test_union_intersection_difference():
    """test operations between sets"""
    set1 = ARgorithmToolkit.Set('set1',algo,[1,2,3])
    set2 = ARgorithmToolkit.Set('set1',algo,[2,4,5])

    union_set = set1.union(set2)
    diff_set = set1.difference(set2)
    inter_set = set1.intersection(set2)
    assert union_set.body == set([1,2,3,4,5])
    assert diff_set.body == set([1,3])
    assert inter_set.body == set([2])

    state = last_state(algo)
    assert state["state_type"] == "set_declare"
    state = last_state(algo)
    assert state["state_type"] == "set_declare"
    state = last_state(algo)
    assert state["state_type"] == "set_declare"
