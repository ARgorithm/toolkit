## Stack

> ARgorithmToolkit.Stack

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> stack = ARgorithmToolkit.Stack('st',algo)
>>> stack.push(1)
>>> stack.push(2)
>>> stack.top()
2
>>> stack.pop()
2
>>> len(stack)
1
>>> while not stack.empty():
...     stack.pop()
... 
1
>>> print(algo)
{'state_type': 'stack_declare', 'state_def': {'variable_name': 'st', 'body': []}, 'comments': ''}
{'state_type': 'stack_push', 'state_def': {'variable_name': 'st', 'body': [1], 'element': 1}, 'comments': ''}
{'state_type': 'stack_push', 'state_def': {'variable_name': 'st', 'body': [1, 2], 'element': 2}, 'comments': ''}
{'state_type': 'stack_top', 'state_def': {'variable_name': 'st', 'body': [1, 2]}, 'comments': ''}
{'state_type': 'stack_pop', 'state_def': {'variable_name': 'st', 'body': [1]}, 'comments': ''}
{'state_type': 'stack_pop', 'state_def': {'variable_name': 'st', 'body': []}, 'comments': ''}

```

Methods supported

| method | parameter   | description                                         | example   |
| ------ | ----------- | --------------------------------------------------- | --------- |
| push   | value:`int` | pushes to top of stack                              | q.push(1) |
| pop    |             | pops from top of stack                              | q.pop()   |
| top    |             | displays the top of stack                           | q.top()   |
| empty  |             | boolean value that indicates whether stack is empty | q.empty() |

