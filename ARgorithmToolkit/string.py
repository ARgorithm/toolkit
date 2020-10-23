from ARgorithmToolkit.utils import State, StateSet, ARgorithmError
# stringState class to create string related states
# Refer string_schema.yml for understanding states
class StringState:
    def __init__(self, name):
        self.name = name
    
    
    def string_declare(self, body, comments=""):
        state_type = "string_declare"
        state_def = {
            "variable_name" : self.name,
            "body" : body
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def string_iter(self, body, index, comments=""):
        state_type = "string_iter"
        state_def = {
            "variable_name" : self.name,
            "body" : body,
            "index" : index
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def string_append(self, body, element, comments=""):
        state_type = "string_append"
        state_def = {
            "variable_name" : self.name,
            "body" : body,
            "element" : element,
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    


# stringIterator to iterate through string while updating states
class StringIterator:
    
    def __init__(self,string):
        assert type(string) == String
        self.string = string
        self._index = 0
        self.size = len(string)

    def __next__(self):
        if self._index == self.size:
            raise StopIteration
        else:
            v = self.string[self._index]
            self._index += 1
            return v



# string class is an template for strings to be used
class String():    
    def __init__(self,name,algo,body='',comments=""):
        try:
            assert type(name)==str 
            self.state_generator = StringState(name)
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == StateSet 
            self.algo = algo
        except:
            raise ARgorithmError("string structure needs a reference of template to store states")
        try:
            assert type(body) == str
            self.body = body
        except:
            raise ARgorithmError("String body should be of type string")
        state = self.state_generator.string_declare(self.body,comments)
        self.algo.add_state(state)
        
    # overload len function for class
    def __len__(self):
        return len(self.body)

    # to give support for string indexing and slicing 
    def __getitem__(self,key,comments=""):
        if type(key) == slice:
            name = f"{self.state_generator.name}_sub"
            return String(name , self.algo , self.body[key] , comments=f"creating new substring for {key}")
        else:
            state = self.state_generator.string_iter(self.body,key,comments=f"accessing character at {key}")
            self.algo.add_state(state)
            return self.body[key]


    def __setitem__(self, key, value):
        raise TypeError("'String' object does not support item assignment")

    # to provide iterable interface
    def __iter__(self):
        return StringIterator(self)

    def __repr__(self):
        return repr(self.body)
    
    def __str__(self):
        return str(self.body)

    def append(self, value, comments=''):
        if type(value) == String:
            value = value.body
        self.body += value
        state = self.state_generator.string_append(self.body , value, comments) 
        self.algo.add_state(state)

    def __add__(self, value):
        if type(value) == String:
            value = value.body
        name = f"{self.state_generator.name}_super"
        new = String(name=name, algo=self.algo, body=self.body, comments=f'creating new string with {value} appended to the original string')
        new.append(value)
        return new