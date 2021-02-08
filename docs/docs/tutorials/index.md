# Tutorials

This section demonstrates how argorithms are created to visualize data structures and algorithm in augmented reality. All the files used in this section can be found [here](https://github.com/ARgorithm/toolkit/tree/master/examples). Before we see and implement some examples, it is important to understand the functioning of `ARgorithmToolkit` and what all data does an *argorithm* require to create dynamic AR visualisations.

## Creating the template

The ARgorithmToolkit CLI comes with the [`init`](/toolkit/cli#init) command  to generate a blank template for your argorithm

<div class="termy">
```
$ ARgorithm init hello_world
Creating empty template for hello_world
[SUCCESS]: TEMPLATE GENERATED
refer documentation at https://argorithm.github.io/toolkit/ to learn how to use it
chech out examples at https://github.com/ARgorithm/toolkit/tree/master/examples
$ ls
hello_world.py
```
</div>

This creates the template `.py` file  This file was covered once in the [getting started page](/toolkit/start). All the examples in this tutorials will be starting from this step onwards.

## Executing the code

One thing to be kept in mind while running an argorithm code file is that what you want to return is the output of the object but the stateset called. Thus, it becomes fundamentally important to be able to decipher stateset.

The [`Stateset`](/toolkit/api//utils#ARgorithmToolkit.utils.StateSet) is an list of [`State`](/toolkit/api//utils#ARgorithmToolkit.utils.State) objects. Each state is an event that occurs during the execution of the program.

```python hl_lines="2 7 12"
{
	'state_type': 'TYPE1', 
	'state_def':  {'DEF1'},
	'comments': 'COMMENTS1'
},
{
	'state_type': 'TYPE2', 
	'state_def': {'DEF2'},
    'comments': ''
}
,{
	'state_type': 'TYPE3', 
	'state_def': {'DEF3'},
    'comments': 'COMMENTS3'
}
```

- The `state_type` is a literal used by the AR application to classify what kind of event is this. The `state_type` by convention is of the form `<structure>_<method>` like `array_iter`,`stack_push` etc. 
- The `state_def` gives data about the particular event. 
- The `comments` are used to add descriptive text to the AR visualisation. 

You can refer all the state types and what they do in the [designs folder](https://github.com/ARgorithm/toolkit/tree/master/designs)