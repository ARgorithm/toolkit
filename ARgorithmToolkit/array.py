from .utils import *

class ArrayState(State):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        pass

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

class Array:
    
    def __init__(self,name,algo,body=[]):
        try:
            assert type(name)==str 
            self.name = name
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == Template 
            self.algo = algo
        except:
            raise ARgorithmError("Array structure needs a reference of template reference to store states")
        try:
            assert type(body) == list 
            self.body = body
        except:
            raise ARgorithmError("Array body should be list")
    
    def __len__(self):
        return len(self.body)

    def __getitem__(self,key,comment=""):
        if type(key) == slice:
            name = f"{self.name}-sub"
            return Array(name , self.algo , self.body[key])
        else:
            return self.body[key]

    def __iter__(self):
        return ArrayIterator(self)

    def insert(self,value,index=None):
        if index==None:
            self.body.append(value)
        elif index >= 0:
            self.body = self.body[:index] + [value] + self.body[index:]

    def remove(self,value=None,index=None):
        if index==None and value==None:
            self.body.pop()
        elif value==None:
            if index >= 0 and index < len(self):
                self.body = self.body[0:index] + self.body[index+1:]
        elif index==None:
            self.body.remove(value)
        else:
            raise ARgorithmError("Either give only a valid index or only value to be deleted , dont give both")

    def compare(self,index1,index2,func=None):
        item1 = self.body[index1]
        item2 = self.body[index2]
        if func == None:
            return item1 == item2
        else:
            return func(item1,item2)
        
    def swap(self,index1,index2):
        temp = self.body[index1]
        self.body[index1] = self.body[index2]
        self.body[index2] = temp

    def __str__(self):
        return (self.body).__str__()
    # add methods , each method should update algo.states