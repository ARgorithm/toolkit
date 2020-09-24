import ARgorithmToolkit

def test_base():
    a = ARgorithmToolkit.ARgorithmTemplate()
    assert( str(a) == f"Not specified\n" )
    a.states.append('test state')
    assert( len(a.states) == 1 )
    
class helloworld(ARgorithmToolkit.ARgorithmTemplate):

    def __init__(self):
        super().__init__()
        self.desc = "testing"

def test_inherit():
    h = helloworld()
    assert( str(h) == f"testing\n" )