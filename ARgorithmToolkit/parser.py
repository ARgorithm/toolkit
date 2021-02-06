# pylint: skip-file
"""Parser module deals with parsing .config.json files
"""
import os
import json
import re

import typer
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "ARgorithm config",
    "description": "ARgorithm configuration file schema",
    "type" : "object",
    "properties" : {
        "argorithmID" : {
            "type" : "string"
        },
        "file" : {
            "type" : "string"
        },
        "function" : {
            "type" : "string"
        },
        "parameters" : {
            "type" : "object",
            "patternProperties" : {
                "^[a-zA-Z].*$":{
                    "type" : "object",
                    "anyOf" : [
                        {
                            "properties" : {
                                "type" : {
                                    "const" : "INT"
                                },
                                "description" : {
                                    "type" : "string"
                                },
                                "start" : {
                                    "type" : "integer",
                                },
                                "end" : {
                                    "type" : "integer"
                                }
                            },
                            "required" : ["type","description"],
                            "additionalProperties" : False
                        },
                        {
                            "properties" : {
                                "type" : {
                                    "const" : "FLOAT"
                                },
                                "description" : {
                                    "type" : "string"
                                },
                                "start" : {
                                    "type" : "number",
                                },
                                "end" : {
                                    "type" : "number"
                                }
                            },
                            "required" : ["type","description"],
                            "additionalProperties" : False
                        },
                        {
                            "properties" : {
                                "type" : {
                                    "const" : "STRING"
                                },
                                "description" : {
                                    "type" : "string"
                                },
                                "size" : {
                                    "type" : ["integer","string"]
                                }
                            },
                            "required" : ["type","description"],
                            "additionalProperties" : False
                        },
                        {
                            "properties" : {
                                "type" : {
                                    "const" : "ARRAY"
                                },
                                "description" : {
                                    "type" : "string"
                                },
                                "size" : {
                                    "type" : ["integer","string"]
                                },
                                "item-type" : {
                                    "type" : "string",
                                    "enum" : [
                                        "INT",
                                        "FLOAT",
                                        "STRING"
                                    ]
                                }
                            },
                            "required" : ["type","description","item-type"],
                            "additionalProperties" : False
                        },
                        {
                            "properties" : {
                                "type" : {
                                    "const" : "ARRAY"
                                },
                                "description" : {
                                    "type" : "string"
                                },
                                "row" : {
                                    "type" : ["integer","string"]
                                },
                                "col" : {
                                    "type" : ["integer","string"]
                                },
                                "item-type" : {
                                    "type" : "string",
                                    "enum" : [
                                        "INT",
                                        "FLOAT",
                                        "STRING"
                                    ]
                                }
                            },
                            "required" : ["type","description","col","row","item-type"],
                            "additionalProperties" : False
                        },
                    ]
                }
            },
            "additionalProperties" : False
        },
        "description" : {
            "type" : "string"
        },
        "example" : {
            "type" : "object",
            "additionalProperties" : True
        }
    },
    "required" : [
        "argorithmID" ,
        "file" ,
        "function" ,
        "description",
        "parameters",
        "example"
    ],
    "additionalProperties" : False
}

def multiline():
    """takes multiline input
    """
    buffer = ''
    while True:
        try:
            line = input()
        except EOFError:
            break
        if not line: 
            break
        buffer += line+"\n"
    return buffer[:-1]

