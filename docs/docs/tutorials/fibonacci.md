# Fibonacci

This tutorial looks towards creating AR visualisation of creating fibonacci number using array using ARgorithm.  It is advised you go through the [previous tutorial](/toolkit/tutorials/bubblesort) before this to understand this better.

## Writing the code

Fibonacci number is a very popular problem at the beginners level to explain concepts of recursion and later dynamic programming. In this example, we will be implementing iterative approach. The `ARgorithmToolkit` class that we'll be using in this example is [`Variable`](/toolkit/api/utils.html#ARgorithmToolkit.utils.Variable). 

```Python
{!../../examples/fibonacci.py!}
```

The `Variable` class is little different from the other classes and interfaces in ARgorithmToolkit. This class does not have any functionality other than remember the states of objects of datatypes like `int`,`float`,`string`,`bool`. It is advised to use this only when you need a particular variable rendered in augmented reality  that can prove helpful to understanding the code.

!!! warning
	Be careful when reading or writing the value of the `Variable` class.
	```python hl_lines="4 7"
    >>> var = ARgorithmToolkit.Variable("var",algo,1)
    >>> var
    Variable(1)
    >>> var.value = 3
    >>> var
    Variable(3)
    >>> var = 3
    >>> var
    3
	``` 
	Directly assigning values to the `Variable` object will overwrite the object and states will no longer be recorded for it.

In the fibonacci sequence, each number is the sum of its previous two fibonacci numbers. We'll be using two variables to store the previous fibonacci.

$$
F\mathbf(n) = F\mathbf(n-1) + F\mathbf(n-2)
$$

```Python  hl_lines="10 15 18-19 21-22"
{!../../examples/fibonacci.py!}
```

## Setting up the config file

For this code, we only need one parameter that is `n` which is the index of the number required in the sequence. We will provide the default value for `n` as 4. As shown in [previous tutorial](/toolkit/tutorials/bubblesort), you can create this using your code editor or the `configure` command [(how to use configure)](/toolkit/tutorials/config)
```json
{!../../examples/fibonacci.config.json!}
```

Now that we are done, we can submit the file to the server
<div class="termy">
```console
$ ARgorithm submit fibonacci
[SUCCESS]: FILES FOUND
[SUCCESS]: FILES VERIFIED
[SUCCESS]: SUBMITTED
```
</div>