### vectors

> ARgorithmToolkit.vector


Methods supported :

| Method   | Parameters                                                   | Description                                                  | example                                       |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ | --------------------------------------------- |
| indexing | index : `int`                                                | accessing a certain index of vector                           | arr[0]                                        |
| slicing  | slice:`slice`                                                | accessing a sub vector of vector                               | arr[1:4]                                      |
| insert   | value:`any`<br/> index:`int` (optional)                      | inserting a element at an index or if no index specified default last | arr.insert(10) ;<br />arr.insert(10,2)        |
| remove   | value:`any` (optional)<br />index:`int`(optional)            | removing a particular value or from a particular index. Specify only one of the two | arr.remove(value=10)<br />arr.remove(index=8) |
| compare  | index1 : `int`<br />index2 : `int`<br />func : `function` (optional) | compares the values at the two indexes. returns result of == if func not specified | arr.compare(1,2)                              |
| swap     | index1 : `int`<br />index2 : `int`                           | swaps the values at the two indexes                          | arr.swap(2,3)                                 |

Example

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> vector = ARgorithmToolkit.Vector('arr' , algo)
>>> print(vector)
[]
>>> vector.insert(12)
>>> vector.insert(11,0,comments="lets insert a number at index 0")
>> vector[0]
11
>>> for x in vector:
...     print(x)
... 
11
12
>>> print(algo)
{'state_type': 'vector_declare', 'state_def': {'variable_name': 'arr', 'body': [12]}, 'comments': ''}
{'state_type': 'vector_insert', 'state_def': {'variable_name': 'arr', 'body': [12], 'element': 12, 'index': 1}, 'comments': ''}
{'state_type': 'vector_insert', 'state_def': {'variable_name': 'arr', 'body': [11, 12], 'element': 11, 'index': 0}, 'comments': 'lets insert a number at index 0'}
{'state_type': 'vector_iter', 'state_def': {'variable_name': 'arr', 'body': [11, 12], 'index': 0}, 'comments': ''}
{'state_type': 'vector_iter', 'state_def': {'variable_name': 'arr', 'body': [11, 12], 'index': 0}, 'comments': ''}
{'state_type': 'vector_iter', 'state_def': {'variable_name': 'arr', 'body': [11, 12], 'index': 1}, 'comments': ''}

```
