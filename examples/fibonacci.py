
import ARgorithmToolkit

def run(**kwargs):
    n = kwargs["n"]
    algo = ARgorithmToolkit.StateSet()
    body = [0]*n
    body[0] = 0
    body[1] = 1
    arr = ARgorithmToolkit.Vector("arr" , algo ,body, "initializing vector")   
    for i in range(2, n):
        arr[i] = arr[i-1] + arr[i-2]
    return algo

        