class InputManager:
    """Create input window for argorithm
    """
    def input_data(self,parameters):
        """creates input as per as argorithm paramters
        """
        example = {}
        types = {
            "INT" : int,
            "FLOAT" : float,
            "STRING" : str,
        }
        for key in parameters:
            param = parameters[key]
            typer.clear()
            typer.secho("ARgortithm input",fg=typer.colors.GREEN)
            typer.echo(f"{key}\n{param['description']}")
            if param["type"] == "INT":
                retry = True
                while retry:
                    retry = False
                    value = typer.prompt("Enter integer value",type=int)
                    if "start" in param:
                        if value <= param["start"]:
                            typer.echo(f"Please enter value larger than {param['start']}")
                            retry = True
                    if "end" in param:
                        if value >= param["end"]:
                            typer.echo(f"Please enter value less than {param['end']}")
                            retry = True
            elif param["type"] == "FLOAT":
                retry = True
                while retry:
                    retry = False
                    value = typer.prompt("Enter float value",type=float)
                    if "start" in param:
                        if value <= param["start"]:
                            typer.echo(f"Please enter value larger than {param['start']}")
                            retry = True
                    if "end" in param:
                        if value >= param["end"]:
                            typer.echo(f"Please enter value less than {param['end']}")
                            retry = True
            elif param["type"] == "STRING":
                retry = True
                while retry:
                    retry = False
                    value = typer.prompt("Enter string value" , type=str)
                    if "size" in param:
                        if isinstance(param["size"],str):
                            assert isinstance(example[param["size"]],int)
                            if len(value) != example[param["size"]]:
                                typer.echo(f"length of string should be {example[param['size']]}")
                                retry = True
                        else:
                            if len(value) != param["size"]:
                                typer.echo(f"length of string should be {param['size']}")
                                retry = True
            elif param["type"] == "ARRAY":
                retry = True
                while retry:
                    retry = False
                    value = typer.prompt("Enter space separated series" , type=str).split(' ')
                    try:
                        value = [types[param['item-type']](x) for x in value]
                    except:
                        typer.echo(f"elements must be of type {types[param['item-type']]}")
                        retry = True
                    if "size" in param:
                        if isinstance(param["size"],str):
                            assert isinstance(example[param["size"]],int)
                            if len(value) != example[param["size"]]:
                                typer.echo(f"length of series should be {example[param['size']]}")
                                retry = True
                        else:
                            if len(value) != param["size"]:
                                typer.echo(f"length of series should be {param['size']}")
                                retry = True
            elif param["type"] == "MATRIX":
                retry = True
                while retry:
                    retry = False
                    if isinstance(param['row'],str):
                        row_count = example[param['row']]
                    else:
                        row_count = param['row']
                    if isinstance(param['col'],str):
                        col_count = example[param['col']]
                    else:
                        col_count = param['col']
                    typer.echo("Enter matrix input, elements in each row must be space separated")
                    typer.echo(f"no. of rows : {row_count}")
                    typer.echo(f"no. of elements per row : {col_count}")
                    value = []
                    for _ in range(row_count):
                        row_value = typer.prompt("",type=str).split(' ')
                        if len(row_value) != col_count:
                            typer.echo(f"row must have {col_count} space separated values")
                            retry = True
                        try:
                            row_value = [types[param['item-type']](x) for x in row_value]
                        except:
                            typer.echo(f"elements must be of type {types[param['item-type']]}")
                            retry = True
                        if retry:
                            break
                        value.append(row_value)
            example[key] = value
        return example

