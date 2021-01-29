
import ARgorithmToolkit

def run(**kwargs):
    n = kwargs["n"]
    algo = ARgorithmToolkit.StateSet()
    if n <= 0:
        algo.add_comment("n has to be natural number, try again")
        return algo

    var1 = ARgorithmToolkit.Variable("first",algo,1,comments="The first fibonacci number")
    if n == 1:
        algo.add_comment("1 is the first fibonacci number")
        return algo

    var2 = ARgorithmToolkit.Variable("second",algo,1,comments="The second fibonacci number")

    for _ in range(2, n):
        temp1 = var1.value
        temp2 = var2.value
        algo.add_comment(f"adding {temp1} and {temp2} and we get next fibonacci number {temp1+temp2}")
        var1.value = temp2
        var2.value = temp1+temp2
    algo.add_comment(f"{var2.value} is the {n}th fibonacci number")
    return algo
