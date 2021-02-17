"""The array module provides support for one dimensional arrays as well as
multinational arrays. The main class in this module is the Array class. The
other classes act as support class to Array class. For this reason the Array
class can directly be imported from the ARgorithmToolkit library without having
to import from the array module Both work:

    >>> arr = ARgorithmToolkit.Array(name='arr',algo=algo,data=test_data)
    >>> arr = ARgorithmToolkit.array.Array(name='arr',algo=algo,data=test_data)
"""

import numpy as np
from ARgorithmToolkit.utils import State, StateSet, ARgorithmError, ARgorithmStructure
from ARgorithmToolkit.encoders import serialize

def check_dimensions(data):
    """This function is an internal function that helps verify the dimensions
    of array from user input.

    Args:
        data : data is a multi-dimensional list or tuple

    Raises:
        ARgorithmError: if data is not of correct format , it raises an ARgorithmError
    """
    if not isinstance(data,list) and not isinstance(data,tuple):
        return 1
    check = -1
    try:
        for x in data:
            if check == -1:
                check = check_dimensions(x)
            else:
                assert check == check_dimensions(x)
        return len(data)
    except Exception as ex:
        raise ARgorithmError('please pass array of fixed dimensions') from ex


class ArrayState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.array.Array`` object.

    Attributes:

        name (str) : Name of the object for which the states are generated
        _id (str) : id of the object for which the states are generated
    """
    def __init__(self,name,_id):
        self.name = name
        self._id = _id

    def array_declare(self,body,comments=""):
        """Generates the `array_declare` state when an instance of Array class
        is created.

        Args:
            body: The contents of the array that are to be sent along with the state
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``array_declare`` state for the respective array mentioned
        """
        state_type = "array_declare"
        state_def = {
            "id": self._id,
            "variable_name" : self.name,
            "body" : body.tolist()
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def array_iter(self,body,index,value=None,last_value=None,comments=""):
        """Generates the `array_iter` state when a particular index of array
        has been accessed.

        Args:
            body: The contents of the array that are to be sent along with the state
            index : The index of array that has been accessed
            value (optional): The current value at array[index] if __setitem__(self, key, value) was called.
            last_value (optional): The current value at array[index] if __setitem__(self, key, value) was called.
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``array_iter`` state for the respective array mentioned
        """
        state_type = "array_iter"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.tolist(),
            "index" : index
        }
        if not (last_value is  None):
            state_def["value"] = value
            state_def["last_value"] = last_value
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def array_swap(self,body,indexes,comments=""):
        """Generates the ``array_swap`` state when values at two indexes of
        array are being swapped.

        Args:
            body: The contents of the array that are to be sent along with the state
            indexes : The indexes that are supposed to be swapped
            comments (optional):The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``array_swap`` state for the respective array mentioned
        """
        state_type = "array_swap"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.tolist(),
            "index1" : indexes[0],
            "index2" : indexes[1]
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def array_compare(self,body,indexes,comments=""):
        """Generates the ``array_compare`` state when values at two indexes of
        array are being compared.

        Args:
            body: The contents of the array that are to be sent along with the state
            indexes : The indexes that are supposed to be compared
            comments (optional):The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``array_compare`` state for the respective array mentioned
        """
        state_type = "array_compare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.tolist(),
            "index1" : indexes[0],
            "index2" : indexes[1]
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

class ArrayIterator:
    """This class is a generator that is returned each time an array has to be
    iterated.

    Yields:
        element of Array

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.array.Array
    """
    def __init__(self,array):
        assert isinstance(array,Array)
        self.array = array
        self._index = 0
        self.size = len(array)

    def __next__(self):
        if self._index == self.size:
            raise StopIteration
        v = self.array[self._index]
        self._index += 1
        return v

@serialize
class Array(ARgorithmStructure):
    """The Array class used to emulate multidimensional arrays that can be
    rendered in the ARgorithm Application as series of blocks.

    Attributes:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of Array Class
        data (list or tuple,optional): The value of array if user wants a predefined value. Defaults to None.
        shape (tuple,optional): The shape of the array. Neccessary if data is not given. Gets overwritten if data is given.
        fill (dtype,optional): Neccessary if shape is given. Fills the array with the fill character. Defaults to 0.
        dtype (type,optional): Datatype of array element.
        comments (str,optional): Description of instance of array and its applications that will be rendered during the ``array_declare`` state.

    Raises:
        ARgorithmError: raised if name is not given or Stateset if not provided

    Examples:
        This is an example of array being declared using predefined values.

        >>> algo = ARgorithmToolkit.StateSet()
        >>> test_data = [[1,2,3],[4,5,6]]
        >>> arr = ARgorithmToolkit.Array(name='arr',algo=algo,data=test_data)
        >>> arr
        Array([[1, 2, 3],[4, 5, 6]])

        This is an example of array being declared with shape and fill

        >>> algo = ARgorithmToolkit.StateSet()
        >>> arr = ARgorithmToolkit.Array(name='arr',algo=algo,shape=(2,3),fill=7)
        >>> arr
        Array([[7, 7, 7],[7, 7, 7]])

        The array generated supports all the functionality of regular array

        >>> len(arr)
        2
        >>> arr.shape()
        (2,3)
        >>> arr[1]
        Array([7, 7, 7])
        >>> arr[1][2]
        7
        >>> arr[1,2]
        7
        >>> for subarr in arr:
        ...     for elem in subarr:
        ...             print(elem)
        7
        7
        7
        7
        7
        7
    """
    def __init__(self, name:str, algo:StateSet, data=None, shape=None, fill=0, dtype=int, comments=""):
        try:
            assert isinstance(name,str)
            self.state_generator = ArrayState(name, str(id(self)))
        except Exception as ex:
            raise ARgorithmError('Give valid name to data structure') from ex
        try:
            assert isinstance(algo, StateSet)
            self.algo = algo
        except Exception as ex:
            raise ARgorithmError("array structure needs a reference of template to store states") from ex

        if data is not None:
            check_dimensions(data)
            self.body = np.array(data)
            self.dtype = self.body.dtype
            state = self.state_generator.array_declare(self.body,comments)
            self.algo.add_state(state)
            return


        self.dtype = dtype
        self.body = np.full(fill_value = fill, shape=shape, dtype=dtype)

        state = self.state_generator.array_declare(self.body,comments)
        self.algo.add_state(state)

    def __len__(self):
        """returns length of array when processed by len() function.

        Returns:
            int: length of array or first dimension of array if it is multidimensional

        Example:
            >>> len(arr)
            2
        """
        return len(self.body)

    def shape(self):
        """Get shape of array. As shown in above example.

        Returns:
            tuple: shape of array as a tuple

        Example:
            >>> arr.shape()
            (2,3)
        """
        return (self.body.shape) if isinstance(self.body.shape,tuple) else self.body.shape

    def __getitem__(self, key, comments=""):
        """overloading the item access operator to generate states and create
        more instances of ARgorithmToolkit Array if subarray is accessed.

        Args:
            key (index or slice):
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Raises:
            ARgorithmError: Raised if key is invalid

        Returns:
            element or subarray: depending on key , the returned object can be an element or an sub-array

        Examples:
            >>> arr[1,2]
            6
        """
        try:
            if isinstance(key,slice):
                name = f"{self.state_generator.name}_sub"
                return Array(name=name , algo=self.algo , data=self.body[key] , comments=comments)

            if isinstance(key,int) and len(self.body.shape)==1:
                state = self.state_generator.array_iter(body=self.body, index=key, comments=comments)
                self.algo.add_state(state)
                return self.body[key]


            if isinstance(key,int) or len(key) < len(self.shape()):
                name = f"{self.state_generator.name}_sub"
                state = self.state_generator.array_iter(body=self.body, index=key, comments=comments)
                self.algo.add_state(state)
                return Array(name=name, algo=self.algo, data=self.body[key], comments=comments)

            state = self.state_generator.array_iter(body=self.body, index=key, comments=comments)
            self.algo.add_state(state)
            return self.body[key]
        except Exception as ex:
            raise ARgorithmError(f"invalid index error : {str(ex)}") from ex

    def __setitem__(self, key, value):
        """Overload element write operation to trigger state.

        Args:
            key (index): index where element is written
            value (dtype): value of element that is written

        Example:
            >>> arr
            Array([[1, 2, 3],[4, 5, 6]])
            >>> arr[1,2] = 0
            >>> arr
            Array([[1, 2, 3],[4, 5, 0]])
        """
        last_value = self.body[key]
        self.body[key] = value
        state = self.state_generator.array_iter(body=self.body, index=key, value=value, last_value=last_value, comments=f'Writing {value} at index {key}')
        self.algo.add_state(state)

    def __iter__(self):
        """Generates a iterator object to iterate the array along its first
        dimension.

        Returns:
            ArrayIterator: Iterator object

        Example:
            >>> [x for x in arr]
            [[1,2,3],[4,5,6]]
        """
        return ArrayIterator(self)

    def compare(self,index1,index2,func=None,comments=""):
        """compares elements at 2 indexes of array.

        Args:
            index1 (index): The index of first element to be compared
            index2 (index): The index of second element to be compared
            func (function, optional): [description] The comparision function to be used , defaults to difference
            comments (str, optional): Any comments to describe comparision

        Returns:
            Result of comparision operation

        Example:
            >>> arr.compare((0,0),(1,1))
            -4
        """
        item1 = self.body[index1]
        item2 = self.body[index2]
        state = self.state_generator.array_compare(self.body,(index1,index2),comments)
        self.algo.add_state(state)
        if func is None:
            def default_comparator(item1, item2):
                return item1-item2
            func = default_comparator
        return func(item1, item2)

    def swap(self,index1,index2,comments=""):
        """swaps elements at 2 indexes of array.

        Args:
            index1 (index): The index of first element to be swapped
            index2 (index): The index of second element to be swapped
            comments (str, optional): Any comments to describe swap

        Example:
            >>> arr
            Array([[1, 2, 3],[4, 5, 6]])
            >>> arr.swap((0,2),(1,2))
            >>> arr
            Array([[1, 2, 6],[4, 5, 3]])

        Note:
            Do not try to swap subarrays in multidimensional arrays. It will lead to unexpected results
        """
        self.body[index1], self.body[index2] = self.body[index2], self.body[index1]
        state = self.state_generator.array_swap(self.body, (index1, index2) ,comments)
        self.algo.add_state(state)

    def tolist(self):
        """Returns array as multidimensional list.

        Returns:
            list: multidimensional python list containing value of array

        Example:
            >>> arr.tolist()
            [[1,2,3],[4,5,6]]

        Note:
            The list generated is a normal python list so will not listen and store states. If you want to do that , store the list in the ARgorithmToolkit.vector.Vector object
        """
        return self.body.tolist()

    def __str__(self):
        """String conversion for Array.

        Returns:
            str: String describing Array
        """
        return f"Array({self.tolist().__str__()})"

    def __repr__(self):
        """Return representation for shell outputs.

        Returns:
            str: shell representation for array
        """
        return f"Array({self.tolist().__repr__()})"
