# Creating your configuration file

The `.config.json` plays an important role in creating argorithms. It stores metadata and useful information that can be used to manage, run and customise input to argorithm. In this tutorial, we will be covering the .config.json step by step created using `configure` command. So lets get started. We'll be creating a `sample.config.json` for `sample.py`

<div class="termy">

```console
$ ARgorithm init sample
Creating empty template for sample
[SUCCESS]: TEMPLATE GENERATED

$ ARgorithm configure sample
# Start CLI config generator?  [y/N]:$ y

+-----------------------------+
|  ARGORITHM CONFIG GENERATOR |
+-----------------------------+

```
</div>

## ARgorithm details

as seen in the [Getting started](/toolkit/start), the configuration has the following properties

| Key         | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| argorithmID | name of your ARgorithm , this is generally pre filled from when you run the init command. The name of your code file should be *name*.py and the config should be *name*.config.json. [will be fixed later] |
| file        | The file containing your codefile                            |
| function    | The function that is going to be called                      |
| parameters  | the parameters that your ARgorithm would need, this helps in anyone using your ARgorithm to understand what is the input format |
| example     | default parameters in case no parameters are passed          |
| description | The description of ARgorithm. Helpful to people using your ARgorithm as well as other developers |

The `argorithmID` and `file` are read from the filename. The `sample.py` file is parsed by the CLI to list out eligible functions. an eligible function is one that can be called by ARgorithm. Your ARgorithm code file must have a function of the form `def foo(**kwargs)`. The input will be passed as keyword arguments according to metadata in config file. If you have more than one eligible function, you can decide which one to call.

The `description` describe what the argorithm does so users know what the argorithm does and renders.

<div class="termy">

```console
ARgorithmID: sample
Codefile found: sample.py
# which function should be called [run]:$ run
Enter ARgorithm Description
Press ENTER on empty line to leave multiline input
# :$ sample config file to demonstrate config generator
```

</div>

```json hl_lines="2-5"
{!../../examples/sample.config.json!}
```

## Input parameters

The `parameters` property is what defines the input to your argorithm. The properties defined inside `parameters` as passed in keyword arguments to your function. Inside the `parameters`, we define the type and input constraints and in `example`, we give a default value that can be used as input on that keyword.

The CLI reads your code and shows you what iinput keywords your code looks for so that you can define its properties. you can add more parameters if you want but you will have to update your function to read that keyword argument.

!!!info
	Our current sample.py does not have any function code utilising keyword arguments. If your code does utilise some keyword arguments than you'll be asked to describe those particular input keywords.

<div class="termy">

```console
Setting up parameters for your argorithm
input keywords are used to map the input passed to your function as kwargs

The following input keywords were found in code
- array
```

</div>

Each parameter has two neccessary fields: `type` and `description`.

- `type`  : Decides the kind of input that is required to be taken from user. It can be of 5 types: `INT`,`FLOAT`,`STRING`,`ARRAY`,`MATRIX`. We'll cover creating parameters of each type below in detail.
- `description` : Tells the user what this input parameter is for. This is useful in telling the user about the importance of this input and how it will be processed.

### INT

Parameters with `INT` type expect an integer input. You can add constraint to the range in which the integer input should be by using the `start` and `end` properties. Below is the schema of a parameter with type `INT`

```json
"properties" : {
    "type" : {
    	"const" : "INT"
    },
    "description" : {
    	"type" : "string"
    },
    "start" : {
    	"type" : "integer"
    },
    "end" : {
    "type" : "integer"
    }
},
"required" : ["type","description"]
```

<div class="termy">

```console
# Enter parameter name:$ n
# Enter parameter type:$ INT
# Do you want to add range constraints to n [y/N]:$ y
# Enter lower limit:$ 0
# Enter upper limit: $ 
Enter parameter description
Press ENTER on empty line to leave multiline input
# :$ integer input
```

</div>

In this example, we have created a input keyword `n` which requires a integer input larger than 0. Please note that the range specified by `start` and `end` is inclusive of the values

$$
n\in [start,end]
$$

```json hl_lines="7"
{!../../examples/sample.config.json!}
```

### FLOAT

Parameters with `FLOAT` type expect an numerical input which include both integers and floating point numbers. You can add constraint to the range in which the numerical input should be by using the `start` and `end` properties. Below is the schema of a parameter with type `FLOAT`

```json
"properties" : {
    "type" : {
    	"const" : "FLOAT"
    },
    "description" : {
    	"type" : "string"
    },
    "start" : {
    	"type" : "number"
    },
    "end" : {
    	"type" : "number"
    }
},
"required" : ["type","description"],
```

<div class="termy">

```console
# Enter parameter name:$ f
# Enter parameter type:$ FLOAT
# Do you want to add range constraints to f [y/N]:$ n
Enter parameter description
Press ENTER on empty line to leave multiline input
# :$ floating point input
```

</div>

In this example, we have defined input keyword `f` as a `float` which has no range constraints. Ranges in `FLOAT` works similar to `INT`.

