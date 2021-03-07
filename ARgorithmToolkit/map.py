"""The map module provides support for hash-map or dictionary data structure
for the Toolkit. It maps key to a value provided. Provides O(1) average case
and O(n) amortized worst case complexity for element lookup. The main class in
this module is the Map class. The other classes act as support class to Map
class. For this reason the Map class can directly be imported from the
ARgorithmToolkit library without having to import from the map module :

    >>> map = ARgorithmToolkit.Map(name='map',algo=algo)
    >>> map = ARgorithmToolkit.map.Map(name='map',algo=algo)
"""

from ARgorithmToolkit.utils import ARgorithmHashable, State, StateSet, ARgorithmError, ARgorithmStructure
from ARgorithmToolkit.encoders import serialize

class MapState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.map.Map`` object.

    Attributes:

        name (str) : Name of the object for which the states are generated
        _id (str) : id of the object for which the states are generated
    """
    def __init__(self,name,_id):
        self.name = name
        self._id = _id

    def map_declare(self, body, comments="") -> State:
        """Generates the `map_declare` state when an instance of Map class is
        created.

        Args:
            body: The contents of the map that are to be sent along with the state
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``map_declare`` state for the respective map mentioned
        """
        state_type = "map_declare"
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

    def map_get(self,body,key,value,comments="") -> State:
        """Generates the `map_get` state when a particular key is looked up.

        Args:
            body : The contents of the map that are to be sent along with the state
            key : The key that has been accessed
            value : The current value associated with key
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``map_get`` state for the respective map mentioned
        """
        state_type = "map_get"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.copy(),
            "key" : key,
            "value" : value
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def map_set(self,body,key,value,last_value=None,comments="") -> State:
        """Generates the `map_set` state when a particular key is set for a new
        value.

        Args:
            body : The contents of the map that are to be sent along with the state
            key : The key that has been accessed
            value : The current value being associated with key
            last_value (optional): the last value that the key was associated to.
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``map_set`` state for the respective map mentioned
        """
        state_type = "map_set"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.copy(),
            "key" : key,
            "value" : value,
            "last_value" : last_value
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )


    def map_remove(self,body,key,value,comments="") -> State:
        """Generates the `map_remove` state when a particular key is deleted.

        Args:
            body : The contents of the map that are to be sent along with the state
            key : The key that has been deleted
            value : The value associated with key
            comments (optional): The comments that are supposed to rendered with the state for descriptive purpose. Defaults to "".

        Returns:
            ARgorithmToolkit.utils.State: returns the ``map_remove`` state for the respective map mentioned
        """
        state_type = "map_remove"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "body" : body.copy(),
            "key" : key,
            "value" : value,
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

class MapIterator:
    """This class is a generator that is returned each time an map has to be
    iterated.

    Yields:
        Tuple(key,value) of Map

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.map.Map
    """
    def __init__(self,_map):
        assert isinstance(_map,Map)
        self.map = _map
        self.size = len(_map)
        self.index = 0
        self.keys = list(self.map.keys())
        self.values = list(self.map.values())

    def __next__(self) -> tuple:
        if self.index == self.size:
            raise StopIteration
        k = self.keys[self.index]
        v = self.values[self.index]
        self.index += 1
        return k,v

@serialize
class Map(ARgorithmStructure):
    """The Map class used to emulate hash-maps/dictionaries that can be
    rendered in the ARgorithm Application as series of key/value pairs.

    Attributes:
        name (str): name given to the rendered block in augmented reality. Essential. Should not be altered after initialisation
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of Map Class
        comments (str,optional): Description of instance of map and its applications that will be rendered during the ``map_declare`` state.

    Raises:
        ARgorithmError: raised if name is not given or Stateset if not provided

    Examples:
        This is an example of map being declared

        >>> algo = ARgorithmToolkit.StateSet()
        >>> map = ARgorithmToolkit.Map(name='map',algo=algo)
        >>> map
        Map({})

        The map generated supports all the functionality of regular dictionary

        >>> len(map)
        0
        >>> map["hello"] = 2
        >>> map["hello"]
        2
        >>> map[3] = "s"
        >>> map
        Map({"hello":2, 3:"s"})
        >>> for key,value in map:
        ...     print(key, value)
        hello 2
        3 s
        >>> del map[3]
        >>> map
        Map({"hello":2})
    """

    def __init__(self, name:str, algo:StateSet, comments:str = ""):
        try:
            assert isinstance(name, str)
            self.state_generator = MapState(name, str(id(self)))
        except Exception as ex:
            raise ARgorithmError('Give valid name to data structure') from ex
        try:
            assert isinstance(algo, StateSet)
            self.algo = algo
        except Exception as ex:
            raise ARgorithmError("Map structure needs a reference of template to store states") from ex

        self.body = {}
        self.__working_dict = {}
        state = self.state_generator.map_declare(self.body,comments)
        self.algo.add_state(state)


    def __len__(self) -> int:
        """returns size of Map when processed by len() function.

        Returns:
            int: size of the map

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> len(map)
            2
        """
        return len(self.__working_dict)

    def __getitem__(self, key) -> any:
        """returns the value associated with 'key' in the Map
        Args:
            key (ARgorithmStructure or (int, str, float, bool)): key to lookup in dict
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            obj: value associated with the key provided

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> map["abc"]
            2
        """
        try:
            _value = self.__working_dict[key]
            value = None
            if isinstance(key, ARgorithmHashable):
                value = self.body[key.to_json()]
            else:
                value = self.body[key]
            state = self.state_generator.map_get(body=self.body, key=key, value=value, comments="")
            self.algo.add_state(state)
            return _value
        except Exception as e:
            raise ARgorithmError(f"Invalid Key Error : {str(e)}") from e


    def get(self, key, default=None, comments="") -> any:
        """returns the value associated with 'key' in the Map without raising key error
        Args:
            key (ARgorithmStructure or (int, str, float, bool)) : key to lookup in dict
            default : return a default value for non-existent key instead of raising an error
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            obj: value associated with the key provided

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> map.get("xyz", -1) #get usage
            -1
            >>> map.get("xyz") is None
            True
        """
        try:
            _value = self.__working_dict[key]
            state = self.state_generator.map_get(body=self.body, key=key, value=_value, comments=comments)
            self.algo.add_state(state)
            return _value
        except KeyError:
            state = self.state_generator.map_get(body=self.body, key=key, value=default if default else "none", comments=f"key not found. value efaulted to {default}")
            self.algo.add_state(state)
            return default

    def set(self, key, value, comments=""):
        """sets a value mapped to a given key in the Map
        Args:
            key (ARgorithmStructure or (int, str, float, bool)) : key to set in the dict
            value (ARgorithmStructure of (int, str, float, bool)) : value to set in the dict
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> map.set("xyz, 5) #__setitem__ usage
            >>> map.get("xyz", -1)
            5
            >>> map["xyz"]
            5
        """
        assert isinstance(key,(ARgorithmHashable, int, str, float, bool)), f"Invalid key : key cannot be any type other than (ARgorithmHashable, int, str, float, bool), {type(key).__name__} is not hashable."
        assert isinstance(value,(ARgorithmStructure, int, str, float, bool)), "Invalid value : value cannot be set to any type other than (ARgorithmStructure, int, str, float, bool)"
        last_value = self.body.get(key, "none")
        self.__working_dict[key] = value
        if isinstance(key, (str, int, float, bool)) and isinstance(value, (str, int, float, bool)):
            self.body[key] = value
        elif isinstance(key, (str, int, float, bool)):
            self.body[key] = value.to_json()
        elif isinstance(value, (str, int, float, bool)):
            self.body[key.to_json()] = value
        else:
            self.body[key.to_json()] = value.to_json()

        state = self.state_generator.map_set(body=self.body, key=key, value=value, last_value=last_value, comments=comments)
        self.algo.add_state(state)


    def __setitem__(self, key, value, comments=""):
        """sets a value mapped to a given key in the Map
        Args:
            key (ARgorithmStructure or (int, str, float, bool)) : key to set in the dict
            value (ARgorithmStructure of (int, str, float, bool)) : value to set in the dict
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> map["xyz"] = 5 #__setitem__ usage
            >>> map.get("xyz", -1)
            5
            >>> map["xyz"]
            5
        """
        assert isinstance(key,(ARgorithmHashable, int, str, float, bool)), f"Invalid key : key cannot be any type other than (ARgorithmHashable, int, str, float, bool), {type(key).__name__} is not hashable."
        assert isinstance(value,(ARgorithmStructure, int, str, float, bool)), "Invalid value : value cannot be set to any type other than (ARgorithmStructure, int, str, float, bool)"
        last_value = self.body.get(key, "none")
        self.__working_dict[key] = value
        if isinstance(key, (str, int, float, bool)) and isinstance(value, (str, int, float, bool)):
            self.body[key] = value
        elif isinstance(key, (str, int, float, bool)):
            self.body[key] = value.to_json()
        elif isinstance(value, (str, int, float, bool)):
            self.body[key.to_json()] = value
        else:
            self.body[key.to_json()] = value.to_json()

        state = self.state_generator.map_set(body=self.body, key=key, value=value, last_value=last_value, comments="")
        self.algo.add_state(state)

    def __iter__(self):
        """Generates a iterator object to iterate the map key/value pairs.

        Returns:
            MapIterator: Iterator object

        Example:
            >>> map
            Map({"abc":3, "efg":4})
            >>> [x for x in map]
            [("abc",3),("efg",4)]
        """
        return MapIterator(self)

    def __delitem__(self, key):
        """deletes the entry associated with 'key' in the Map
        Args:
            key (ARgorithmHashable or (int, str, float, bool)) : key to lookup in dict
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> del map["abc"] # __delitem__ usage
            >>> map
            Map({"efg":3})
        """
        try:
            value = None
            if isinstance(key, ARgorithmHashable):
                value = self.body[key.to_json()]
                del self.body[key.to_json()]
            else:
                value = self.body[key]
                del self.body[key]

            del self.__working_dict[key]
            state = self.state_generator.map_remove(self.body, key, value, "")
            self.algo.add_state(state)

        except Exception as e:
            raise ARgorithmError(f"Invalid Key Error : {str(e)}") from e

    def remove(self, key, comments=""):
        """deletes the entry associated with 'key' in the Map without raising an error
        Args:
            key (ARgorithmHashable or (int, str, float, bool)) : key to lookup in dict
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Example:
            >>> map
            Map({"abc":2, "efg":3})
            >>> map.remove("abc")
            >>> map
            Map({"efg":3})
            >>> map.remove("abc")
            >>> map
            Map({"efg":3})
        """
        try:
            value = None
            if isinstance(key, ARgorithmHashable):
                value = self.body[key.to_json()]
                del self.body[key.to_json()]
            else:
                value = self.body[key]
                del self.body[key]

            del self.__working_dict[key]
            state = self.state_generator.map_remove(self.body, key, value, comments)
            self.algo.add_state(state)

        except KeyError:
            state = self.state_generator.map_remove(self.body, key, "none", "key not found, nothing removed.")
            self.algo.add_state(state)
            return

    def __repr__(self) -> str:
        """Return representation for shell outputs.

        Returns:
            str: shell representation for Map
        """
        return f"Map({self.__working_dict.__repr__()})"

    def __str__(self) -> str:
        """Return string conversion for map.

        Returns:
            str: string conversion for Map
        """
        return f"Map({self.__working_dict.__str__()})"

    def keys(self):
        """Returns a list of key entries in the map.

        Returns:
            list: list of keys
        """

        return self.__working_dict.keys()

    def values(self):
        """Returns a list of values in the map.

        Returns:
            list: list of values
        """

        return self.__working_dict.values()
