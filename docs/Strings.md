## Strings

> ARgorithmToolkit.String

Methods Supported

| Method     | Parameters               | Description                                                  |
| ---------- | ------------------------ | ------------------------------------------------------------ |
| initialise | body:`str`               | The string class is an immutable class. So the value can be initialised only once. Value can be appended to it though |
| indexing   | index:`index`            | The characters of the string class can be indexed            |
| slicing    | slice:`slice`            | Substrings of array can be generated using python slicing    |
| append     | value:`str`  or `String` | You can append string values or another ARgorithmToolkit.String to your string using the append function |
| addition   | value:`str`  or `String` | append is different from addition. Addition returns a new String object. Append adds your string to the Same string and doesn't return anything |

:warning: Be care with use of append and addition

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> s = ARgorithmToolkit.String("s",algo,"hello")
>>> print(s)
hello
>>> s[1]
'e'
>>> s[1:3]
'el'
>>> s.append(' world')
>>> print(s)
hello world
>>> a = s + s
>>> print(a)
hello worldhello world
>>> print(algo)
{'state_type': 'string_declare', 'state_def': {'variable_name': 's', 'body': 'hello'}, 'comments': ''}
{'state_type': 'string_iter', 'state_def': {'variable_name': 's', 'body': 'hello', 'index': 1}, 'comments': 'accessing character at 1'}
{'state_type': 'string_declare', 'state_def': {'variable_name': 's_sub', 'body': 'el'}, 'comments': 'creating new substring for slice(1, 3, None)'}
{'state_type': 'string_append', 'state_def': {'variable_name': 's', 'body': 'hello world', 'element': ' world'}, 'comments': ''}
{'state_type': 'string_declare', 'state_def': {'variable_name': 's_super', 'body': 'hello world'}, 'comments': 'creating new string with hello world appended to the original string'}
{'state_type': 'string_append', 'state_def': {'variable_name': 's_super', 'body': 'hello worldhello world', 'element': 'hello world'}, 'comments': ''}
```

