
import ARgorithmToolkit

def run(**kwargs):
    n = kwargs["n"]
    algo = ARgorithmToolkit.StateSet()
    st = ARgorithmToolkit.Stack("stack" , algo , "creating the stack")
    st.push(0)
    st.push(1)    
    curr = ARgorithmToolkit.Variable("answer",algo , comments="this will store the answer")
    temp = ARgorithmToolkit.Variable("answer",algo , comments="this will store the second highest")
    if n > 0:
        for i in range(1,n):
            temp.value =  st.pop()
            curr.value = temp.value + st.top()
            st.push(temp.value)
            st.push(curr.value)
    return algo

        