
import ARgorithmToolkit

def check(a,b):
    return a>b

def run(**kwargs):
    algo = ARgorithmToolkit.StateSet()
    arr = ARgorithmToolkit.Array('arr',algo,data=kwargs['array'],comments="This is our unsorted array")
    for i in range(0,len(arr)):
        algo.add_comment(f"Iterating the array starting from the {i}th index")
        for j in range(i+1,len(arr)):
            if arr.compare(i,j,check,comments=f"comparing the {i}th and {j}th element"):
                arr.swap(i,j,comments=f"as arr[{i}] > arr[{j}] , we swap them")
    return algo

        