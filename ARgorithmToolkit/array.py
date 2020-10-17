from ARgorithmToolkit.utils import *

# ArrayState class to create Array related states
# Refer array_schema.yml for understanding states
class ArrayState:
    def __init__(self,name):
        self.name = name
    
    
    def array_declare(self,body,comments=""):
        state_type = "array_declare"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body]
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
            "body" : [x for x in body],
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def array_remove(self,body,index , comments=""):
        state_type = "array_remove"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def array_insert(self,body,element,index,comments=""):
        state_type = "array_insert"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
            "element" : element,
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
            "body" : [x for x in body],
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
            "body" : [x for x in body],
            "index1" : indexes[0],
            "index2" : indexes[1]
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )


# ArrayIterator to iterate through Array while updating states
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



# Array class is an template for Arrays to be used
class Array:    
    def __init__(self,name,algo,body=[],comments=""):
        try:
            assert type(name)==str 
            self.state_generator = ArrayState(name)
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == StateSet 
            self.algo = algo
        except:
            raise ARgorithmError("Array structure needs a reference of template to store states")
        try:
            assert type(body) == list 
            self.body = body
        except:
            raise ARgorithmError("Array body should be list")
        state = self.state_generator.array_declare(self.body,comments)
        self.algo.add_state(state)
        
    # overload len function for class
    def __len__(self):
        return len(self.body)

    # to give support for array indexing and slicing 
    def __getitem__(self,key,comments=""):
        if type(key) == slice:
            name = f"{self.state_generator.name}-sub"
            return Array(name , self.algo , self.body[key] , comments)
        else:
            state = self.state_generator.array_iter(self.body,key,comments)
            self.algo.add_state(state)
            return self.body[key]

    # to provide iterable interface
    def __iter__(self):
        return ArrayIterator(self)

    # insertion operation
    def insert(self,value,index=None,comments=""):
        if index==None:
            self.body.append(value)
            state = self.state_generator.array_insert(self.body , value , len(self) , comments) 
            self.algo.add_state(state)
        elif index >= 0:
            self.body = self.body[:index] + [value] + self.body[index:]
            state = self.state_generator.array_insert(self.body , value , index , comments) 
            self.algo.add_state(state)

    # deletion operation
    def remove(self,value=None,index=None,comments=""):
        if index==None and value==None:
            self.body.pop()
            state = self.state_generator.array_remove(self.body,len(self)-1,comments)
            self.algo.add_state(state)
        elif value==None and index >= 0 and index < len(self):
            self.body = self.body[0:index] + self.body[index+1:]
            state = self.state_generator.array_remove(self.body,index,comments)
            self.algo.add_state(state)
        elif index==None:
            index = self.body.index(value)
            self.body.remove(value)
            state = self.state_generator.array_remove(self.body,index,comments)
            self.algo.add_state(state)
        else:
            raise ARgorithmError("Either give only a valid index or only value to be deleted , dont give both")

    # comparision operation with lambda support
    def compare(self,index1,index2,func=None,comments=""):
        item1 = self.body[index1]
        item2 = self.body[index2]
        state = self.state_generator.array_compare(self.body,(index1,index2),comments)
        self.algo.add_state(state)
        if func == None:
            return item1 == item2
        else:
            return func(item1,item2)

    # swap operation
    def swap(self,index1,index2,comments=""):
        temp = self.body[index1]
        self.body[index1] = self.body[index2]
        self.body[index2] = temp
        state = self.state_generator.array_swap(self.body,(index1,index2),comments)
        self.algo.add_state(state)
        
    # print format
    def __str__(self):
        return self.body.__str__()
    