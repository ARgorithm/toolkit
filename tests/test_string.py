import ARgorithmToolkit

algo = ARgorithmToolkit.StateSet()
st = ARgorithmToolkit.String('st', algo, "Hello world! 1234")

def test_body():
    assert st.body == "Hello world! 1234"
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'string_declare'
    assert last_state.content["state_def"]["body"] == "Hello world! 1234"

def test_append():
    global st
    st.append(" Hahaha")
    assert st.body == "Hello world! 1234 Hahaha"
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'string_append'
    assert last_state.content["state_def"]["element"] == " Hahaha"
    st+='xyz'
    assert st.body == "Hello world! 1234 Hahahaxyz"
    last_state = algo.states[-1]
    second_last_state = algo.states[-2]
    assert last_state.content["state_type"] == 'string_append'
    assert last_state.content["state_def"]["element"] == "xyz"
    assert second_last_state.content["state_type"] == 'string_declare'
    assert second_last_state.content["state_def"]["body"] == "Hello world! 1234 Hahaha"
    assert second_last_state.content["state_def"]["variable_name"] == "st_super"

def test_indexing():
    assert st[1] == st.body[1]
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'string_iter'
    assert last_state.content["state_def"]["index"] == 1
    
    subst = st[1:3]
    assert type(subst) == type(st)
    last_state = algo.states[-1]
    assert last_state.content["state_type"] == 'string_declare'
    assert last_state.content["state_def"]["variable_name"] == 'st_super_sub'
    assert last_state.content["state_def"]["body"] == st.body[1:3]
    

def test_iteration():
    for i,(a,b) in enumerate(zip(st,st.body)):
        assert a==b
        last_state = algo.states[-1]
        assert last_state.content["state_type"] == 'string_iter'
        assert last_state.content["state_def"]["index"] == i
    

    