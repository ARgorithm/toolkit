from ARgorithmToolkit.utils import State, StateSet, ARgorithmError
import heapq
# PriorityQueueState class to create queue related states
# Refer priorityqueue_schema.yml for understanding states
class PriorityQueueState():
    
    def __init__(self,name):
        self.name = name

    def priorityqueue_declare(self,comments=""):
        state_type = "priorityqueue_declare"
        state_def = {
            "variable_name" : self.name,
            "body" : []
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )
    
    def priorityqueue_offer(self,body,element,comments=""):
        state_type = "priorityqueue_offer"
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
    
    def priorityqueue_poll(self,body,comments=""):
        state_type = "priorityqueue_poll"
        state_def = {
            "variable_name" : self.name,
            "body" : [x for x in body],
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def priorityqueue_peek(self,body,comments=""):
        state_type = "priorityqueue_peek"
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
class PriorityQueue:
    
    def __init__(self, name:str, algo:StateSet, comments:str = ""):
        try:
            assert type(name)==str 
            self.state_generator = PriorityQueueState(name)
        except:
            raise ARgorithmError('Give valid name to data structure')
        try:
            assert type(algo) == StateSet 
            self.algo = algo
        except:
            raise ARgorithmError("Queue structure needs a reference of template to store states")
        self.body = []
        state = self.state_generator.priorityqueue_declare(comments)
        self.algo.add_state(state)

    def __len__(self):
        return len(self.body)
    
    def empty(self):
        return len(self)==0

    def offer(self,element,comments=""):
        heapq.heappush(self.body, element)
        state = self.state_generator.priorityqueue_offer(self.body,element,comments)
        self.algo.add_state(state)

    def poll(self,comments=""):
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = heapq.heappop(self.body)
        state = self.state_generator.priorityqueue_poll(self.body,comments)
        self.algo.add_state(state)
        return item

    def peek(self,comments=""):
        if self.empty():
            raise ARgorithmError('queue is empty')
        item = self.body[0]
        state = self.state_generator.priorityqueue_peek(self.body,comments)
        self.algo.add_state(state)
        return item


        