class ARgorithmConfig:
    """Validates and stores argorithm config
    """
    def __init__(self,filepath):
        self.validator = Draft7Validator(CONFIG_SCHEMA)
        directory = os.getcwd()
        if os.path.isfile( os.path.join(directory , f"{filepath}") ):
            with open(os.path.join(directory , f"{filepath}") , 'r') as configfile:
                data = json.load(configfile)
                try:
                    self.validator.validate(data)
                except ValidationError as ve:
                    raise ve
                self.config = data
        else:
            confirm = typer.confirm("Config file is missing. Start CLI config generator? ")
            if confirm:
                self.create(filepath)
            else:
                raise FileNotFoundError("No config file")

    def create(self,filepath):
        """implements the CLI config generator to run create config files using CLI
        """
        typer.clear()
        heading = typer.style("CONFIG GENERATOR", fg=typer.colors.CYAN , bold=True)
        typer.echo(heading)

        config = {}
        config["argorithmID"] = filepath.split(".")[0]
        config["file"] = config["argorithmID"]+".py"
        
        function_regex = re.compile("def.([A-Za-z]+).?\(\*\*kwargs\)")
        with open(config["file"],"r") as codefile:
            text = codefile.read()
        func_list = list(re.search(function_regex,text).groups())
        if len(func_list) == 0:
            raise KeyError("No valid function in ARgorithm code")
        function = typer.prompt("enter function name",default=func_list[0])
        while function not in func_list:
            function = typer.prompt("function not found. enter valid function name",default=func_list[0])
        config["function"] = function
        
        typer.echo("Enter ARgorithm Description (Press Enter twice to save and continue): ")
        config["description"] = multiline()
        config["parameters"] = {}
        
        typer.echo("Setting up input parameters")
        typer.echo("These parameters are used to define the input passed to your function as kwargs")
        print()
        confirm = typer.confirm("Do you want to add parameter?")
        while(confirm):
            parameter_name = typer.prompt("Enter parameter name")
            name_regex = r"^[A-Za-z].*$"
            while re.match(name_regex,parameter_name) is None:
                parameter_name = typer.prompt("Invalid name, re-enter parameter name")
            config["parameters"][parameter_name] = {}
            
            parameter_types = ["INT","FLOAT","STRING","ARRAY","MATRIX"]
            parameter_type = typer.prompt("Enter parameter type")
            while parameter_type not in parameter_types:
                typer.echo("Invalid parameter type. Accepted values: INT FLOAT ARRAY MATRIX STRING")
                parameter_type = typer.prompt("Enter parameter type")
            
            typer.secho("Enter parameter description (Press Enter twice to save and continue): ")
            parameter_description = multiline()
            config["parameters"][parameter_name]["description"] = parameter_description
            config["parameters"][parameter_name]["type"] = parameter_type
            
            if parameter_type == "INT":
                range_confirm = typer.confirm(f"Do you want to add range constraints to {parameter_name}")
                if range_confirm:
                    start = typer.prompt("Enter lower limit",type=int)
                    if start:
                        config["parameters"][parameter_name]["start"] = start
                    end = typer.prompt("Enter upper limit",type=int)
                    if end:
                        config["parameters"][parameter_name]["end"] = end
            
            elif parameter_type == "FLOAT":
                range_confirm = typer.confirm(f"Do you want to add range constraints to {parameter_name}")
                if range_confirm:
                    start = typer.prompt("Enter lower limit",type=float)
                    if start:
                        config["parameters"][parameter_name]["start"] = start
                    end = typer.prompt("Enter upper limit",type=float)
                    if end:
                        config["parameters"][parameter_name]["end"] = end
            
            elif parameter_type == "STRING":
                range_confirm = typer.confirm(f"Do you want to set a size constraint to {parameter_name}")
                if range_confirm:
                    size = typer.prompt(f"Enter integer size or name of pre-existing INT type parameter")
                    try:
                        size = int(size)
                    except ValueError:
                        assert size in config["parameters"]
                    config["parameters"][parameter_name]["size"] = size
            
            elif parameter_type == "ARRAY":
                item_types = ["INT","FLOAT","STRING"]
                item_type = typer.prompt("Enter type of array element")
                while item_type not in item_types:
                    typer.echo("Invalid element type. Accepted values: INT FLOAT STRING")
                    item_type = typer.prompt("Enter item type")
                config["parameters"][parameter_name]["item-type"] = item_type
                range_confirm = typer.confirm(f"Do you want to set a size constraint to {parameter_name}")
                if range_confirm:
                    size = typer.prompt(f"Enter integer size or name of pre-existing INT type parameter")
                    try:
                        size = int(size)
                    except ValueError:
                        assert size in config["parameters"]
                    config["parameters"][parameter_name]["size"] = size
            
            elif parameter_type == "MATRIX":
                item_types = ["INT","FLOAT","STRING"]
                item_type = typer.prompt("Enter type of array element")
                while item_type not in item_types:
                    typer.echo("Invalid element type. Accepted values: INT FLOAT STRING")
                    item_type = typer.prompt("Enter item type")
                config["parameters"][parameter_name]["item-type"] = item_type
                row = typer.prompt(f"Enter row size as integer or refer pre-existing INT type parameter")
                try:
                    row = int(row)
                    assert row > 0
                except ValueError:
                    assert row in config["parameters"]
                config["parameters"][parameter_name]["row"] = row
                col = typer.prompt(f"Enter col size as integer or refer pre-existing INT type parameter")
                try:
                    col = int(col)
                    assert col > 0
                except ValueError:
                    assert col in config["parameters"]
                config["parameters"][parameter_name]["col"] = col
            typer.clear()
            confirm = typer.confirm("Do you want to add parameter?")
        ip = InputManager()
        example = ip.input_data(config["parameters"])
        config["example"] = example
        directory = os.getcwd()
        with open(os.path.join(directory , f"{filepath}") , 'w') as configfile:
            json.dump(config,configfile)