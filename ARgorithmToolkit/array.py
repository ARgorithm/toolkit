from ARgorithmToolkit.utils import State, StateSet, ARgorithmError
import numpy as np
# arrayState class to create array related states
# Refer array_schema.yml for understanding states

def check_dimensions(data):
    if type(data) != list and type(data)!= tuple:
        return 1
    else:
        check = -1
        try:
            for x in data:
                if check == -1:
                    check = check_dimensions(x)
                else:
                    assert check == check_dimensions(x)    
            return len(data)
        except:
            raise ARgorithmError('please pass array of fixed dimensions')    


class ArrayState:
    def __init__(self,name):
        self.name = name
    
    
    def array_declare(self,body,comments=""):
        state_type = "array_declare"
        state_def = {
            "variable_name" : self.name,
            "body" : body.tolist()
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def array_iter(self,body,index,comments=""):
        state_type = "array_iter"
        state_def = {
            "variable_name" : self.name,
            "body" : body.tolist(),
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def array_swap(self,body,indexes,comments=""):
        state_type = "array_swap"
        state_def = {
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
        state_type = "array_compare"
        state_def = {
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
    
    def __init__(self,array):
        assert type(array) == Array
        self.array = array
        self._index = 0
        self.size = len(array)

    def __next__(self):
        if self._index == self.size:
            raise StopIteration
        else:
            v = self.array[self._index]
            self._index += 1
            return v

# array class is an template for arrays to be used
class Array:    
    
    def __init__(self, name, algo, data=None, shape=None, fill=0, dtype=int, comments=""):
        try:
            assert type(name)==str 
            self.state_generator = ArrayState(name)
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == StateSet 
            self.algo = algo
        except:
            raise ARgorithmError("array structure needs a reference of template to store states")
        
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
        return len(self.body)

    def shape(self):
        return (self.body.shape) if type(self.body.shape) != tuple else self.body.shape

    # to give support for array indexing and slicing 
    def __getitem__(self, key, comments=""):
        try:
            if type(key) == slice:
                name = f"{self.state_generator.name}_sub"
                return Array(name=name , algo=self.algo , data=self.body[key] , comments=comments)

            if type(key)==int and len(self.body.shape)==1:
                state = self.state_generator.array_iter(self.body, key, comments)
                self.algo.add_state(state)
                return self.body[key]


            if type(key)==int or len(key) < len(self.shape()):
                name = f"{self.state_generator.name}_sub"
                state = self.state_generator.array_iter(self.body, key, comments)
                self.algo.add_state(state)
                return Array(name=name, algo=self.algo, data=self.body[key], comments=comments)
            
            state = self.state_generator.array_iter(self.body, key, comments)
            self.algo.add_state(state)
            return self.body[key]
        except Exception as e:
            raise ARgorithmError(f"invalid index error : {str(e)}")

    def __setitem__(self, key, value):
        self.body[key] = value
        state = self.state_generator.array_iter(self.body, key, comments=f'Writing {value} at index {key}')
        self.algo.add_state(state)

    # to provide iterable interface
    def __iter__(self):
        return iter(self.body)

    # comparision operation with lambda support
    def compare(self,index1,index2,func=None,comments=""):
        item1 = self.body[index1]
        item2 = self.body[index2]
        state = self.state_generator.array_compare(self.body,(index1,index2),comments)
        self.algo.add_state(state)
        if func == None:
            def default_comparator(item1, item2):
                return item1-item2
            func = default_comparator 
        return func(item1, item2)

    # swap operation
    def swap(self,index1,index2,comments=""):
        self.body[index1], self.body[index2] = self.body[index2], self.body[index1]
        state = self.state_generator.array_swap(self.body, (index1, index2) ,comments)
        self.algo.add_state(state)

    def tolist(self):
        return self.body.tolist()
        
    # print format
    def __str__(self):
        return self.body.__str__()

    def __repr__(self):
        return self.body.__repr__()
    
