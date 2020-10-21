## Queue

> ARgorithmToolkit.Queue

Methods supported

| method | parameter   | description                                         | example   |
| ------ | ----------- | --------------------------------------------------- | --------- |
| push   | value:`int` | pushes to back of queue                             | q.push(1) |
| pop    |             | pops from front of queue                            | q.pop()   |
| front  |             | displays the front of queue                         | q.front() |
| back   |             | displays the back of queue                          | q.back()  |
| empty  |             | boolean value that indicates whether queue is empty | q.empty() |

Example

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> queue = ARgorithmToolkit.Queue('qu',algo)
>>> queue.push(1)
>>> queue.push(2)
>>> queue.front()
1
>>> queue.pop()
1
>>> len(queue)
1
>>> while not queue.empty():
...     queue.pop()
... 
2
>>> print(algo)
{'state_type': 'queue_declare', 'state_def': {'variable_name': 'qu', 'body': []}, 'comments': ''}
{'state_type': 'queue_push', 'state_def': {'variable_name': 'qu', 'body': [1], 'element': 1}, 'comments': ''}
{'state_type': 'queue_push', 'state_def': {'variable_name': 'qu', 'body': [1, 2], 'element': 2}, 'comments': ''}
{'state_type': 'queue_front', 'state_def': {'variable_name': 'qu', 'body': [1, 2]}, 'comments': ''}
{'state_type': 'queue_pop', 'state_def': {'variable_name': 'qu', 'body': [2]}, 'comments': ''}
{'state_type': 'queue_pop', 'state_def': {'variable_name': 'qu', 'body': []}, 'comments': ''}

```
