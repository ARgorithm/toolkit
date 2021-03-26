"""Testing linked list
"""
import ARgorithmToolkit
from .utils import last_state
algo = ARgorithmToolkit.StateSet()

def test_node():
    """Testing linked list node
    """
    llnode = ARgorithmToolkit.LinkedListNode(algo,7)
    assert llnode._value == 7
    assert llnode._next is None
    assert last_state(algo).state_type == "llnode_declare"

    llnode.value = 5
    assert llnode._value == 5
    assert llnode._next is None
    assert last_state(algo).state_type == "llnode_iter"


    temp = ARgorithmToolkit.LinkedListNode(algo,3)
    llnode.next = temp

    assert isinstance(llnode._next,ARgorithmToolkit.LinkedListNode)
    assert llnode._next == temp
    assert last_state(algo).state_type == "llnode_next"

    llnode.next = None
    del temp
    assert llnode._next is None
    assert last_state(algo).state_type == "llnode_delete"
