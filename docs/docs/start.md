 You can install the ARgorithmToolkit using pip 

<div class="termy">

```console
$ pip install ARgorithmToolkit

---> 100%
Successfully installed ARgorithmToolkit
```
</div>

You can setup auto completion for your shell by using --install-completion option provided by `Typer`. After that you can get started with your own ARgorithm

<div class="termy">
```console
$ ARgorithm init hello_world
Creating empty template for hello_world
[SUCCESS]: TEMPLATE GENERATED
refer documentation at https://argorithm.github.io/toolkit/ to learn how to use it
chech out examples at https://github.com/ARgorithm/toolkit/tree/master/examples

$ ls
hello_world.py
```
</div>

This will generate your `.py` file. The  `<name>.py` file will store your code that you will submit to the server hosting all ARgorithms

The `<name>.py` file initially looks like this

```python
import ARgorithmToolkit

def run(**kwargs):
    stateset = ARgorithmToolkit.StateSet()
	
    #
    #	Your code
	#
    
    return
```

You can add whatever code you want to this file using all the tools and classes present in ARgorithmToolkit but be sure that

1. Your file should have one function which takes `**kwargs` input (refer [here](https://book.pythontips.com/en/latest/args_and_kwargs.html) to know more about kwargs) that will should perform whatever you desire and should return the stateset. You can check out later in the document on how to use this stateset
2.  you can create classes and additional functions in your code. Support for importing external modules is not yet added so its advisable not to use those.

Once you have created your code, you need to create a `<name>.config.json` in which you will describe metadata regarding your argorithm. You can create a blank config file by using the `--config` flag in `init` command and enter your values. You can also create a `.config.json` later using the `configure` command.

the `<name>.config.json` file is a JSON file storing all the metadata. Below is an example of the config.json for [bubblesort](/toolkit/tutorials/bubblesort). You can understand the `.config.json` file [here](/toolkit/tutorials/config)

```json
{
    "argorithmID": "bubblesort", 
    "file": "bubblesort.py", 
    "function": "run", 
    "parameters": {
        "array" : {
            "description" : "Array to be sorted",
            "type" : "ARRAY",
            "item-type" : "INT"
        }
    }, 
    "example": {
        "array" : [
            6,3,2,4,5,1
        ]
    }, 
    "description": "demonstrate bubble sort"
}
```

| Key         | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| argorithmID | name of your ARgorithm , this is generally pre filled from when you run the init command. The name of your code file should be *name*.py and the config should be *name*.config.json. [will be fixed later] |
| file        | The file containing your codefile                            |
| function    | The function that is going to be called                      |
| parameters  | the parameters that your ARgorithm would need, this helps in anyone using your ARgorithm to understand what is the input format |
| example     | default parameters in case no parameters are passed          |
| description | The description of ARgorithm. Helpful to people using your ARgorithm as well as other developers |

You can check out ARgorithm examples in our Github Repo.
Check out the commandline interface for more details

## Using ARgorithmToolkit

ARgorithmToolkit adds a few extra steps when it comes to initializing instances whose states you want to record but thats because a lot of data has to be maintained in order for smooth transitions

```python hl_lines="1-3"
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> x = ARgorithmToolkit.Variable('x',algo,0,comments='Our first variable')
>>> x.value
0
>>> x.value += 10
>>> x.value
10
>>> print(algo)
{
	'state_type': 'variable_declare', 
	'state_def': {'variable_name': 'x', 'value': 0},
    'comments': 'Our first variable'
}
{
	'state_type': 'variable_highlight', 
	'state_def': {'variable_name': 'x', 'value': 10},
	'comments': ''
}
```

As ARgorithm is tool for creating visual demonstration , you can add comments parameter to most functions. These comments get included in states and get featured as text when that state is rendered in AR.

Make sure you design the objects you want to keep track of as part of the same stateset. Each object is instantiated with a **name** this is important to identify arrays when rendering them

You can refer the docs and samples in the [repo](https://github.com/ARgorithm/toolkit) to understand more clearly.



## StateSet

The core class to all algorithm and data structures in ARgorithmToolkit
You will always need a object of this class when using different ARgorithmToolkit features. This is where the states are stored that later get rendered to ARgorithm App. So obviously all your ARgorithms are supposed to return this

You wont have to interact with it much other than while initialising objects and returning results.
It has a `add_comment` method that allows you to create blank states carrying description in the form of comments that you might want to show to the client while the ARgorithm is being rendered. This will prove handy when creating good demonstrations

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> algo.add_comment("Hello world")
>>> print(algo)
{'state_type': 'comment', 'state_def': None, 'comments': 'Hello world'}
```



