# Bubblesort

This tutorial looks towards creating AR visualisation of bubblesort using ARgorithm. [Bubblesort](https://www.geeksforgeeks.org/bubble-sort/) is one of the most basic sorting algorithms. 

## Writing the code

This is the argorithm code for bubblesort. As you can see other than some differences in object creation and methods. The core logic behind the algorithm remains unchanged and the lines of code are not very different from the normal implementation of bubblesort.

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

Lets break down the differences. as we mentioned before for an argorithm to able to record states, we need an object of type StateSet and that is what our ARgorithm should return and not the output of the algorithm. The output of the algorithm if not specified with any of the states can be appended to the stateset.

```Python hl_lines="7 14"
{!../../examples/bubblesort.py!}
```
### Using the ARgorithm STL

For ARgorithm to listen to the state changes you need to implement the containers and objects that you want rendered using the classes provided in ARgorithmToolkit. We have an array here on which we have to show bubblesort so insteaed of using `list`, we will use the [`ARgorithmToolkit.Array`](/toolkit/api/array.html#ARgorithmToolkit.array.Array). The constructor for the `Array` class will take the stateset and the array.

```Python hl_lines="8"
{!../../examples/bubblesort.py!}
```

Now whenever the values of array are accessed or altered, the stateset will record the events. The `Array` class can be indexed normally as a list would be. The `Array` class comes with built-in functions that are not only useful but create special states that can be used to create more powerful animations. For eg. we can just index the array elements and compare them and swap their values as done in a normal bubblesort but by using the `Array.compare` and `Array.swap` we get the same functionalities and create more animations.

```Python hl_lines="12-13"
{!../../examples/bubblesort.py!}
```

### Adding comments

The goal of ARgorithm is to create visualisations for educational purposes. Thus textual hints that can be showed along with AR powered visualisations make them easier to understand. We highly recommend that comments be used wherver required to make clearer visualisations. You can add your comments in your method calls or use the [`add_comment`](/toolkit/api/utils.html#ARgorithmToolkit.utils.StateSet.add_comment) method.

```Python hl_lines="8 10 12-13"
{!../../examples/bubblesort.py!}
```

## Setting up the config file

Now that your argorithm is ready, it's time to configure the `bubblesort.config.json`.`argorithmID` and `file` is already filled and need not be altered. The `function` is set to `run` which is the function from the file we need to call. The `description` stored description of the agorithm. These are useful metadata for the CLI and server when it comes to parsing and execution. The most important keys are `parameters` and `default`.



1. `parameters` : This key stores an object where each key is a key for the function `**kwargs` and its value is the type of value expected.

   

2. `default` : This key stores an object that specifies the default value for function `**kwargs`. These values would be used to in case of any exception in executing parameters. 

!!! info
	The keys inside the parameters and default objects must be the same



```JSON hl_lines="5-12"
{!../../examples/bubblesort.config.json!}
```

Now that we are done, we can submit the file to the server
<div class="termy">
```console
$ ARgorithm submit bubblesort
[SUCCESS]: FILES FOUND
[SUCCESS]: FILES VERIFIED
[SUCCESS]: SUBMITTED
```
</div>

