"""Testing JSON Encoder for ARgorithm containers
"""
import json
import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
arr = arr = ARgorithmToolkit.Array(name='arr',algo=algo,data=[1,2,3])
dllnode = ARgorithmToolkit.DoublyLinkedListNode(algo,7)
dll = ARgorithmToolkit.DoublyLinkedList("dllnode",algo)
dl = ARgorithmToolkit.List("dl",algo)
llnode = ARgorithmToolkit.LinkedListNode(algo,7)
ll = ARgorithmToolkit.LinkedList("llnode",algo,llnode)
fl = ARgorithmToolkit.ForwardList("fl",algo)
pq = ARgorithmToolkit.PriorityQueue(name="pq",algo=algo)
q = ARgorithmToolkit.Queue(name="q",algo=algo)
st = ARgorithmToolkit.stack.Stack(name="st",algo=algo)
s = ARgorithmToolkit.string.String(name="s",algo=algo,body="hello world")
vec = ARgorithmToolkit.Vector(name='vec',algo=algo)

def test_encoder():
    """Tests serializability of all classes
    """
    objects = [
        arr,dllnode,dll,dl,ll,llnode,fl,pq,q,s,vec,st
    ]
    json_string = json.dumps(objects,cls=ARgorithmToolkit.encoders.StateEncoder)
    parsed_objects = json.loads(json_string)
    for serialized,actual in zip(parsed_objects,objects):
        modulename,classname_id = serialized.split('.')
        try:
            assert modulename == "$ARgorithmToolkit"
            classname,obj_id = classname_id.split(':')
            assert classname == actual.__class__.__name__
            assert int(obj_id) == id(actual)
        except AssertionError as ae:
            if actual.__class__.__name__ == "Variable":
                pass
            raise Exception from ae
        try:
            json.dumps(algo,cls=ARgorithmToolkit.encoders.StateEncoder)
            raise AssertionError("Should have raised type error")
        except TypeError:
            pass
