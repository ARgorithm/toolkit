import ARgorithmToolkit

def test_base():
    a = ARgorithmToolkit.Template()
    assert( str(a) == f"Not specified\n" )
    a.states.append('test state')
    assert( len(a.states) == 1 )
    
class helloworld(ARgorithmToolkit.Template):

    def __init__(self):
        super().__init__()
        self.desc = "testing"

def test_inherit():
    h = helloworld()
    assert( str(h) == f"testing\n" )