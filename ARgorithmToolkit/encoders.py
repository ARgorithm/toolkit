"""For support of nested ARgorithm Classes, this module provides with a Encoder that stores the reference to ARgorithm Object
whenever an ARgorithm Class object is serialized in the StateSet (which only happens when we nest one ARgorithm Class in another)
"""
import inspect
from json import JSONEncoder
import ARgorithmToolkit

def serialize(cls):
    """Decorator to make classes serializable
    """
    def to_json(self):
        """Creates a string representing a reference to ARgorithmObject for use in application
        """
        class_name = type(self).__name__
        obj_id = id(self)
        return f"$ARgorithmToolkit.{class_name}:{obj_id}"
    setattr(cls,'to_json',to_json)
    return cls

class StateEncoder(JSONEncoder):
    """The custon Encoder to be used to convert StateSet into JSON. Supports ARgorithm Classes as well
    """
    def default(self, o):
        """The function called when an object has to be serialized

        Args:
            o ([type]): The object to be serialized
        """
        classes = inspect.getmembers(ARgorithmToolkit,inspect.isclass)
        classes = tuple([x for _,x in classes])
        if isinstance(ARgorithmToolkit.Variable,classes) :
            return super().default(o.value)
        elif isinstance(o, classes):
            try:
                return o.to_json()
            except Exception as ex:
                raise TypeError("Unserializable ARgorithm class",) from ex
        return super().default(o)
