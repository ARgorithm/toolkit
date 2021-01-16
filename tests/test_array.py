"""Testing Array
"""
import numpy as np
import ARgorithmToolkit
algo = ARgorithmToolkit.StateSet()
test_data = [[1,2,3],[4,5,6]]
arr = ARgorithmToolkit.Array(name='arr',algo=algo,data=test_data)

def test_body():
    """Test array contents
    """
    assert np.all(arr.body == test_data)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_declare'
    assert np.all(last_state.content["state_def"]["body"] == arr.body)


def test_indexing():
    """Test array indexing
    """
    assert arr[1].tolist() == list(arr.body[1])
    last_state = algo.states[-2]

    assert last_state.content["state_type"] == 'array_iter'
    assert last_state.content["state_def"]["index"] == 1

    assert arr[1,1] == arr.body[1,1]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_iter'
    assert last_state.content["state_def"]["index"] == (1,1)

    assert arr[1][2].tolist() == arr.body[1][2]
    last_state = algo.states[-1]
    second_last_state = algo.states[-2]
    assert second_last_state.content["state_type"] == 'array_declare'
    assert last_state.content["state_type"] == 'array_iter'
    assert last_state.content["state_def"]["index"] == 2

    subarr = arr[1]
    assert isinstance(subarr,ARgorithmToolkit.Array)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_declare'
    assert last_state.content["state_def"]["variable_name"] == 'arr_sub'
    assert np.all(last_state.content["state_def"]["body"] == arr.body[1])

    subarr = arr[1:2]
    assert isinstance(subarr,ARgorithmToolkit.Array)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_declare'
    assert last_state.content["state_def"]["variable_name"] == 'arr_sub'
    assert np.all(last_state.content["state_def"]["body"] == arr.body[1:2])


def test_iteration():
    """Test Array iteration
    """
    for i in range(2):
        for j in range(2):
            arr[i,j] = arr[j,i]
            last_state = algo.states[-1]
            assert last_state.content["state_type"] == 'array_iter'
            assert last_state.content["state_def"]["index"] == (i,j)

    for i in range(2):
        for j in range(3):
            assert arr[i,j] == arr.body[i,j]
            last_state = algo.states[-1]
            assert last_state.content["state_type"] == 'array_iter'
            assert last_state.content["state_def"]["index"] == (i,j)

def test_compare():
    """Test Array compare
    """
    func = lambda x,y : x+2 > y/2
    elemA = arr[0,1]
    elemB = arr[1,1]

    assert arr[0,1]-arr[1,1] == arr.compare((0,1),(1,1))
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_compare'
    assert last_state.content["state_def"]["index1"] == (0,1)
    assert last_state.content["state_def"]["index2"] == (1,1)

    assert func(elemA,elemB) == arr.compare((0,1),(1,1),func)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_compare'
    assert last_state.content["state_def"]["index1"] == (0,1)
    assert last_state.content["state_def"]["index2"] == (1,1)


def test_swap():
    """Test array swap
    """
    elemA = arr[0,2]
    elemB = arr[1,2]
    arr.swap((0,2),(1,2))
    last_state = algo.states[-1]
    assert elemA == arr[1,2] and elemB == arr[0,2]
    assert last_state.content["state_type"] == 'array_swap'
    assert last_state.content["state_def"]["index1"] == (0,2)
    assert last_state.content["state_def"]["index2"] == (1,2)
    assert np.all(last_state.content["state_def"]["body"] == arr.body)

def test_dimension_check():
    """Test array dimension check
    """
    assert isinstance(arr[1],ARgorithmToolkit.Array)
    last_state = algo.states[-1]
    second_last_state = algo.states[-2]
    assert last_state.content["state_type"] == 'array_declare'
    assert second_last_state.content["state_type"] == 'array_iter'
    assert second_last_state.content["state_def"]["index"] == 1
    try:
        ARgorithmToolkit.Array(name='arr',algo=algo,data=[[1,2],[3],[4,5]])
        assert False
    except ARgorithmToolkit.ARgorithmError:
        pass
