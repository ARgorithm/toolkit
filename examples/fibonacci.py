
import ARgorithmToolkit

def run(**kwargs):
    n = kwargs["n"]
    algo = ARgorithmToolkit.StateSet()
    body = [0]*n
    body[0] = 0
    body[1] = 1
    arr = ARgorithmToolkit.Array("arr" , algo ,body, "initializing array")   
    for i in range(2, n):
        arr[i] = arr[i-1] + arr[i-2]
    return algo

        