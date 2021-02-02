"""Testing Doubly linked list
"""
import ARgorithmToolkit
from .utils import last_state
algo = ARgorithmToolkit.StateSet()

def test_node():
    """Test Doubly linked list node
    """
    dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
    assert dllnode.value == 7
    assert dllnode.next is None
    assert dllnode.prev is None
    assert last_state(algo)['state_type'] == "dllnode_declare"

    dllnode.value = 5
    assert dllnode.value == 5
    assert dllnode.next is None
    assert dllnode.prev is None
    assert last_state(algo)['state_type'] == "dllnode_iter"


    temp = ARgorithmToolkit.DoublyLinkedListNode(algo,3)
    dllnode.prev = temp

    assert isinstance(dllnode.prev,ARgorithmToolkit.DoublyLinkedListNode)
    assert dllnode.next is None
    assert dllnode.prev == temp
    assert last_state(algo)['state_type'] == "dllnode_prev"

    dllnode.prev = None
    del temp
    assert dllnode.next is None
    assert last_state(algo)['state_type'] == "dllnode_delete"

def test_ll():
    """Test doubly linked list
    """
    dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
    dll = ARgorithmToolkit.DoublyLinkedList("dllnode",algo,dllnode)

    assert dll.head == dllnode
    assert dll.tail == dllnode
    assert last_state(algo)['state_type'] == "dll_declare"

    temp = ARgorithmToolkit.DoublyLinkedListNode(algo,3)
    dll.head = temp

    assert dll.head == temp
    assert dll.tail == dllnode
    assert last_state(algo)['state_type'] == "dll_head"

def test_list():
    """Test List class
    """
    dl = ARgorithmToolkit.List("dl",algo)
    assert last_state(algo)['state_type'] == "dll_declare"

    dl.push_front(4)
    assert len(dl) == 1
    assert isinstance(dl.head,ARgorithmToolkit.DoublyLinkedListNode)
    assert last_state(algo)['state_type'] == "dll_tail"
    assert last_state(algo)['state_type'] == "dll_head"
    assert last_state(algo)['state_type'] == "dllnode_declare"

    dl.push_front(3)
    assert last_state(algo)['state_type'] == "dll_head"
    assert last_state(algo)['state_type'] == "dllnode_prev"
    assert last_state(algo)['state_type'] == "dllnode_next"
    assert last_state(algo)['state_type'] == "dllnode_declare"

    dl.push_back(5)
    assert last_state(algo)['state_type'] == "dll_tail"
    assert last_state(algo)['state_type'] == "dllnode_next"
    assert last_state(algo)['state_type'] == "dllnode_prev"
    assert last_state(algo)['state_type'] == "dllnode_declare"

    dl.insert(5,2)
    assert last_state(algo)['state_type'] == "dllnode_next"
    assert last_state(algo)['state_type'] == "dllnode_prev"
    assert last_state(algo)['state_type'] == "dllnode_prev"
    assert last_state(algo)['state_type'] == "dllnode_next"
    assert last_state(algo)['state_type'] == "dllnode_declare"

    assert dl.tolist() == [3,4,5,5]

    dl.remove(5)
    assert dl.tolist() == [3,4]
    assert dl.head.value == 3
    assert dl.tail.value == 4
    assert last_state(algo)['state_type'] == "dllnode_delete"

    k = dl.pop_back()
    assert k == 4
    assert dl.tolist() == [3]
    assert last_state(algo)['state_type'] == "dllnode_delete"
    assert last_state(algo)['state_type'] == "dllnode_next"

    k = dl.pop_front()
    assert k == 3
    assert len(dl) == 0
    assert dl.tail is None
    assert last_state(algo)['state_type'] == "dll_tail"
    assert last_state(algo)['state_type'] == "dllnode_delete"
    assert last_state(algo)['state_type'] == "dll_head"

    dl.push_front(3)
    dl.push_back(4)

    k = dl.pop_front()
    assert k == 3
    assert last_state(algo)['state_type'] == "dllnode_delete"
    assert last_state(algo)['state_type'] == "dllnode_prev"
    assert last_state(algo)['state_type'] == "dll_head"

    k = dl.pop_back()
    assert k == 4
    assert last_state(algo)['state_type'] == "dll_head"
    assert last_state(algo)['state_type'] == "dllnode_delete"
    assert last_state(algo)['state_type'] == "dll_tail"

    try:
        dl.pop_front()
        raise AssertionError("Error not raised")
    except ARgorithmToolkit.ARgorithmError:
        pass
