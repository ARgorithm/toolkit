# Bubblesort

This tutorial looks towards creating an AR visualisation of bubblesort using ARgorithm. [Bubblesort](https://www.geeksforgeeks.org/bubble-sort/) is one of the most basic sorting algorithms. 

## Writing the code

This is the argorithm code for bubblesort. As you can see other than some differences in object creation and methods, the core logic behind the algorithm remains unchanged and the lines of code do not differ much from the normal implementation of bubblesort.

```Python hl_lines="5 8-10"
def check(a,b):
    return a>b

def run(**kwargs):
    arr = kwargs['array']
    for i in range(0,len(arr)):
        for j in range(i+1,len(arr)):
            if check(arr[i],arr[j]):
            	arr[i],arr[j] = arr[j],arr[i]
    return array
```

```Python hl_lines="1-2 7-8 10 12-14"
{!../../examples/bubblesort.py!}
```
### The StateSet Object

Let's break down the differences. As we mentioned before for an argorithm to be able to record states, we need an object of type StateSet and that is what our ARgorithm should return, not the output of the algorithm. The output of the algorithm if not specified with any of the states can be appended to the stateset.

```Python hl_lines="7 14"
{!../../examples/bubblesort.py!}
```
### Using the ARgorithm STL

For ARgorithm to listen to the state changes you need to implement the containers and objects that you want rendered using the classes provided in ARgorithmToolkit. We have an array here on which we have to show bubblesort so insteaed of using `list`, we will use the [`ARgorithmToolkit.Array`](/toolkit/api/array.html#ARgorithmToolkit.array.Array). The constructor for the `Array` class will take the stateset and the array.

```Python hl_lines="8"
{!../../examples/bubblesort.py!}
```

Now whenever the values of the array are accessed or altered, the stateset will record the events. The `Array` class can be indexed normally as a list would be. The `Array` class comes with built-in functions that are not only useful but create special states that can be used to create more powerful animations. For eg. we can just index the array elements and compare them and swap their values as done in a normal bubblesort but by using the `Array.compare` and `Array.swap`, we get the same functionalities and create more animations.

```Python hl_lines="12-13"
{!../../examples/bubblesort.py!}
```

### Adding comments

The goal of ARgorithm is to create visualisations for educational purposes. Thus, textual hints can be shown along with AR powered visualisations to make them easier to understand. We highly recommend that comments be used wherever required to make clearer visualisations. You can add your comments in your method calls or use the [`add_comment`](/toolkit/api/utils.html#ARgorithmToolkit.utils.StateSet.add_comment) method.

```Python hl_lines="8 10 12-13"
{!../../examples/bubblesort.py!}
```

## Setting up the config file

Now that your argorithm is ready, it's time to configure the `bubblesort.config.json`. We can use the configure command or create the file and set it up in the code editor. As you can see below, we have demonstrated how to create the `bubblesort.config.json` using the `configure` command and how the file should look like. You can directly check out the final `bubblesort.config.json` below.

<div class="termy">

```console
$ ARgorithm configure bubblesort 
# Start CLI config generator?  [y/N]:$ y

+-----------------------------+
|  ARGORITHM CONFIG GENERATOR |
+-----------------------------+

ARgorithmID: bubblesort
Codefile found: bubblesort.py
# which function should be called [run]:$ run
Enter ARgorithm Description
Press ENTER on empty line to leave multiline input
# :$ demonstrate bubble sort
```

</div>

We need to define `array` which would be the array that we will sort.

<div class="termy">

```console
Setting up parameters for your argorithm
input keywords are used to map the input passed to your function as kwargs

The following input keywords were found in code
- array
input keyword: array
# Enter parameter type:$ ARRAY
# Enter type of array element:$ INT
# Do you want to set a size constraint to array [y/N]:$ N
Enter parameter description
Press ENTER on empty line to leave multiline input:
# :$ Array to be sorted

# Do you want to another input keyword [y/N]:$ n
```

</div>

We now need to define the default array that will be used when `array` is not input by user

<div class="termy">

```console
----------------------------------------
ENTER INPUT FOR ARGORITHM
----------------------------------------
Based on argorithm parameters, input will be taken

input keyword: array
Description: Array to be sorted
# Enter space separated series:$ 6 3 2 4 5 1

```

</div>

This is how the `bubblesort.config.json` should look like.

```JSON
{!../../examples/bubblesort.config.json!}
```

Finally, we can submit the file to the server.
<div class="termy">
```console
$ ARgorithm submit bubblesort
[SUCCESS]: FILES FOUND
[SUCCESS]: FILES VERIFIED
[SUCCESS]: SUBMITTED
```
</div>

