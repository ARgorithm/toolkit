"""Test queue
"""
import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
queue = ARgorithmToolkit.Queue("q",algo)

def test_declare():
    """Test queue creation
    """
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_declare"

def test_operations():
    """Test queue operations
    """
    queue.push(3)
    queue.push(9)
    assert queue.body == [3,9]

    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_push"
    assert last_state.content["state_def"]["body"] == queue.body
    assert last_state.content["state_def"]["element"] == 9

    assert queue.front() == 3
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_front"

    assert queue.back() == 9
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_back"

    assert queue.front() == queue.pop()
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "queue_pop"
    assert queue.body == [9]


    queue.pop()

    try:
        queue.pop()
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_size():
    """Test queue size
    """
    assert queue.empty() and len(queue)==0
