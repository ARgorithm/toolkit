import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
arr = ARgorithmToolkit.Array('arr',algo,[1,2,3,5,2])

def test_body():
    assert arr.body == [1, 2, 3, 5, 2]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_declare'

def test_insert_remove():
    arr.insert(12)
    assert arr.body == [1, 2, 3, 5, 2 , 12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_insert'
    
    arr.insert(12,1)
    assert arr.body == [1,12,2,3,5,2,12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_insert'
    

    arr.remove(12)
    assert arr.body == [1,2,3,5,2,12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_remove'
    
    arr.remove(index=1)
    assert arr.body == [1,3,5,2,12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_remove'
    
    try:
        arr.remove(3,1)
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_indexing():
    assert arr[1] == arr.body[1]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_iter'
    
    subarr = arr[1:3]
    assert type(subarr) == type(arr)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_declare'
    

def test_iteration():
    for a,b in zip(arr,arr.body):
        assert a==b
        last_state = algo.states[-1]
        assert last_state.content["state_type"] == 'array_iter'
    

def test_compare():
    func = lambda x,y : x+2 > y/2
    elemA = arr[0]
    elemB = arr[1]
    
    assert (elemA==elemB) == arr.compare(0,1)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_compare'
    
    assert func(elemA,elemB) == arr.compare(0,1,func)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'array_compare'
    

def test_swap():
    elemA = arr[0]
    elemB = arr[1]
    arr.swap(0,1)
    last_state = algo.states[-1]
    assert elemA == arr[1] and elemB == arr[0]
    assert last_state.content["state_type"] == 'array_swap'
    