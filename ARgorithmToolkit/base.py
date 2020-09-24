# Base template that all algorithms will use

# error class to simplify user debugging
class ARgorithmError(Exception):

  def __init__(self,*args):
    if args:
        self.message = args[0]
    else:
        self.message = None
        
  def __str__(self):
    if self.message:
        return f'{self.message}'
    else:
        return f'Please check all resources'


# the template class proves as a base for our algorithms
class Template:

    def __init__(self):
        self.desc = "Not specified"
        self.states = []

    def __str__(self):
        state_desc = "\n".join([x for x in self.states]) if len(self.states) > 0 else ""
        return f"{self.desc}\n{state_desc}"


# the state template class to ensure each state is of same structure
class State:
    def __init__(self,*args):
        pass