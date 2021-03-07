"""The Doubly linked list module provides support for rendering doubly linked
lists.

The classes are designed similar to that of classes in linkedlist module.

- The DoublyLinkedListNode class is used to represent a node.
- The DoublyLinkedList class is used to store the head pointer.
- The List class is a complete implementation of doubly linked list

These three classes can be directly imported from the toolkit:

    >>> dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
    >>> dll = ARgorithmToolkit.DoublyLinkedList("dllnode",algo)
    >>> dl = ARgorithmToolkit.List("dl",algo)
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
            "next" : next_node.name if next_node else "none",
            "prev" : prev_node.name if prev_node else "none",
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
            "next" : next_node.name if next_node else "none",
            "prev" : prev_node.name if prev_node else "none",
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
            "next" : next_node.name if next_node else "none",
            "prev" : prev_node.name if prev_node else "none",
            "last_next" : last_next.name if last_next else "none",
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
            "next" : next_node.name if next_node else "none",
            "prev" : prev_node.name if prev_node else "none",
            "last_prev" : last_prev.name if last_prev else "none",
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

    def __init__(self,algo:StateSet,value=None,comments=""):
        self.name = str(id(self))
        self._id = str(id(self))
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("algo should be of type StateSet") from e

        self.state_generator = DoublyLinkedListNodeState(self.name, self._id)

        self._flag = False
        self.value = value
        self.prev = None
        self.next = None
        self._flag = True

        state = self.state_generator.dllnode_declare(
            self.value,self.next,self.prev,comments
        )
        self.algo.add_state(state)

    def __setattr__(self,key,value):
        """The __setattr__ function is overriden to listen to state changes in
        the value of node or the next attribute.

        Raises:
            ARgorithmError: Raised if next pointer is not type None or DoublyLinkedListNode
        """
        if key in ['next','prev'] and value:
            assert isinstance(value,DoublyLinkedListNode) , ARgorithmError("next should be of type None or DoublyLinkedListNode")
        last_value = None
        last_prev = None
        last_next = None
        if key == 'value' and self._flag:
            last_value = self.value
        elif key == 'prev' and self._flag:
            last_prev = self.prev
        elif key == 'next' and self._flag:
            last_next = self.next
        self.__dict__[key] = value
        if key == 'prev' and self._flag:
            if last_prev or self.prev:
                state = self.state_generator.dllnode_prev(
                    value=self.value,
                    next_node=self.next,
                    prev_node=self.prev,
                    last_prev=last_prev,
                    comments="prev pointer updated"
                )
                self.algo.add_state(state)
        elif key == 'next' and self._flag:
            if last_next or self.next:
                state = self.state_generator.dllnode_next(
                    value=self.value,
                    next_node=self.next,
                    prev_node=self.prev,
                    last_next=last_next,
                    comments="next pointer updated"
                )
                self.algo.add_state(state)
        elif key == 'value' and self._flag:
            state = self.state_generator.dllnode_iter(
                value=self.value,
                next_node=self.next,
                prev_node=self.prev,
                last_value=last_value,
                comments="value updated"
            )
            self.algo.add_state(state)

    def __del__(self):
        """The __del__ function is overriden is there to listen to node
        deletion."""
        state = self.state_generator.dllnode_delete(
            "Node was deleted"
        )
        self.algo.add_state(state)

    def __str__(self):
        return f"DoublyLinkedListNode({self.value}) at {self.name}"

    def __repr__(self):
        return f"DoublyLinkedListNode({self.value}) at {self.name}"

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

@serialize
class DoublyLinkedList(ARgorithmStructure, ARgorithmHashable):
    """The DoublyLinkedList class is used to just store the head of the linked
    list.

    This class is useful when programmer want to program his own List class using
    the nodes. Only contains head attribute and no methods

    Attributes:
        name (str): The name given to the linked list
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of DoublyLinkedList Class
        head (DoublyLinkedListNode): The referece to head and tail of linked list as initially they will be same

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> dll = ARgorithmToolkit.DoublyLinkedList("llnode",algo)
        >>> dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
        >>> dll.head = llnode
    """

    def __init__(self,name:str,algo:StateSet,head=None,comments=""):

        assert isinstance(name,str) , ARgorithmError("Name should be of type string")
        self.name = name
        self._id = str(id(self))
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("algo should be of type StateSet") from e
        self.state_generator = DoublyLinkedListState(self.name, self._id)

        if head:
            assert self.algo == head.algo, ARgorithmError("The head node belongs to a different StateSet")

        self._flag = False
        self.head = head
        self.tail = head
        self._flag = True

        state = self.state_generator.dll_declare(self.head,self.tail,comments)
        self.algo.add_state(state)

    def __setattr__(self,key,value):
        """The __setattr__ function is overriden to listen to state changes in
        the head.

        Raises:
            ARgorithmError: Raised if head pointer is not type None or DoublyLinkedListNode
        """
        if key in ['head','tail'] and value:
            assert isinstance(value,DoublyLinkedListNode) , ARgorithmError("next should be of type None or DoublyLinkedListNode")
        last_head = None
        last_tail = None
        if key == 'head' and self._flag:
            last_head = self.head._id if self.head else "none"
        elif key == 'tail' and self._flag:
            last_tail = self.tail._id if self.tail else "none"
        self.__dict__[key] = value
        if key == 'head' and self._flag:
            state = self.state_generator.dll_head(self.head,self.tail,last_head=last_head,comments="head pointer shifts")
            self.algo.add_state(state)
        if key == 'tail' and self._flag:
            state = self.state_generator.dll_tail(self.head,self.tail,last_tail=last_tail,comments="tail pointer shifts")
            self.algo.add_state(state)

    def __str__(self):
        return f"DoublyLinkedList(head at {self.head})"

    def __repr__(self):
        return f"DoublyLinkedList(head at {self.head})"


class ListIterator:
    """This class is a generator that is returned each time an List has to be
    iterated.

    Yields:
        Value of List Node

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.doublylinkedlist.List
    """
    def __init__(self,doublylist):
        assert isinstance(doublylist,List)
        self._curr = doublylist.head

    def __next__(self):
        if self._curr:
            data = self._curr.value
            self._curr = self._curr.next
            return data
        raise StopIteration

class List(DoublyLinkedList):
    """The List class is proper implementation of doubly linked list.

    The difference between DoublyLinkedList and List class is that List
    is a ready implementation of singly linked list. In the DoublyLinkedList class the
    programmer will have to make their own methods.

    Attributes:
        name (str): The name given to the linked list
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of List Class
        head (DoublyLinkedListNode): The referece to head of linked list
        tail (DoublyLinkedListNode): The referece to tail of linked list
        size (int): Number of nodes i.e size of list

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> lis = ARgorithmToolkit.List("list",algo)
        >>> lis
        List([])
    """

    def __init__(self,name:str,algo:StateSet,comments=""):
        super().__init__(name,algo,comments="")
        self.size = 0

    def __len__(self):
        """overloads the len() operator to return size of list.

        Returns:
            int: size of list

        Example:

            >>> len(lis)
        """
        return self.size

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
        if self.size == 0 or index == 0:
            self.push_front(value)
        elif index is None or self.size < index:
            self.push_back(value)
        else:
            count = 1
            temp = self.head
            while index > count:
                count += 1
                temp = temp.next
            curr = DoublyLinkedListNode(self.algo,value)
            curr.next = temp.next
            curr.prev = temp
            if curr.next:
                curr.next.prev = curr
            if curr.prev:
                curr.prev.next = curr
            self.size += 1

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
        if self.head:
            curr.next = self.head
            self.head.prev = curr
            self.head = curr
        else:
            curr.next = None
            curr.prev = None
            self.head = curr
            self.tail = curr
        self.size+=1

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
        if self.tail:
            curr.prev = self.tail
            self.tail.next = curr
            self.tail = curr
        else:
            curr.next = None
            self.head = curr
            self.tail = curr
        self.size+=1


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
        if self.head is None:
            raise ARgorithmError("Empty list")
        data = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        self.size -= 1
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
        if self.head is None:
            raise ARgorithmError("Empty list")
        data = self.tail.value
        self.tail = self.tail.prev
        if self.tail:
            self.tail.next = None
        else:
            self.head = None
        self.size -= 1
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
        if self.head is None:
            raise ARgorithmError("Empty list")
        return self.head.value

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
        if self.head is None:
            raise ARgorithmError("Empty list")
        return self.tail.value

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
        if self.head is None:
            raise ARgorithmError("Empty list")
        curr = self.head
        while curr:
            if curr.value == value:
                self.size -= 1
                if self.size == 1:
                    self.head = None
                    self.tail = None
                    break
                if curr.prev:
                    curr.prev.next = curr.next
                else:
                    self.head = curr.next
                    self.head.prev = None
                if curr.next:
                    curr.next.prev = curr.prev
                else:
                    self.tail = curr.prev
                    self.tail.next = None
            curr = curr.next

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
        curr = self.head
        data = []
        while curr:
            data.append(curr.value)
            curr = curr.next
        return data

    def __repr__(self):
        return f"List({self.tolist()})"

    def __str__(self):
        return f"List({self.tolist()})"
