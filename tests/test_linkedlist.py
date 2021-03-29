"""Testing linked list."""
from ARgorithmToolkit import LinkedList,StateSet,LinkedListNode
from .utils import last_state,check_states
algo = StateSet()

def test_node():
    """Testing linked list node."""
    llnode = LinkedListNode(algo,7)
    assert llnode._value == 7
    assert llnode._next is None
    assert last_state(algo).state_type == "llnode_declare"

    llnode.value = 5
    assert llnode._value == 5
    assert llnode._next is None
    assert last_state(algo).state_type == "llnode_iter"


    temp = LinkedListNode(algo,3)
    llnode.next = temp

    assert isinstance(llnode._next,LinkedListNode)
    assert llnode._next == temp
    assert last_state(algo).state_type == "llnode_next"

    llnode.next = None
    del temp
    assert llnode._next is None
    assert last_state(algo).state_type == "llnode_delete"

def test_linkedlist():
    """Tests the LinkedList class."""
    algo = StateSet()
    linkedlist = LinkedList('list',algo)
    temp = LinkedListNode(algo,2)
    linkedlist.head = temp

    algo = StateSet()
    linkedlist = LinkedList('list',algo)
    linkedlist.insert(3)
    states_expected = [
        "ll_declare",
        "llnode_declare",
        "ll_head"
    ]
    check_states(states_expected,algo)

    linkedlist.insert(4)
    states_expected = [
        "llnode_declare",
        "llnode_next",
        "ll_head"
    ]
    check_states(states_expected,algo)

    linkedlist.insert(2,1)
    states_expected = [
        "llnode_declare",
        "llnode_iter",
        "llnode_next",
        "llnode_next"
    ]
    check_states(states_expected,algo)

    linkedlist.push_front(5)
    states_expected = [
        "llnode_declare",
        "llnode_next",
        "ll_head"
    ]
    check_states(states_expected,algo)

    linkedlist.pop_front()
    states_expected = [
        "llnode_iter",
        "ll_head",
        "llnode_delete"
    ]
    check_states(states_expected,algo)

    linkedlist.remove(2)
    states_expected = [
        "llnode_next",
        "llnode_delete",
        "llnode_iter"
    ]
    check_states(states_expected,algo)
