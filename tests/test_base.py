import ARgorithmToolkit

def test_base():
    a = ARgorithmToolkit.Template()
    a.states.append('test state')
    assert( len(a.states) == 1 )
    
def test_state():
    s = ARgorithmToolkit.State(state_def="Test" , state_type="Test" , comments="test")
    try:
        s = ARgorithmToolkit.State(state_def="ErrorTest")
        assert False , 'No error raised'
    except ARgorithmToolkit.ARgorithmError:
        pass

def test_variable():
    algo = ARgorithmToolkit.Template()
    s = ARgorithmToolkit.Variable("s",algo,10)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'variable_declare'
    s.highlight(comments="this is an important 's'")
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'variable_highlight'