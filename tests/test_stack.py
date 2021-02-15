"""Test stack
"""
import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
stack = ARgorithmToolkit.Stack("st",algo)

def test_declare():
    """Test stack creation
    """
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "stack_declare"

def test_operations():
    """Test stack operations
    """
    stack.push(3)
    stack.push(9)
    assert stack.body == [3,9]

    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "stack_push"
    assert last_state.content["state_def"]["body"] == stack.body
    assert last_state.content["state_def"]["element"] == 9

    assert stack.top() == 9
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "stack_top"

    assert stack.top() == stack.pop()
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == "stack_pop"
    assert stack.body == [3]

    stack.pop()
    try:
        stack.pop()
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_size():
    """Test size operations
    """
    assert stack.empty() and len(stack)==0
