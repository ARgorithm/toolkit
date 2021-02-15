"""Test priority queue
"""
import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
queue = ARgorithmToolkit.PriorityQueue("pq",algo)
queue_object = ARgorithmToolkit.PriorityQueue("pq2",algo)

def test_declare():
    """Test priority queue creation
    """
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_declare"

def test_operations():
    """Test priority quque operations
    """
    queue.offer(9)
    queue.offer(3)
    queue.offer(7)
    class A:
        pass
    a = A()
    queue_object.offer((2, 'ABC'))
    queue_object.offer((1, {"A":1}))
    queue_object.offer((3, a))
    assert queue.body[0] == 3
    assert queue_object.body[0] == (1, {"A":1})

    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_offer"
    assert last_state.content["state_def"]["body"] == queue_object.body
    assert last_state.content["state_def"]["element"] == (3,a)

    assert queue.peek() == 3
    assert queue_object.peek() == (1, {"A":1})
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_peek"

    assert queue.peek() == queue.poll()
    assert queue_object.peek() == queue_object.poll()
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "priorityqueue_poll"
    queue.poll()
    queue_object.poll()
    assert queue.body == [9]
    assert queue_object.body == [(3, a)]
    queue.poll()
    queue_object.poll()
    try:
        queue.poll()
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_size():
    """Test priorityqueue size
    """
    assert queue.empty() and len(queue)==0
