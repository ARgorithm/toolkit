"""Testing linked list
"""
import ARgorithmToolkit
from .utils import last_state
algo = ARgorithmToolkit.StateSet()
fl = ARgorithmToolkit.ForwardList("fl",algo)

def test_node():
    """Testing linked list node
    """
    llnode = ARgorithmToolkit.LinkedListNode(algo,7)
    assert llnode.value == 7
    assert llnode.next is None
    assert last_state(algo)['state_type'] == "llnode_declare"

    llnode.value = 5
    assert llnode.value == 5
    assert llnode.next is None
    assert last_state(algo)['state_type'] == "llnode_iter"


    temp = ARgorithmToolkit.LinkedListNode(algo,3)
    llnode.next = temp

    assert isinstance(llnode.next,ARgorithmToolkit.LinkedListNode)
    assert llnode.next == temp
    assert last_state(algo)['state_type'] == "llnode_next"

    llnode.next = None
    del temp
    assert llnode.next is None
    assert last_state(algo)['state_type'] == "llnode_delete"

def test_ll():
    """Testing linked list class
    """
    llnode = ARgorithmToolkit.LinkedListNode(algo,7)
    ll = ARgorithmToolkit.LinkedList("llnode",algo,llnode)

    assert last_state(algo)['state_type'] == "ll_declare"

    temp = ARgorithmToolkit.LinkedListNode(algo,3)
    ll.head = temp

    assert last_state(algo)['state_type'] == "ll_head"

def test_forwardlist():
    """Testing forwardlist
    """
    fl = ARgorithmToolkit.ForwardList("fl",algo)
    assert last_state(algo)['state_type'] == "ll_declare"

    fl.push_front(4)
    assert len(fl) == 1
    assert isinstance(fl.head,ARgorithmToolkit.LinkedListNode)
    assert last_state(algo)['state_type'] == "ll_head"

    fl.push_front(3)
    assert fl.tolist() == [3,4]

    fl.insert(5,1)
    assert len(fl) == 3
    assert isinstance(fl.head,ARgorithmToolkit.LinkedListNode)
    assert last_state(algo)['state_type'] == "llnode_next"
    assert fl.tolist() == [3,5,4]

    k = fl.pop_front()
    assert k == 3
    assert len(fl) == 2
    assert last_state(algo)['state_type'] == "llnode_delete"

    for _ in range(5):
        fl.insert(9,2)

    assert fl.tolist() == [5,4,9,9,9,9,9]

    for _ in range(5):
        fl.push_front(9)

    fl.remove(9)
    assert fl.tolist() == [5,4]
    assert last_state(algo)['state_type'] == "llnode_delete"

    fl.remove(5)
    fl.pop_front()

    assert fl.tolist() == []
    assert len(fl) == 0
    assert last_state(algo)['state_type'] == "llnode_delete"

    try:
        fl.pop_front()
        raise AssertionError("Error not raised")
    except ARgorithmToolkit.ARgorithmError:
        pass
