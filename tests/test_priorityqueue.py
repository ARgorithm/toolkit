import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
queue = ARgorithmToolkit.PriorityQueue("pq",algo)

def test_declare():
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_declare"

def test_operations():
    
    queue.offer(9)
    queue.offer(3)
    queue.offer(7)
    assert queue.body[0] == 3
   
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_offer"
    
    assert queue.peek() == 3
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_peek"

    assert queue.peek() == queue.poll()
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_poll"
    queue.poll()
    assert queue.body == [9]
    queue.poll()
    try:
        queue.poll()
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_size():
    assert queue.empty() and len(queue)==0

    
