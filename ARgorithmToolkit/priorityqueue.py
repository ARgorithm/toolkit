"""The priorityqueue module provides support for priority queues maintained
using min heap tree. The main class in this module is the PriorityQueue class.
The PriorityQueueState acts as a support class to PriorityQueue class. For this
reason the PriorityQueue class can directly be imported from the
ARgorithmToolkit library without having to import from the priorityqueue
module:

    >>> pq = ARgorithmToolkit.priorityqueue.PriorityQueue(name="pq",algo=algo)
    >>> pq = ARgorithmToolkit.PriorityQueue(name="pq",algo=algo)
"""
import heapq
from ARgorithmToolkit.utils import State, StateSet, ARgorithmError, ARgorithmStructure
from ARgorithmToolkit.encoders import serialize

class PriorityQueueState():
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.priorityqueue.PriorityQueue`` object.

    Attributes:

        name (str) : Name of the variable for whom we are generating states
        _id (str) : id of the variable for whom we are generating states
    """
    def __init__(self,name,_id):
        self.name = name
        self._id = _id

    def priorityqueue_declare(self,comments=""):
        """Generates the `priorityqueue_declare` state when an instance of
        PriorityQueue is created.

        Args:
            body: The contents of the PriorityQueue that are to be sent along with the state
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``priorityqueue_declare`` state for the respective PriorityQueue mentioned
        """
        state_type = "priorityqueue_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : []
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def priorityqueue_offer(self,body,element,comments=""):
        """Generates the `priorityqueue_offer` when an element is added to
        priority queue.

        Args:
            body: The contents of the PriorityQueue that are to be sent along with the state
            element: The element to be added
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``priorityqueue_offer`` state for the respective PriorityQueue mentioned
        """
        state_type = "priorityqueue_offer"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
            "element" : element
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def priorityqueue_poll(self,body,comments=""):
        """Generates the `priorityqueue_offer` when an element is popped from
        priority queue.

        Args:
            body: The contents of the PriorityQueue that are to be sent along with the state
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``priorityqueue_poll`` state for the respective PriorityQueue mentioned
        """
        state_type = "priorityqueue_poll"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def priorityqueue_peek(self,body,comments=""):
        """Generates the `priorityqueue_peek` when first element of priority
        queue is accessed.

        Args:
            body: The contents of the PriorityQueue that are to be sent along with the state
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``priorityqueue_peek`` state for the respective PriorityQueue mentioned
        """
        state_type = "priorityqueue_peek"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

@serialize
class PriorityQueue(ARgorithmStructure):
    """The PriorityQueue class offes a priority queue container that stores
    states in its stateset which later are used to make dynamic Augmented
    reality visualizations.

    Attributes:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of PriorityQueue Class
        comments (str, optional): Comments for descriptive format. Defaults to "".

    Raises:
        ARgorithmError: raised if name is not given or Stateset if not provided

    Examples:
        >>> algo = ARgorithmToolkit.StateSet()
        >>> pq = ARgorithmToolkit.PriorityQueue(name="pq",algo=algo)
    """

    def __init__(self, name:str, algo:StateSet, comments:str = ""):
        try:
            assert isinstance(name,str)
            self._id = str(id(self))
            self.state_generator = PriorityQueueState(name, self._id)
        except AssertionError as e:
            raise ARgorithmError('Give valid name to data structure') from e
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("Queue structure needs a reference of template to store states") from e
        self.body = []
        state = self.state_generator.priorityqueue_declare(comments)
        self.algo.add_state(state)

    def __len__(self):
        """returns length of PriorityQueue when processed by len() function.

        Returns:
            int: Size of PriorityQueue

        Example:
            >>> len(pq)
            0
        """
        return len(self.body)

    def empty(self):
        """Checks whether PriorityQueue is empty or not.

        Returns:
            bool: flag that is true if PriorityQueue is empty

        Example:
            >>> pq = ARgorithmToolkit.PriorityQueue(name="pq",algo=algo)
            >>> pq.empty()
            True
            >>> pq.offer(1)
            >>> pq.empty()
            False
        """
        return len(self)==0

    def offer(self,element,comments=""):
        """Add element to priority queue.

        Args:
            element : element to be added to priority queue
            comments (str, optional): Comments for descriptive format. Defaults to "".

        Example:
            >>> pq.offer(4)
            >>> pq.offer(3)
            >>> pq.offer(5)
            >>> pq
            PriorityQueue([3, 4, 5])
        """
        heapq.heappush(self.body, element)
        state = self.state_generator.priorityqueue_offer(self.body,element,comments)
        self.algo.add_state(state)

    def poll(self,comments=""):
        """pops first element from priority queue.

        Args:
            comments (str, optional): Comments for descriptive format. Defaults to "".

        Raises:
            ARgorithmError: If priority queue is empty

        Returns:
            element : first element of priority queue

        Example:
            >>> pq.offer(2)
            >>> pq.offer(4)
            >>> pq.offer(3)
            >>> pq.poll()
            2
            >>> pq.poll()
            3
            >>> pq.poll()
            4
        """
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = heapq.heappop(self.body)
        state = self.state_generator.priorityqueue_poll(self.body,comments)
        self.algo.add_state(state)
        return item

    def peek(self,comments=""):
        """peeks at first element of priority queue.

        Args:
            comments (str, optional): Comments for descriptive format. Defaults to "".

        Raises:
            ARgorithmError: If priority queue is empty

        Returns:
            element : first element of priority queue

        Example:
            >>> pq.offer(4)
            >>> pq.offer(3)
            >>> pq.offer(5)
            >>> pq.peek()
            3
            >>> pq.peek()
            3
        """
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = self.body[0]
        state = self.state_generator.priorityqueue_peek(self.body,comments)
        self.algo.add_state(state)
        return item

    def __str__(self):
        """String conversion for Priority Queue.

        Returns:
            str: String describing Priority Queue
        """
        return f"PriorityQueue({self.body.__str__()})"

    def __repr__(self):
        """Return representation for shell outputs.

        Returns:
            str: shell representation for priority queue
        """
        return f"PriorityQueue({self.body.__repr__()})"
