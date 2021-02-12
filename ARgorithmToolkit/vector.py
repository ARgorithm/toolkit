"""The vector module provides support for vectors. The main class in this
module is the Vector class. The other classes act as support class to Vector
class. For this reason the Vector class can directly be imported from the
ARgorithmToolkit library without having to import from the vector module Both
work:

    >>> vec = ARgorithmToolkit.Vector(name='vec',algo=algo)
    >>> vec = ARgorithmToolkit.vector.Vector(name='vec',algo=algo)
"""

from ARgorithmToolkit.utils import State, StateSet, ARgorithmError, ARgorithmStructure
from ARgorithmToolkit.encoders import serialize

class VectorState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.vector.Vector`` object.

    Attributes:

        name (str) : Name of the variable for whom we are generating states
    """
    def __init__(self,name,_id):
        self.name = name
        self._id = _id


    def vector_declare(self,body,comments=""):
        """Generates the `vector_declare` state when an instance of Vector
        class is created.

        Args:
            body (list): The contents of the vector that are to be sent along with the state
            comments (str,optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``vector_declare`` state for the respective vector mentioned
        """
        state_type = "vector_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body)
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def vector_iter(self,body,index,value=None,last_value=None,comments=""):
        """Generates the `vector_iter` state when a particular index of vector
        has been accessed.

        Args:
            body (list): The contents of the vector that are to be sent along with the state
            index (int): The index of vector that has been accessed
            value (optional): The current value at array[index] if __setitem__(self, key, value) was called.
            last_value (optional): The current value at array[index] if __setitem__(self, key, value) was called.
            comments (str,optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``vector_iter`` state for the respective vector mentioned
        """
        state_type = "vector_iter"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
            "index" : index
        }
        if not (last_value is None):
            state_def["value"] = value
            state_def["last_value"] = last_value
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def vector_remove(self,body,index , comments=""):
        """Generates the `vector_remove` state when a element at particular
        index of vector is removed.

        Args:
            body (list): The contents of the vector that are to be sent along with the state
            index (int): The index of vector at which the element has to be removed
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``vector_remove`` state for the respective vector mentioned
        """
        state_type = "vector_remove"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def vector_insert(self,body,element,index,comments=""):
        """Generates the `vector_insert` state when a element is to be inserted
        at particular index of vector.

        Args:
            body (list): The contents of the vector that are to be sent along with the state
            element : The element that is to be added at index
            index (int): The index of vector at which the element has to be added
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``vector_insert`` state for the respective vector mentioned
        """
        state_type = "vector_insert"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
            "element" : element,
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def vector_swap(self,body,indexes,comments=""):
        """Generates the ``vector_swap`` state when values at two indexes of
        vector are being swapped.

        Args:
            body (list): The contents of the vector that are to be sent along with the state
            indexes (tuple): The indexes that are supposed to be swapped
            comments (str,optional):The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``vector_swap`` state for the respective vector mentioned
        """
        state_type = "vector_swap"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
            "index1" : indexes[0],
            "index2" : indexes[1]
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def vector_compare(self,body,indexes,comments=""):
        """Generates the ``vector_compare`` state when values at two indexes of
        vector are being compared.

        Args:
            body (list): The contents of the vector that are to be sent along with the state
            indexes (tuple): The indexes that are supposed to be compared
            comments (str,optional):The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``vector_compare`` state for the respective vector mentioned
        """
        state_type = "vector_compare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : list(body),
            "index1" : indexes[0],
            "index2" : indexes[1]
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

class VectorIterator:
    """This class is a generator that is returned each time an vector has to be
    iterated.

    Yields:
        element of Vector

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.vector.Vector
    """
    def __init__(self,vector):
        assert isinstance(vector,Vector)
        self.vector = vector
        self._index = 0
        self.size = len(vector)

    def __next__(self):
        if self._index == self.size:
            raise StopIteration
        v = self.vector[self._index]
        self._index += 1
        return v

@serialize
class Vector(ARgorithmStructure):
    """The Vector class provides a wrapped around the python list class to
    emulate it as a vector.

    Args:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of Vector Class
        data (list or tuple,optional): The value of vector if user wants a predefined value. Defaults to None.
        comments (str,optional): Description of instance of vector and its applications that will be rendered during the ``vector_declare`` state.

    Raises:
        ARgorithmError: raised if name is not given or Stateset if not provided
        TypeError: if data is not a list

    Example:
        >>> algo = ARgorithmToolkit.StateSet()
        >>> vec = ARgorithmToolkit.Vector("vec",algo)
    """

    def __init__(self,name,algo,data=None,comments=""):
        try:
            assert isinstance(name,str)
            self._id = str(id(self))
            self.state_generator = VectorState(name, self._id)
        except AssertionError as e:
            raise ARgorithmError('Give valid name to data structure') from e
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("vector structure needs a reference of template to store states") from e
        try:
            if data is None:
                data = []
            assert isinstance(data,list) or data
            self.body = data
        except AssertionError as e:
            raise TypeError("vector body should be list") from e
        state = self.state_generator.vector_declare(self.body,comments)
        self.algo.add_state(state)

    def __len__(self):
        """Function overload for the len() function. Returns size of vector.

        Returns:
            int: size of vector

        Example:
            >>> len(vec)
            0
        """
        return len(self.body)

    def __getitem__(self,key,comments=""):
        """Operator overload for indexing to access element. Can also be used
        for slicing.

        Args:
            key (int or slice): The index or range for slicing
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            element: If key is int
            Vector: if key in slice

        Example:
            >>> vec
            Vector([1, 2, 3])
            >>> vec[2]
            3
            >>> vec[1:]
            Vector([2, 3])
        """
        if isinstance(key,slice):
            name = f"{self.state_generator.name}_sub"
            return Vector(name , self.algo , self.body[key] , comments)
        state = self.state_generator.vector_iter(body=self.body,index=key,comments=comments)
        self.algo.add_state(state)
        return self.body[key]

    def __setitem__(self, key, value):
        """Operator overload for indexing for assignment to listen to states if
        any element is changed.

        Args:
            key (int): Index at which we need assign the value
            value : The value to be set at index of vector

        Example:
            >>> vec
            Vector([1, 2, 3])
            >>> vec[1] = 5
            >>> vec
            Vector([1, 5, 3])
        """
        last_value = self.body[key]
        self.body[key] = value
        state = self.state_generator.vector_iter(body=self.body,index=key,value=value,last_value=last_value,\
            comments=f'Writing {value} at index {key}')
        self.algo.add_state(state)

    def __iter__(self):
        """Returns the generator object to iterate through elements of Vector.

        Returns:
            VectorIterator: Generator class for Vector

        Example:
            >>> [x for x in vec]
            [1, 5, 3]
        """
        return VectorIterator(self)

    def insert(self,value,index=None,comments=""):
        """Inserts element at particular index, if index not given then element
        is added to the end.

        Args:
            value : The value to be inserted
            index (int, optional): The index where element is to be inserted at. If not given , then element is added to end.
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> vec
            Vector([])
            >>> vec.insert(2)
            >>> vec
            Vector([2])
            >>> vec.insert(3)
            >>> vec
            Vector([2, 3])
            >>> vec.insert(1,0)
            >>> vec
            Vector([1, 2, 3])
        """
        if index is None:
            self.body.append(value)
            state = self.state_generator.vector_insert(self.body , value , len(self)-1 , comments)
            self.algo.add_state(state)
        elif index >= 0:
            self.body = self.body[:index] + [value] + self.body[index:]
            state = self.state_generator.vector_insert(self.body , value , index , comments)
            self.algo.add_state(state)

    def remove(self,value=None,index=None,comments=""):
        """Removes element from vector.If value is given then first instance of
        element of that value is removed. If index is given instead then the
        element at that index is removed. If neither is given then the last
        element is deleted.

        Args:
            value (optional): Value of element to be deleted
            index (int, optional): Index of element which has to be deleted
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Raises:
            ARgorithmError: Raised if both valur and index is given

        Example:
            >>> vec
            Vector([3, 3, 3, 3, 4, 5])
            >>> vec.remove(index=3)
            >>> vec
            Vector([3, 3, 3, 4, 5])
            >>> vec.remove()
            >>> vec
            Vector([3, 3, 3, 4])
            >>> vec.remove(value=3)
            >>> vec
            Vector([3, 3, 4])

        Note:
            Please make note of the position of arguments if passing positional arguments. It is recommended not to do that
        """
        if index is None and value is None:
            self.body.pop()
            state = self.state_generator.vector_remove(self.body,len(self)-1,comments)
            self.algo.add_state(state)
        elif value is None and 0 <= index < len(self):
            self.body = self.body[0:index] + self.body[index+1:]
            state = self.state_generator.vector_remove(self.body,index,comments)
            self.algo.add_state(state)
        elif index is None:
            index = self.body.index(value)
            self.body.remove(value)
            state = self.state_generator.vector_remove(self.body,index,comments)
            self.algo.add_state(state)
        else:
            raise ARgorithmError("Either give only a valid index or only value to be deleted , dont give both")

    def compare(self,index1,index2,func=None,comments=""):
        """compares elements at 2 indexes of vector.

        Args:
            index1 (int): The index of first element to be compared
            index2 (int): The index of second element to be compared
            func (function, optional): [description] The comparision function to be used , defaults to difference
            comments (str, optional): Any comments to describe comparision

        Returns:
            Result of comparision operation

        Example:
            >>> vec
            Vector([1, 2, 3])
            >>> vec.compare(0,1)
            -1
        """
        item1 = self.body[index1]
        item2 = self.body[index2]
        state = self.state_generator.vector_compare(self.body,(index1,index2),comments)
        self.algo.add_state(state)
        if func is None:
            def default_comparator(item1, item2):
                return item1-item2
            func = default_comparator
        return func(item1, item2)

    def swap(self,index1,index2,comments=""):
        """swaps elements at 2 indexes of vector.

        Args:
            index1 (index): The index of first element to be swapped
            index2 (index): The index of second element to be swapped
            comments (str, optional): Any comments to describe swap

        Example:
            >>> vec
            Vector([1, 2, 3])
            >>> vec.swap(0,2)
            >>> vec
            Vector([3, 2, 1])
        """
        temp = self.body[index1]
        self.body[index1] = self.body[index2]
        self.body[index2] = temp
        state = self.state_generator.vector_swap(self.body,(index1,index2),comments)
        self.algo.add_state(state)

    def __str__(self):
        """Returns string representation of vector.

        Returns:
            str: string representation of vector
        """
        return f"Vector({self.body.__str__()})"

    def __repr__(self):
        """Returns representation of vector.

        Returns:
            str: representation of vector
        """
        return f"Vector({self.body.__repr__()})"
