
import ARgorithmToolkit

def run(**kwargs):
    n = kwargs["n"]
    algo = ARgorithmToolkit.StateSet()
    if n <= 0:
        return algo
    
    body = [0]*n
    body[0] = 0
    if n == 1:
        return ARgorithmToolkit.Vector("arr" , algo, body, "initializing vector with first fibonacci number 0")

    body[1] = 1

    arr = ARgorithmToolkit.Vector("arr" , algo, body, "initializing vector with first two fibonacci numbers 0, 1")   
    for i in range(2, n):
        arr[i] = arr[i-1] + arr[i-2]
    return algo

        