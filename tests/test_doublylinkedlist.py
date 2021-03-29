"""Testing Doubly linked list."""
from ARgorithmToolkit import DoublyLinkedList,DoublyLinkedListNode,StateSet
from .utils import last_state,check_states
algo = StateSet()

def test_node():
    """Test Doubly linked list node."""
    dllnode = DoublyLinkedListNode(algo,7)
    assert dllnode._value == 7
    assert dllnode._next is None
    assert dllnode._prev is None
    assert last_state(algo).state_type == "dllnode_declare"

    dllnode.value = 5
    assert dllnode._value == 5
    assert dllnode._next is None
    assert dllnode._prev is None
    assert last_state(algo).state_type == "dllnode_iter"


    temp = DoublyLinkedListNode(algo,3)
    dllnode.prev = temp

    assert isinstance(dllnode._prev,DoublyLinkedListNode)
    assert dllnode._next is None
    assert dllnode._prev == temp
    assert last_state(algo).state_type == "dllnode_prev"

    dllnode._prev = None
    del temp
    assert dllnode._next is None
    assert last_state(algo).state_type == "dllnode_delete"

def test_doubly_linkedlist():
    """Tests the DoublyLinkedList."""
    algo = StateSet()
    dl = DoublyLinkedList('list',algo)
    temp = DoublyLinkedListNode(algo,1)
    dl.head = temp
    dl.tail = temp
    states_expected = [
        "dll_declare",
        "dllnode_declare",
        "dll_head",
        "dll_tail"
    ]
    del temp
    check_states(states_expected,algo)

    dl.push_front(3)
    states_expected = [
        "dllnode_declare",
        "dllnode_next",
        "dllnode_prev",
        "dll_head"
    ]
    check_states(states_expected,algo)

    dl.push_back(4)
    states_expected = [
        "dllnode_declare",
        "dllnode_prev",
        "dllnode_next",
        "dll_tail"
    ]
    check_states(states_expected,algo)

    dl.insert(2,1)
    states_expected = [
        "dllnode_declare",
        "dllnode_iter",
        "dllnode_next",
        "dllnode_prev",
        "dllnode_prev",
        "dllnode_next"
    ]
    check_states(states_expected,algo)

    dl.front()
    dl.back()
    states_expected = [
        "dllnode_iter",
        "dllnode_iter"
    ]
    check_states(states_expected,algo)

    dl.remove(2)
    states_expected = [
        "dllnode_iter",
        "dllnode_iter",
        "dllnode_iter",
        "dllnode_next",
        "dllnode_iter",
        "dllnode_prev",
        "dllnode_delete",
        "dllnode_iter",
        "dllnode_iter"
    ]
    check_states(states_expected,algo)

    dl.pop_back()
    states_expected = [
        'dllnode_iter',
        'dll_tail',
        'dllnode_delete',
        'dllnode_next',
    ]
    check_states(states_expected,algo)

    dl.pop_front()
    states_expected = [
        'dllnode_iter',
        'dllnode_iter',
        'dll_head',
        'dllnode_delete',
        'dllnode_prev',
    ]
    check_states(states_expected,algo)

    dl.remove(1)
    states_expected = [
        'dllnode_iter',
        'dll_head',
        'dll_tail',
        'dllnode_delete',
    ]
    check_states(states_expected,algo)
