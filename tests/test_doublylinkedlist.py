"""Testing Doubly linked list
"""
import ARgorithmToolkit
from .utils import last_state
algo = ARgorithmToolkit.StateSet()

def test_node():
    """Test Doubly linked list node
    """
    dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
    assert dllnode._value == 7
    assert dllnode._next is None
    assert dllnode._prev is None
    assert last_state(algo).state_type == "dllnode_declare"

    dllnode.value = 5
    assert dllnode._value == 5
    assert dllnode._next is None
    assert dllnode._prev is None
    assert last_state(algo).state_type == "dllnode_iter"


    temp = ARgorithmToolkit.DoublyLinkedListNode(algo,3)
    dllnode.prev = temp

    assert isinstance(dllnode._prev,ARgorithmToolkit.DoublyLinkedListNode)
    assert dllnode._next is None
    assert dllnode._prev == temp
    assert last_state(algo).state_type == "dllnode_prev"

    dllnode._prev = None
    del temp
    assert dllnode._next is None
    assert last_state(algo).state_type == "dllnode_delete"
