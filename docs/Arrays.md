## Arrays

> ArgorithmToolkit.Array

Methods supported

| Method     | Parameter                                                 | Description                                                  |
| ---------- | --------------------------------------------------------- | ------------------------------------------------------------ |
| initialise | data:`list` , shape:`tuple` , dtype: `int` , fill:`dtype` | The array can be initialised using a preexisting list or can use  shape that has to be filled, we also offer choice of dtype and fill. Data is prefered over shape. Fill only works if shape is provided |
| indexing   | index:`index`                                             | The array generates states whenever a element is read or set in the array |
| swap       | index1:`index` , index2:`index`                           | Swaps two elements in an array                               |
| compare    | index1:`index` , index2:`index` , func:`function`         | compares the elements at the indexes using the function provided else send difference |

:warning: Please prefer using `arr[i,j]` over `arr[i][j]` as the latter can cause discrepancies

Example

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> arr = ARgorithmToolkit.Array("arr",algo,data=[[1,2],[3,4],[4,5]],comments="shape_declare")
>>> print(arr)
[[1 2]
 [3 4]
 [4 5]]
>>> arr[0,0]
1
>>> arr[1,1] = 8
>>> print(arr)
[[1 2]
 [3 8]
 [4 5]]
>>> arr.swap((0,1),(2,0))
>>> print(arr)
[[1 4]
 [3 8]
 [2 5]]
>>> for i in range(2):
...     for j in range(2):
...             print(arr[i,j])
... 
1
4
3
8
>>> arr = ARgorithmToolkit.Array("arr2",algo,shape=(3,4),comments="shape_declare") 
>>> print(arr)
[[0 0 0 0]
 [0 0 0 0]
 [0 0 0 0]]
>>> arr = ARgorithmToolkit.Array("arr2",algo,shape=(3,4),fill=3,comments="shape_declare") 
>>> print(arr)
[[3 3 3 3]
 [3 3 3 3]
 [3 3 3 3]]
>>> print(algo)
{'state_type': 'array_declare', 'state_def': {'variable_name': 'arr', 'body': [[1, 2], [3, 4], [4, 5]]}, 'comments': 'shape_declare'}
{'state_type': 'array_iter', 'state_def': {'variable_name': 'arr', 'body': [[1, 2], [3, 4], [4, 5]], 'index': (0, 0)}, 'comments': ''}
{'state_type': 'array_iter', 'state_def': {'variable_name': 'arr', 'body': [[1, 2], [3, 8], [4, 5]], 'index': (1, 1)}, 'comments': 'Writing 8 at index (1, 1)'}
{'state_type': 'array_swap', 'state_def': {'variable_name': 'arr', 'body': [[1, 4], [3, 8], [2, 5]], 'index1': (0, 1), 'index2': (2, 0)}, 'comments': ''}
{'state_type': 'array_iter', 'state_def': {'variable_name': 'arr', 'body': [[1, 4], [3, 8], [2, 5]], 'index': (0, 0)}, 'comments': ''}
{'state_type': 'array_iter', 'state_def': {'variable_name': 'arr', 'body': [[1, 4], [3, 8], [2, 5]], 'index': (0, 1)}, 'comments': ''}
{'state_type': 'array_iter', 'state_def': {'variable_name': 'arr', 'body': [[1, 4], [3, 8], [2, 5]], 'index': (1, 0)}, 'comments': ''}
{'state_type': 'array_iter', 'state_def': {'variable_name': 'arr', 'body': [[1, 4], [3, 8], [2, 5]], 'index': (1, 1)}, 'comments': ''}
{'state_type': 'array_declare', 'state_def': {'variable_name': 'arr2', 'body': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]}, 'comments': 'shape_declare'}
{'state_type': 'array_declare', 'state_def': {'variable_name': 'arr2', 'body': [[3, 3, 3, 3], [3, 3, 3, 3], [3, 3, 3, 3]]}, 'comments': 'shape_declare'}
```

