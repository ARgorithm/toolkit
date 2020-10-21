from ARgorithmToolkit.utils import State, StateSet, ARgorithmError
# StackState class to create stack related states
# Refer stack_schema.yml for understanding states
class StackState():
    
    def __init__(self,name):
        self.name = name

    def stack_declare(self,comments=""):
        state_type = "stack_declare"
        state_def = {
            "variable_name" : self.name,
            "body" : []
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def stack_push(self,body,element,comments=""):
        state_type = "stack_push"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
            "element" : element
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def stack_pop(self,body,comments=""):
        state_type = "stack_pop"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def stack_top(self,body,comments=""):
        state_type = "stack_top"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
# Stack class is an template for Stacks to be used
class Stack:
    
    def __init__(self,name,algo,comments=""):
        try:
            assert type(name)==str 
            self.state_generator = StackState(name)
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == StateSet 
            self.algo = algo
        except:
            raise ARgorithmError("Stack structure needs a reference of template to store states")
        self.body = []
        state = self.state_generator.stack_declare(comments)
        self.algo.add_state(state)

    def __len__(self):
        return len(self.body)
    
    def empty(self):
        return len(self)==0

    def push(self,element,comments=""):
        self.body.append(element)
        state = self.state_generator.stack_push(self.body,element,comments)
        self.algo.add_state(state)

    def pop(self,comments=""):
        if self.empty():
            raise ARgorithmError('Stack is empty')
        item = self.body[-1]
        self.body.pop()
        state = self.state_generator.stack_pop(self.body,comments)
        self.algo.add_state(state)
        return item

    def top(self,comments=""):
        if self.empty():
            raise ARgorithmError('Stack is empty')
        item = self.body[-1]
        state = self.state_generator.stack_top(self.body,comments)
        self.algo.add_state(state)
        return item


        