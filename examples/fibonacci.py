
import ARgorithmToolkit

def run(**kwargs):
    n = kwargs["n"]
    algo = ARgorithmToolkit.StateSet()
    if n <= 0:
        return algo
    
    body = [0]*n
    body[0] = 0
    if n == 1:
        return ARgorithmToolkit.Array("arr" , algo, data=body, comments="initializing vector with first fibonacci number 0")

    body[1] = 1

    arr = ARgorithmToolkit.Array("arr" , algo, data=body, comments="initializing vector with first two fibonacci numbers 0, 1")   
    for i in range(2, n):
        temp1 = arr[i-2]
        temp2 = arr[i-1]
        algo.add_comment(f"adding {temp1} and {temp2} and putting sum {temp1+temp2} in index {i}")
        arr[i] = temp1+temp2
    return algo

        