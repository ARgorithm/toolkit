"""Test module for ARgorithmToolkit.Map"""
import ARgorithmToolkit
algo = ARgorithmToolkit.StateSet()
str1 = ARgorithmToolkit.String("str1", algo, "xyz")
map1 = ARgorithmToolkit.Map("map1", algo)
def test_map():
    """Tests Map body, states, and get/set methods
    """
    assert algo.states[-1].content['state_type'] == "map_declare"
    map1["abcd"] = 123
    map1.set(2,"hello")
    map1[str1] = 456
    assert algo.states[-1].content['state_type'] == "map_set"
    assert map1[str1] == 456
    assert map1["abcd"] == 123
    assert map1[2] == "hello"
    assert algo.states[-1].content['state_type'] == "map_get"
    assert map1[str1] == 456
    assert map1.get("123",-1) == -1
    assert algo.states[-1].content['state_def']['value'] == -1

def test_remove():
    """Tests map item deletion
    """
    map1.remove("abcd")
    assert algo.states[-1].content['state_type'] == "map_remove"
    map1.remove("abcd")
    assert algo.states[-1].content['state_def']['value'] == "none"
    del map1[2]
    assert algo.states[-1].content['state_type'] == "map_remove"
    map1.get(2, "not found")
    assert algo.states[-1].content['state_def']['value'] == "not found"
    print(map1)

def test_iteration():
    """Tests map iteration
    """
    map1['123']=123
    res = []
    for key, value in map1:
        res.append((key,value))

    assert res == [(str1, 456),('123',123)]
    assert algo.states[-1].content['state_type'] == "map_set"
