from ARgorithmToolkit.utils import *

class ArrayState(State):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        pass

class Array():

    def __init__(self,algo,body=[]):
        try:
            assert type(algo) == ARgorithmToolkit.Template 
            self.algo = algo
        except:
            raise ARgorithmError("Array structure needs a reference of template reference to store states")
        try:
            assert type(body) == list 
            self.body = body
        except:
            raise ARgorithmError("Array body should be list")

    # add methods , each method should update algo.states