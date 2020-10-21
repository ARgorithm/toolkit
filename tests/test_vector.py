import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
arr = ARgorithmToolkit.Vector('arr',algo,[1,2,3,5,2])

def test_body():
    assert arr.body == [1, 2, 3, 5, 2]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_declare'
    assert last_state.content["state_def"]["body"] == [1, 2, 3, 5, 2]

def test_insert_remove():
    arr.insert(12)
    assert arr.body == [1, 2, 3, 5, 2 , 12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_insert'
    assert last_state.content["state_def"]["element"] == 12
    assert last_state.content["state_def"]["index"] == 5
    
    arr.insert(12,1)
    assert arr.body == [1,12,2,3,5,2,12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_insert'
    assert last_state.content["state_def"]["element"] == 12
    assert last_state.content["state_def"]["index"] == 1
    

    arr.remove(12)
    assert arr.body == [1,2,3,5,2,12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_remove'
    assert last_state.content["state_def"]["index"] == 1
    
    arr.remove(index=1)
    assert arr.body == [1,3,5,2,12]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_remove'
    assert last_state.content["state_def"]["index"] == 1
    
    try:
        arr.remove(3,1)
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_indexing():
    assert arr[1] == arr.body[1]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_iter'
    assert last_state.content["state_def"]["index"] == 1
    
    subarr = arr[1:3]
    assert type(subarr) == type(arr)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_declare'
    assert last_state.content["state_def"]["variable_name"] == 'arr_sub'
    assert last_state.content["state_def"]["body"] == arr.body[1:3]
    

def test_iteration():
    for i,(a,b) in enumerate(zip(arr,arr.body)):
        assert a==b
        last_state = algo.states[-1]
        assert last_state.content["state_type"] == 'vector_iter'
        assert last_state.content["state_def"]["index"] == i
    

def test_compare():
    func = lambda x,y : x+2 > y/2
    elemA = arr[0]
    elemB = arr[1]
    
    assert (elemA==elemB) == arr.compare(0,1)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_compare'
    assert last_state.content["state_def"]["index1"] == 0
    assert last_state.content["state_def"]["index2"] == 1
    
    assert func(elemA,elemB) == arr.compare(0,1,func)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'vector_compare'
    assert last_state.content["state_def"]["index1"] == 0
    assert last_state.content["state_def"]["index2"] == 1
    

def test_swap():
    elemA = arr[0]
    elemB = arr[1]
    arr.swap(0,1)
    last_state = algo.states[-1]
    assert elemA == arr[1] and elemB == arr[0]
    assert last_state.content["state_type"] == 'vector_swap'
    assert last_state.content["state_def"]["index1"] == 0
    assert last_state.content["state_def"]["index2"] == 1
    assert last_state.content["state_def"]["body"] == arr.body
    