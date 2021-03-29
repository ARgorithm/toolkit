# pylint: disable=protected-access
"""The Doubly linked list module provides support for rendering doubly linked
lists.

The classes are designed similar to that of classes in linkedlist module.

- The DoublyLinkedListNode class is used to represent a node.
- The DoublyLinkedList class is a complete implementation of doubly linked list
which provide various functions and record the head and tail nodes as well

These three classes can be directly imported from the toolkit:

    >>> dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
    >>> dll = ARgorithmToolkit.DoublyLinkedList("dllnode",algo)

"""

from ARgorithmToolkit.utils import ARgorithmHashable, ARgorithmStructure, State, StateSet, ARgorithmError
from ARgorithmToolkit.encoders import serialize

class DoublyLinkedListNodeState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.doublylinkedlist.DoublyLinkedListNode`` object.

    Attributes:

        name (str) : Name of the object for which states are generated
        _id (str) : id of the object for which states are generated
    """

    def __init__(self,name:str,_id:str):
        self.name = name
        self._id = _id

    def dllnode_declare(self,value,next_node,prev_node,comments=""):
        """Generates the `dllnode_declare` state when a new node is created.

        Args:
            value : The value stored in the doubly linked list node
            next_node (DoublyLinkedListNode): The next pointer
            prev_node (DoublyLinkedListNode): The prev pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dllnode_declare` state
        """
        state_type = "dllnode_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : next_node._id if next_node else "none",
            "prev" : prev_node._id if prev_node else "none",
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def dllnode_iter(self,value,next_node,prev_node,last_value=None,comments=""):
        """Generates the `dllnode_iter` state when a node is accessed or its
        value is changed.

        Args:
            value : The value stored in the linked list node
            next_node (DoublyLinkedListNode): The next pointer
            prev_node (DoublyLinkedListNode): The prev pointer
            last_value (optional): stores the value in the linked list node before it was changed.
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dllnode_iter` state
        """
        state_type = "dllnode_iter"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : next_node._id if next_node else "none",
            "prev" : prev_node._id if prev_node else "none",
        }
        if last_value is not None:
            state_def["last_value"] = last_value
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def dllnode_next(self,value,next_node,prev_node,last_next,comments=""):
        """Generates the `dllnode_next` state when the next pointer changes.

        Args:
            value : The value stored in the linked list node
            next_node (DoublyLinkedListNode): The next pointer
            prev_node (DoublyLinkedListNode): The prev pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dllnode_next` state
        """
        state_type = "dllnode_next"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : next_node._id if next_node else "none",
            "prev" : prev_node._id if prev_node else "none",
            "last_next" : last_next if last_next else "none",
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def dllnode_prev(self,value,next_node,prev_node,last_prev,comments=""):
        """Generates the `dllnode_prev` state when the prev pointer changes.

        Args:
            value : The value stored in the linked list node
            next_node (DoublyLinkedListNode): The next pointer
            prev_node (DoublyLinkedListNode): The prev pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dllnode_prev` state
        """
        state_type = "dllnode_prev"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : next_node._id if next_node else "none",
            "prev" : prev_node._id if prev_node else "none",
            "last_prev" : last_prev if last_prev else "none",
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )


    def dllnode_delete(self,comments=""):
        """Generates the `dllnode_delete` state when a node is deleted.

        Args:
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dllnode_delete` state
        """
        state_type = "dllnode_delete"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

@serialize
class DoublyLinkedListNode(ARgorithmStructure, ARgorithmHashable):
    """The DoublyLinkedListNode class is an implementation of a Linked list
    Node for which we store states. Unlike other data structure classes, in
    which we have to give a name to the instance, we dont have to provide name
    in the DoublyLinkedListNode Class.

    Attributes:
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of DoublyLinkedListNode Class
        value: The value stored in the node
        next (DoublyLinkedListNode): The reference to next node
        prev (DoublyLinkedListNode): The reference to prev node

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
        >>> dllnode.value = 10
        >>> temp = = ARgorithmToolkit.DoublyLinkedListNode(algo,6)
        >>> temp.next = dllnode
        >>> dllnode.prev = temp
    """
    def __init__(self,algo:StateSet,value,comments=""):
        self.name = str(id(self))
        self._id = str(id(self))
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("algo should be of type StateSet") from e

        self.state_generator = DoublyLinkedListNodeState(self.name, self._id)

        self._value = value
        self._next = None
        self._prev = None

        state = self.state_generator.dllnode_declare(
            self._value,self._next,comments
        )
        self.algo.add_state(state)

    def highlight(self):
        """The highlight function trigger the `dllnode_iter` state
        """
        state = self.state_generator.dllnode_iter(self._value,self._next,self._prev)
        self.algo.add_state(state)

    @property
    def value(self):
        """Getter function for the value of node

        Example:
            >>> ll = DoublyLinkedListNode(algo,3)
            >>> ll.value
            3
        """
        self.highlight()
        return self._value

    @value.setter
    def value(self,v):
        """Setter function for the value of node

        Example:
            >>> ll = DoublyLinkedListNode(algo,3)
            >>> ll.value = 4
            >>> ll.value
            4
        """
        last = self._value
        self._value = v
        state = self.state_generator.dllnode_iter(self._value,self._next,self._prev,last_value=last)
        self.algo.add_state(state)

    @property
    def next(self):
        """Getter function for the next node

        Example:
            >>> ll.next
        """
        if self._next:
            self._next.highlight()
        return self._next

    @next.setter
    def next(self,n):
        """Setter function for the next node

        Example:
            >>> ll.next = DoublyLinkedListNode(algo,5)

        Raises:
            TypeError: if the next node is not None or of type `DoublyLinkedListNode`
        """
        try:
            assert n is None or isinstance(n,DoublyLinkedListNode)
        except AssertionError as ae:
            raise TypeError("next attribute can only set as None or instance of DoublyLinkedListNode")
        last = self._next
        last = self._next._id if self._next else None
        self._next = n
        if self._next is not None or last is not None:
            state = self.state_generator.dllnode_next(self._value,self._next,self._prev,last_next=last)
            self.algo.add_state(state)

    @property
    def prev(self):
        """Getter function for the prev node

        Example:
            >>> ll.prev
        """
        if self._prev:
            self._prev.highlight()
        return self._prev

    @prev.setter
    def prev(self,n):
        """Setter function for the prev node

        Example:
            >>> ll.prev = DoublyLinkedListNode(algo,5)

        Raises:
            TypeError: if the prev node is not None or of type `DoublyLinkedListNode`
        """
        try:
            assert n is None or isinstance(n,DoublyLinkedListNode)
        except AssertionError as ae:
            raise TypeError("prev attribute can only set as None or instance of DoublyLinkedListNode")
        last = self._prev._id if self._prev else None
        self._prev = n
        if self._prev is not None or last is not None:
            state = self.state_generator.dllnode_prev(self._value,self._next,self._prev,last_prev=last)
            self.algo.add_state(state)

    def __del__(self):
        """The __del__ function is overriden is there to listen to node
        deletion."""
        state = self.state_generator.dllnode_delete(
            "Node was deleted"
        )
        self.algo.add_state(state)

    def __str__(self):
        return f"LinkedListNode({self._value}) at {self._id}"

    def __repr__(self):
        return f"LinkedListNode({self._value}) at {self._id}"

class DoublyLinkedListState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.doublylinkedlist.DoublyLinkedList`` object.

    Attributes:

        name (str) : Name of the variable for whom we are generating states
        _id (str) : id of the variable for whom we are generating states
    """
    def __init__(self,name:str,_id:str):
        self.name = name
        self._id = _id

    def dll_declare(self,head,tail,comments=""):
        """Generates the `dll_declare` state when a new linked list is created.

        Args:
            head (DoublyLinkedListNode): The head pointer
            tail (DoublyLinkedListNode): The tail pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dll_declare` state
        """
        state_type = "dll_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "head" : head.name if head else "none",
            "tail" : tail.name if tail else "none"
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def dll_head(self,head,tail,last_head=None,comments=""):
        """Generates the `dll_head` state when linked list head is changed.

        Args:
            head (DoublyLinkedListNode): The head pointer
            tail (DoublyLinkedListNode): The tail pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dll_head` state
        """
        state_type = "dll_head"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "head" : head.name if head else "none",
            "tail" : tail.name if tail else "none"
        }
        if not (last_head is None):
            state_def['last_head'] = last_head
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def dll_tail(self,head,tail,last_tail=None,comments=""):
        """Generates the `dll_tail` state when linked list tail is changed.

        Args:
            head (DoublyLinkedListNode): The head pointer
            tail (DoublyLinkedListNode): The tail pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `dll_tail` state
        """
        state_type = "dll_tail"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "head" : head.name if head else "none",
            "tail" : tail.name if tail else "none"
        }
        if not(last_tail is None):
            state_def['last_tail'] = last_tail
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

class ListIterator:
    """This class is a generator that is returned each time an List has to be
    iterated.

    Yields:
        Value of List Node

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.doublylinkedlist.DoublyLinkedList
    """
    def __init__(self,doublylist):
        assert isinstance(doublylist,DoublyLinkedList)
        self._curr = doublylist.head

    def __next__(self):
        if self._curr:
            data = self._curr.value
            self._curr = self._curr.next
            return data
        raise StopIteration

@serialize
class DoublyLinkedList:
    """The DoublyLinkedList class is proper implementation of doubly linked list.

    Attributes:
        name (str): The name given to the linked list
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of DoublyLinkedList Class
        head (DoublyLinkedListNode): The referece to head of linked list
        tail (DoublyLinkedListNode): The referece to tail of linked list

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> lis = ARgorithmToolkit.DoublyLinkedList("list",algo)
        >>> lis
        DoublyLinkedList([])
    """

    def __init__(self,name:str,algo:StateSet,comments=""):

        assert isinstance(name,str) , ARgorithmError("Name should be of type string")
        self.name = name
        self._id = str(id(self))
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("algo should be of type StateSet") from e
        self.state_generator = DoublyLinkedListState(self.name, self._id)

        self._head = None
        self._tail = None

        state = self.state_generator.dll_declare(self._head,comments)
        self.algo.add_state(state)

    @property
    def head(self):
        return self._head

    @head.setter
    def head(self,h):
        if h:
            assert isinstance(h,DoublyLinkedListNode) , ARgorithmError("head should be of type None or LinkedListNode")
        last_head = self._head._id if self._head else None
        self._head = h
        state = self.state_generator.dll_head(self._head,self._tail,last_head=last_head, comments="head pointer shifts")
        self.algo.add_state(state)

    @property
    def tail(self):
        return self._tail

    @tail.setter
    def tail(self,t):
        if t:
            assert isinstance(t,DoublyLinkedListNode) , ARgorithmError("tail should be of type None or LinkedListNode")
        last_tail = self._tail._id if self._tail else None
        self._tail = t
        state = self.state_generator.dll_tail(self._head,self._tail,last_tail=last_tail, comments="tail pointer shifts")
        self.algo.add_state(state)

    def __len__(self):
        """overloads the len() operator to return size of list.

        Returns:
            int: size of list

        Example:

            >>> len(lis)
        """
        size = len(self.tolist())
        return size

    def insert(self,value,index=None):
        """Insert node with given value at particular index. If index is not
        given,insert at back.

        Args:
            value : The value to be inserted
            index (int, optional): The index where value has to inserted . Defaults to None.

        Example:

            >>> lis = ARgorithmToolkit.List("list",algo)
            >>> lis.insert(1)
            >>> lis.insert(3)
            >>> lis.insert(2,1)
            >>> lis
            List([1, 2, 3])
        """
        if self._head is None or index == 0:
            self.push_front(value)
        else:
            count = 1
            temp = self.head
            while index > count:
                count += 1
                temp = temp.next
            curr = DoublyLinkedListNode(self.algo,value)
            curr.next = temp.next
            curr.prev = temp
            if curr._next:
                curr._next.prev = curr
            if curr._prev:
                curr._prev.next = curr

    def push_front(self,value):
        """Pushes value to front.

        Args:
            value : Value to be appended to front

        Example:

            >>> lis = ARgorithmToolkit.List("list",algo)
            >>> lis.push_front(2)
            >>> lis.push_front(1)
            >>> lis
            List([1, 2])
        """
        curr = DoublyLinkedListNode(self.algo,value)
        if self._head:
            curr.next = self.head
            self.head.prev = curr
            self.head = curr
        else:
            curr.next = None
            curr.prev = None
            self.head = curr
            self.tail = curr

    def push_back(self,value):
        """Pushes value to back.

        Args:
            value : Value to be appended to back

        Example:

            >>> lis = ARgorithmToolkit.List("list",algo)
            >>> lis.push_back(1)
            >>> lis.push_back(3)
            >>> lis
            List([1, 3])
        """
        curr = DoublyLinkedListNode(self.algo,value)
        if self._tail:
            curr.prev = self.tail
            self.tail.next = curr
            self.tail = curr
        else:
            curr.next = None
            self.head = curr
            self.tail = curr

    def pop_front(self):
        """Pops first element of List.

        Raises:
            ARgorithmError: Raised if list is empty

        Returns:
            element: The first element of list

        Example:

            >>> lis
            List([5, 1, 2, 3, 7])
            >>> lis.pop_front()
            5
            >>> lis
            List([1, 2, 3, 7])
        """
        if self._head is None:
            raise ARgorithmError("Empty list")
        data = self.head.value
        self.head = self.head.next
        if self._head:
            self.head.prev = None
        else:
            self.tail = None
        return data

    def pop_back(self):
        """Pops first element of List.

        Raises:
            ARgorithmError: Raised if list is empty

        Returns:
            element: The first element of list

        Example:

            List([1, 2, 3, 7])
            >>> lis.pop_back()
            7
            >>> lis
            List([1, 2, 3])
        """
        if self._head is None:
            raise ARgorithmError("Empty list")
        data = self.tail.value
        self.tail = self.tail.prev
        if self._tail:
            self.tail.next = None
        else:
            self.head = None
        return data

    def front(self):
        """Returns the first element of list.

        Raises:
            ARgorithmError: Raised when list is empty

        Returns:
            element: The first element of list

        Example:

            >>> lis
            List([1, 2, 3])
            >>> lis.front()
            1
            >>> lis
            List([1, 2, 3])
        """
        if self._head is None:
            raise ARgorithmError("Empty list")
        return self._head.value

    def back(self):
        """Returns the last element of list.

        Raises:
            ARgorithmError: Raised when list is empty

        Returns:
            element: The last element of list

        Example:

            >>> lis
            List([2, 3, 5, 4, 4, 3, 3])
            >>> lis.back()
            3
            >>> lis
            List([2, 3, 5, 4, 4, 3, 3])
        """
        if self._head is None:
            raise ARgorithmError("Empty list")
        return self._tail.value

    def __iter__(self):
        """Returns the generator object to iterate through elements of List.

        Returns:
            ListIterator: Generator class for List

        Example:

            >>> [x for x in lis]
            [2, 3, 5, 4, 4, 3, 3]
        """
        return ListIterator(self)

    def remove(self,value):
        """Remove elements with given value from list.

        Args:
            value : The value which has to be removed

        Raises:
            ARgorithmError: Raised if list is empty

        Example:

            >>> lis
            List([2, 3, 5, 4, 4, 3, 3])
            >>> lis.remove(3)
            >>> lis
            List([2, 5, 4, 4])
        """
        if self._head is None:
            raise ARgorithmError("Empty list")
        curr = self.head
        while curr:
            if curr.value == value:
                if self._head is curr and self._tail is curr:
                    self.head = None
                    self.tail = None
                    break
                if curr._prev:
                    curr._prev.next = curr.next
                else:
                    self.head = curr.next
                    self.head.prev = None
                if curr._next:
                    curr._next.prev = curr.prev
                else:
                    self.tail = curr.prev
                    self.tail.next = None
            curr = curr._next

    def tolist(self):
        """Converts the List to python list.

        Returns:
            list: list of List items

        Example:

            >>> lis
            List([2, 5, 4, 4])
            >>> lis.tolist()
            [2, 5, 4, 4]
        """
        curr = self._head
        data = []
        while curr:
            data.append(curr._value)
            curr = curr._next
        return data

    def __repr__(self):
        return f"DoublyLinkedList({self.tolist()})"

    def __str__(self):
        return f"DoublyLinkedList({self.tolist()})"
