"""The set module provides support for set data structure for the Toolkit. It
stores keys and avoid duplication. Provides O(1) average case and O(n)
amortized worst case complexity for element lookup. The main class in this
module is the Set class. The other classes act as support class to Set class.
For this reason the Set class can directly be imported from the
ARgorithmToolkit library without having to import from the set module :

    >>> set1 = ARgorithmToolkit.Set(name='set1',algo=algo,data=data)
    >>> set1 = ARgorithmToolkit.set.Set(name='set1',algo=algo,data=data)
"""

from numpy.lib.function_base import iterable
from numpy import generic
from ARgorithmToolkit.utils import ARgorithmHashable, State, StateSet, ARgorithmError, ARgorithmStructure
from ARgorithmToolkit.encoders import serialize

class SetState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.set.Set`` object.

    Attributes:

        name (str) : Name of the object for which the states are generated
        _id (str) : id of the object for which the states are generated
    """
    def __init__(self,name,_id):
        self.name = name
        self._id = _id

    def set_declare(self, body, comments="") -> State:
        """Generates the `set_declare` state when an instance of Set class is
        created.

        Args:
            body: The contents of the set that are to be sent along with the state
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``set_declare`` state for the respective set mentioned
        """
        state_type = "set_declare"
        state_def = {
            "id": self._id,
            "variable_name" : self.name,
            "body" : body.copy()
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def set_add(self, body, key, comments="") -> State:
        """Generates the `set_add` state when a particular key is add.

        Args:
            body : The contents of the set that are to be sent along with the state
            key : The key that has been added
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``set_add`` state for the respective set mentioned
        """
        state_type = "set_add"
        state_def = {
            "id": self._id,
            "variable_name" : self.name,
            "key" : key,
            "body" : body.copy()
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )


    def set_remove(self,body,key,comments="") -> State:
        """Generates the `set_remove` state when a particular key is deleted.

        Args:
            body : The contents of the set that are to be sent along with the state
            key : The key that has been deleted
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``set_remove`` state for the respective set mentioned
        """
        state_type = "set_remove"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.copy(),
            "key" : key,
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def set_find(self, body, key, found, comments="") -> State:
        """Generates the `set_find` state when a particular key is searched
        for.

        Args:
            body : The contents of the set that are to be sent along with the state
            key : The key that has been searched
            found : true if found false if not found
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``set_find`` state for the respective set mentioned
        """
        state_type = "set_find"
        state_def = {
            "id": self._id,
            "variable_name" : self.name,
            "key" : key,
            "found": found,
            "body" : body.copy()
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

@serialize
class Set(ARgorithmStructure):
    """The Set class used to emulate set datastructure that can be rendered in
    the ARgorithm Application as series of unique keys.

    Attributes:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of Set Class
        data (Vector, Array) : to generate set from an existent list
        comments (str,optional): Description of instance of set and its applications that will be rendered during the ``set_declare`` state.

    Raises:
        ARgorithmError: raised if name is not given or Stateset if not provided

    Examples:
        This is an example of set being declared

        >>> algo = ARgorithmToolkit.StateSet()
        >>> set1 = ARgorithmToolkit.Set(name='set1',algo=algo,data=[1,2,3,4,4,2,1])
        >>> set1
        Set({1,2,3,4})

        The set generated supports all the functionality of default set

        >>> len(set1)
        4
        >>> set1.find(2)
        True
        >>> set1.add("s")
        >>> set1
        Set({1, 2, 3, 4, "s"})
        >>> for key in set1:
        ...    print(key)
        1
        2
        3
        4
        5
        "s"
        >>> set1.remove("s")
        >>> set1
        Set({1, 2, 3, 4})
    """

    def __init__(self, name:str, algo:StateSet, data:iterable=None, comments= ""):
        try:
            assert isinstance(name, str)
            self.state_generator = SetState(name, str(id(self)))
        except Exception as ex:
            raise ARgorithmError('Give valid name to data structure') from ex
        try:
            assert isinstance(algo, StateSet)
            self.algo = algo
        except Exception as ex:
            raise ARgorithmError("Set structure needs a reference of template to store states") from ex

        self.body = set()
        if data:
            for x in data:
                if isinstance(x, ARgorithmHashable):
                    self.body.add(x.to_json())
                elif isinstance(x, (int,str,bool,float,generic)):
                    self.body.add(x)
                else:
                    raise TypeError("Invalid key error : Please provide data with ARgorithmHashable type or (int, float, bool, str)")
        self.__working_set = set(data) if data else set()
        state = self.state_generator.set_declare(self.body, comments=comments)
        self.algo.add_state(state)

    def __len__(self) -> int:
        """returns size of Set when processed by len() function.

        Returns:
            int: size of the set

        Example:
            >>> set1
            Set({1,2,3})
            >>> len(set1)
            3
        """
        return len(self.__working_set)


    def add(self, key, comments=""):
        """Adds a unique key to the set.
        Args:
            key (ARgorithmStructure or (int, str, float, bool)) : key to add to the set
            comments (str, optional): Comments for descriptive purpose. Defaults to "".
        Example:
        >>> set1
        Set({1,2})
        >>> set1.add('abc')
        Set({1,2,'abc'})
        >>> set1.add(1)
        >>> set1
        Set({1,2,'abc'})
        """
        try:
            assert isinstance(key,(ARgorithmHashable,int,bool,str,float))
        except AssertionError as ae:
            raise TypeError("Invalid key error : Please provide data with ARgorithmHashable type or (int, float, bool, str)") from ae
        if isinstance(key, ARgorithmHashable):
            self.body.add(key.to_json())
        else:
            self.body.add(key)

        self.__working_set.add(key)
        state = self.state_generator.set_add(self.body, key,comments)
        self.algo.add_state(state)


    def remove(self, key, comments=""):
        """removes the key from the set
        Args:
            key (ARgorithmStructure or (int, str, float, bool)) : key to remove from the set
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> set1
            Set({1,2,3})
            >>> set1.remove(1)
            >>> set1
            Set({2,3})
        """
        try:
            if isinstance(key, ARgorithmHashable):
                self.body.remove(key.to_json())
            else:
                self.body.remove(key)
            self.__working_set.remove(key)
            state = self.state_generator.set_remove(self.body, key,comments)
            self.algo.add_state(state)
        except Exception as e:
            raise ARgorithmError(f"Invalid Key Error : {str(e)}") from e

    def find(self, key, comments="") -> bool:
        """finds if a key is present in the set
        Args:
            key (ARgorithmStructure or (int, str, float, bool)) : key to find in the set
            comments (str, optional): Comments for descriptive purpose. Defaults to "".
        Returns:
            bool : true if key found else false

        Example:
            >>> set1
            Set({1,2,"abc"})
            >>> set1.find("abc")
            True
            >>> set1.find("abcd")
            False
        """
        found = key in self.__working_set
        state = self.state_generator.set_find(self.body, key, found,comments)
        self.algo.add_state(state)
        return found


    def intersection(self, other, comments="") :
        """Creates a new set with the intersection of the calling set with the set in the arguments provided
        Args:
            other (Set) : set to find the intersection with
            comments (str, optional): comments for descriptive purpose. Defaults to "".

        returns:
            Set : intersection of self and other

        example:
            >>> set1
            Set({1,2})
            >>> set2
            Set({2,3,4})
            >>> set1.intersection(set2)
            Set({2})
        """
        if not comments:
            comments = f"Creating new set with intersection of {self.state_generator.name} and {other.state_generator.name}"
        intersect_data = self.__working_set.intersection(other.__working_set) # pylint: disable=protected-access
        intersect_name = f"{self.state_generator.name}_intersection_{other.state_generator.name}"
        intersect = Set(intersect_name, self.algo, intersect_data, comments=comments)
        return intersect

    def union(self, other, comments="") :
        """Creates a new set with the union of the calling set with the set in the arguments provided
        Args:
            other (Set) : set to find the union with
            comments (str, optional): comments for descriptive purpose. Defaults to "".

        returns:
            Set : union of self and other

        example:
            >>> set1
            Set({1,2})
            >>> set2
            Set({2,3,4})
            >>> set1.union(set2)
            Set({1,2,3,4})
        """
        if not comments:
            comments = f"Creating new set with union of {self.state_generator.name} and {other.state_generator.name}"
        union_data = self.__working_set.union(other.__working_set) # pylint: disable=protected-access
        union_name = f"{self.state_generator.name}_union_{other.state_generator.name}"
        _union = Set(union_name, self.algo, union_data, comments=comments)
        return _union

    def difference(self, other, comments="") :
        """Creates a new set with the difference of the calling set with the set in the arguments provided
        Args:
            other (Set) : set to find the difference with
            comments (str, optional): comments for descriptive purpose. Defaults to "".

        returns:
            Set : difference of self and other

        example:
            >>> set1
            Set({1,2})
            >>> set2
            Set({2,3,4})
            >>> set1.difference(set2)
            Set({1})
        """
        if not comments:
            comments = f"Creating new set with difference of {self.state_generator.name} and {other.state_generator.name}"
        diff_data = self.__working_set.difference(other.__working_set) # pylint: disable=protected-access
        diff_name = f"{self.state_generator.name}_difference_{other.state_generator.name}"
        diff = Set(diff_name, self.algo, diff_data, comments=comments)
        return diff

    def __repr__(self) -> str:
        """Return representation for shell outputs.

        Returns:
            str: shell representation for Set
        """
        empty = "{}"
        return f"Set({self.__working_set.__repr__() if len(self.__working_set) > 0 else empty})"

    def __str__(self) -> str:
        """Return string conversion for Set.

        Returns:
            str: string conversion for Set
        """
        empty = "{}"
        return f"Set({self.__working_set.__str__() if len(self.__working_set) > 0 else empty})"
