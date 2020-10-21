from ARgorithmToolkit.utils import State, StateSet, ARgorithmError
# QueueState class to create queue related states
# Refer queue_schema.yml for understanding states
class QueueState():
    
    def __init__(self,name):
        self.name = name

    def queue_declare(self,comments=""):
        state_type = "queue_declare"
        state_def = {
            "variable_name" : self.name,
            "body" : []
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def queue_push(self,body,element,comments=""):
        state_type = "queue_push"
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
    
    def queue_pop(self,body,comments=""):
        state_type = "queue_pop"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def queue_front(self,body,comments=""):
        state_type = "queue_front"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def queue_back(self,body,comments=""):
        state_type = "queue_back"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
# Queue class is an template for queues to be used
class Queue:
    
    def __init__(self, name:str, algo:StateSet, comments:str = ""):
        try:
            assert type(name)==str 
            self.state_generator = QueueState(name)
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == StateSet 
            self.algo = algo
        except:
            raise ARgorithmError("Queue structure needs a reference of template to store states")
        self.body = []
        state = self.state_generator.queue_declare(comments)
        self.algo.add_state(state)

    def __len__(self):
        return len(self.body)
    
    def empty(self):
        return len(self)==0

    def push(self,element,comments=""):
        self.body.append(element)
        state = self.state_generator.queue_push(self.body,element,comments)
        self.algo.add_state(state)

    def pop(self,comments=""):
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = self.body[0]
        self.body = self.body[1:]
        state = self.state_generator.queue_pop(self.body,comments)
        self.algo.add_state(state)
        return item

    def front(self,comments=""):
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = self.body[0]
        state = self.state_generator.queue_front(self.body,comments)
        self.algo.add_state(state)
        return item

    def back(self,comments=""):
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = self.body[-1]
        state = self.state_generator.queue_back(self.body,comments)
        self.algo.add_state(state)
        return item

        