```json hl_lines="8"
{!../../examples/sample.config.json!}
```

### STRING

Parameters with type `STRING` take a single line string input from the user. This length of this string can be defined using the `size` property. `size` can store a integer value defining the size or can store the name of an `INT` type parameter so that size is input at runtime. `size` is an optional property, in case it is absent the user can enter a string of any length. Below is the schema of `STRING`

```json
"properties": {
  "type": {
    "const": "STRING"
  },
  "description": {
    "type": "string"
  },
  "size": {
    "type": ["integer", "string"]
  }
},
  "required": ["type", "description"]
```

<div class="termy">

```console
# Enter parameter name:$ s
# Enter parameter type:$ STRING
# Do you want to set a size constraint to s [y/N]:$ y
# Enter integer size or name of pre-existing INT type parameter:$ n
Enter parameter description
Press ENTER on empty line to leave multiline input
# :$ string input
```

</div>

Here we have defined `s` which is on type `string` and the length of string must be value stored in `n`.

$$
len(s) = n
$$

```json hl_lines="9"
{!../../examples/sample.config.json!}
```

!!!warning
	The input to `STRING` can be multiline but the input manager within CLI does not support that yet.

### ARRAY

Parameters with type `ARRAY` will expect a 1-dimensional series of items. The number of items in the series is controlled similarly to length of string i.e. using the `size` property. If `size` is not defined then the series can be of any size > 0. When using `ARRAY`, you need to define the `item-type` property as well. `item-type` can be `INT`,`FLOAT` or `STRING`. Below is the schema for `ARRAY` type parameters.

```json
"properties": {
  "type": {
    "const": "ARRAY"
  },
  "description": {
    "type": "string"
  },
  "size": {
    "type": ["integer", "string"]
  },
  "item-type": {
    "type": "string",
    "enum": ["INT", "FLOAT", "STRING"]
  }
},
"required": ["type", "description", "item-type"]
```

<div class="termy">

```console
# Enter parameter name:$ arr
# Enter parameter type:$ ARRAY
# Enter type of array element:$ INT
# Do you want to set a size constraint to arr [y/N]:$ n
Enter parameter description
Press ENTER on empty line to leave multiline input
# :$ array input
```

Here we have defined `arr` of type `ARRAY` where each element has to be of type `INT`. The `size` of `arr` has not been defined so it can be of any size. 

</div>

```json hl_lines="10-14"
{!../../examples/sample.config.json!}
```

### MATRIX

Parameters with type `MATRIX` will expect a1-dimensional series of items. The dimensions are controlled by `row` and `column` which is parsed similar to the `size` property. Unlike `size`, `row` and `col` are neccessary properties.. When using `MATRIX`, you need to define the `item-type` property as well. `item-type` can be `INT`,`FLOAT` or `STRING`. Below is the schema for `MATRIX` type parameters.

```json
"properties": {
  "type": {
    "const": "ARRAY"
  },
  "description": {
    "type": "string"
  },
  "row": {
    "type": ["integer", "string"]
  },
  "col": {
    "type": ["integer", "string"]
  },
  "item-type": {
    "type": "string",
    "enum": ["INT", "FLOAT", "STRING"]
  }
},
  "required": ["type", "description", "col", "row", "item-type"],
```

<div class="termy">

```console
# Enter parameter name:$ mat 
# Enter parameter type:$ MATRIX
# Enter type of array element:$ INT
# Enter integer row size or name of pre-existing INT type parameter:$ 4
# Enter integer col_size or name of pre-existing INT type parameter:$ 3
Enter parameter description
Press ENTER on empty line to leave multiline input
# :$ 2d input
```

</div>

Here we have defined `mat` as a 4x3 matrix in which elements are type of `INT`.

```json hl_lines="15-21"
{!../../examples/sample.config.json!}
```

## Adding default values

Now that we have defined our input parameters, we need to provide some default values to these in the `example` property.

1. These values are used in case the user doesnt want to give custom input or gives faulty input to keywords
2. These values are used for testing purposes as well

The CLI generates input fields according to the parameters in which you can enter you details.

<div class="termy">

```console
----------------------------------------
ENTER INPUT FOR ARGORITHM
----------------------------------------
Based on argorithm parameters, input will be taken

input keyword: n
Description: integer input
# Enter integer value:$ 6

input keyword: f
Description: floating point input
# Enter integer value:$ 3.4

input keyword: s
Description: string input
# Enter string value:$ sample

input keyword: arr
Description: array input
# Enter space separated series:$ 3 4 1 2

input keyword: mat
Description: 2d input
Enter matrix input, elements in each row must be space separated
no. of rows: 4
no. of elements per row: 3
# :$ 1 4 2
# :$ 5 4 2
# :$ 5 6 4
# :$ 8 1 9

```

</div>

```json hl_lines="23-33"
{!../../examples/sample.config.json!}
```

## Alternative methods

You can generate a blank `sample.config.json` by using the `--config` option in the `init` command. You can then edit this file in your code editor.

!!!info
	We are working on GUI interface which should make the config generation process even more simpler