# pylint: skip-file
"""Parser module deals with parsing .config.json files
"""
import os
import json
import re
import math
import inspect
import typer
from jsonschema import Draft7Validator
from jsonschema.exceptions import ValidationError

import ARgorithmToolkit

with open(os.path.join(ARgorithmToolkit.__path__[0],'data/config.schema.json')) as schema:
    CONFIG_SCHEMA = json.load(schema)

config_cli_heading ="""
    +-----------------------------+
    |                             |
    |  ARGORITHM CONFIG GENERATOR |
    |                             |
    +-----------------------------+
"""

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

def master_heading():
    """Renders the ARgorithm config generator heading
    """
    text = typer.style(config_cli_heading,fg=typer.colors.BLUE,bold=True)
    typer.echo(text)

def heading(title,message):
    """Create a heading text

    Args:
        title (str): The title of the heading
        message (str): The message that
    """
    # typer.clear()
    text = typer.style(title.upper(),fg=typer.colors.BLUE,bold=True)
    typer.echo('-'*(len(text)+2))
    typer.echo(text)
    typer.echo('-'*(len(text)+2))
    typer.echo(message+"\n")
    return typer

def input_prompt(message,default=None,type=str,show_default=True):
    """Uses typer to create a single input field in CLI

    Args:
        message (str): The input field text
        type (type, optional): The type of input
        default (type, optional): The default value if user does not enter any value
        show_default (bool, optional): By default, True. If True shows the default value to user

    Returns:
        ip : The data entered by user
    """
    text = typer.style(message,fg=typer.colors.BLUE)
    if default:
        ip = typer.prompt(text,default=default,type=type,show_default=show_default)
    else:
        ip = typer.prompt(text,type=type)
    return ip

def confirm_prompt(message):
    """Uses typer to create a confirmation prompt

    Args:
        message (str): The text for confirmation

    Returns:
        flag: boolean value as entered by user
    """
    text = typer.style(message,fg=typer.colors.BLUE)
    flag = typer.confirm(text)
    return flag

def multiline_input_prompt(message):
    """Uses typer and ARgorithmToolkit.parser.multiline to create a multiline input prompt

    Args:
        message (str): The text for prompt

    Returns:
        ip: data entered by user
    """
    text = typer.style(message + ':',fg=typer.colors.BLUE)
    helptext = typer.style("Press ENTER on empty line to leave multiline input",fg=typer.colors.CYAN)
    typer.echo(text)
    typer.echo(helptext)
    ip = multiline()
    return ip

def info(message,data):
    """Display information using typer

    Args:
        message (str): Description of the information
        data : The data to be displayed
    """
    message = typer.style(message,fg=typer.colors.BLUE)
    data = typer.style(str(data),fg=typer.colors.GREEN)
    typer.echo(message+": "+data)

def warning(message):
    """Generate warning message using typer

    Args:
        message (str): warning text
    """
    text = typer.style("⚠  " + message , fg=typer.colors.YELLOW)
    typer.echo(text)

def find_parameters(filename,function):
    """Finds the keyword arguments accessed in the file

    find_parameters parses the code line by line and check which all keywords
    were accessed in the function code within the code file

    Args:
        filename (str): filename of the codefile
        function (str): function name where we need to check the kwargs

    Returns:
        params: list of keywords which need to be defined in config file
    """
    function_regex = re.compile(f"^def.([A-Za-z0-9]+).?\(\*\*kwargs\)")
    kwarg_regex = r"kwargs\[[\'\"]([A-Za-z0-9]+)[\'\"]\]"
    with open(filename,'r') as codefile:
        parameters = set()
        flag = False
        for line in codefile.readlines():
            search = re.search(function_regex,line)
            if search:
                func = list(search.groups())[0]
                flag = func == function
            if flag:
                search = re.search(kwarg_regex,line)
                if search:
                    params = list(search.groups())
                    for p in params:
                        parameters.add(p)
        return list(parameters)

def input_data(parameters):
    """Generates a input form based on the parameters in config

    Args:
        parameters (dict): The config parameters which will be used to generate the input fields

    Returns:
        example: The values for each param (key in parameters)
    """
    example = {}
    types = {
        "INT" : int,
        "FLOAT" : float,
        "STRING" : str,
    }
    heading("Enter input for ARgorithm","Based on argorithm parameters, input will be taken")
    for key in parameters:
        param = parameters[key]
        # typer.clear()
        info("\ninput keyword",key)
        info("Description",param['description'])

        def numeric_input(param,input_type):
            retry = True
            while retry:
                retry = False
                value = input_prompt("Enter integer value",type=input_type)
                if "start" in param:
                    if value <= param["start"]:
                        warning(f"Please enter value larger than {param['start']}")
                        retry = True
                if "end" in param:
                    if value >= param["end"]:
                        warning(f"Please enter value less than {param['end']}")
                        retry = True
            return input_type(value)

        def check_size(value,param,example):
            if "size" in param:
                if isinstance(param["size"],str):
                    assert isinstance(example[param["size"]],int)
                    if len(value) != example[param["size"]]:
                        warning(f"length of string should be {example[param['size']]}")
                        return True
                else:
                    if len(value) != param["size"]:
                        warning(f"length of string should be {param['size']}")
                        return True
            return False

        if param["type"] == "INT":
            value = numeric_input(param,int)

        elif param["type"] == "FLOAT":
            value = numeric_input(param,float)

        elif param["type"] == "STRING":
            retry = True
            while retry:
                retry = False
                value = input_prompt("Enter string value" , type=str)
                retry = check_size(value,param,example)

        elif param["type"] == "ARRAY":
            retry = True
            while retry:
                retry = False
                value = input_prompt("Enter space separated series" , type=str).split(' ')
                try:
                    value = [types[param['item-type']](x) for x in value]
                except:
                    warning(f"elements must be of type {types[param['item-type']]}")
                    retry = True
                retry = check_size(value,param,example)

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
                info(f"no. of rows", row_count)
                info(f"no. of elements per row",col_count)
                value = []
                for _ in range(row_count):
                    row_value = input_prompt("",type=str).split(' ')
                    if len(row_value) != col_count:
                        warning(f"row must have {col_count} space separated values")
                        retry = True
                    try:
                        row_value = [types[param['item-type']](x) for x in row_value]
                    except:
                        warning(f"elements must be of type {types[param['item-type']]}")
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
            confirm = typer.confirm("Start CLI config generator? ")
            if confirm:
                self.create(filepath)
            else:
                raise FileNotFoundError("No config file")

    def create(self,filepath):
        """implements the CLI config generator to run create config files using CLI
        """
        master_heading()

        config = {}

        info("ARgorithmID", filepath.split(".")[0])
        config["argorithmID"] = filepath.split(".")[0]
        config["file"] = config["argorithmID"]+".py"

        function_regex = re.compile("def.([A-Za-z]+).?\(\*\*kwargs\)")
        with open(config["file"],"r") as codefile:
            text = codefile.read()
        func_list = list(re.search(function_regex,text).groups())
        if len(func_list) == 0:
            raise KeyError("No valid function in ARgorithm code")
        info("Codefile found",config['file'])
        function = input_prompt("which function should be called",default=func_list[0])
        while function not in func_list:
            warning("function not found in code")
            function = input_prompt("enter valid function name",default=func_list[0])
        config["function"] = function

        config["description"] = multiline_input_prompt('Enter ARgorithm Description')
        config["parameters"] = {}

        def define_parameter(config,parameter_name):
            """Nested function that asks use information regarding parameter

            Args:
                config (dict): The config object where the parameter data has to be updated
                parameter_name (str): The parameter whose metadata is being collected

            Returns:
                config: Returns updated config object
            """
            parameter_types = ["INT","FLOAT","STRING","ARRAY","MATRIX"]
            parameter_type = input_prompt("Enter parameter type")
            while parameter_type not in parameter_types:
                warning("Invalid parameter type. Accepted values: INT FLOAT ARRAY MATRIX STRING")
                parameter_type = input_prompt("Enter parameter type")
            config["parameters"][parameter_name]["type"] = parameter_type

            def range_input(config,parameter_name):
                """Update config with the range for `INT` and `FLOAT` parameters

                Args:
                    config (dict): The config object where the parameter data has to be updated
                    parameter_name (str): The parameter whose metadata is being collected
                """
                start = input_prompt("Enter lower limit",type=int,default=-math.inf,show_default=False)
                if start != -math.inf:
                    config["parameters"][parameter_name]["start"] = start
                end = input_prompt("Enter upper limit",type=int,default=math.inf,show_default=False)
                if end != math.inf:
                    config["parameters"][parameter_name]["end"] = end

            def size_ref(data_field):
                """Inputs size constraint for `STRING`,`ARRAY` and `MATRIX` parameters

                Args:
                    data_field (str): What is the size constraint being used as

                Returns:
                    size: Returns size constraint
                """
                size = input_prompt(f"Enter integer {data_field} or name of pre-existing INT type parameter")
                try:
                    size = int(size)
                except ValueError:
                    assert size in config["parameters"]
                return size

            if parameter_type == "INT":
                range_confirm = confirm_prompt(f"Do you want to add range constraints to {parameter_name}")
                if range_confirm:
                    range_input(config,parameter_name)

            elif parameter_type == "FLOAT":
                range_confirm = confirm_prompt(f"Do you want to add range constraints to {parameter_name}")
                if range_confirm:
                    range_input(config,parameter_name)

            elif parameter_type == "STRING":
                range_confirm = confirm_prompt(f"Do you want to set a size constraint to {parameter_name}")
                if range_confirm:
                    config["parameters"][parameter_name]["size"] = size_ref("size")

            elif parameter_type == "ARRAY":
                item_types = ["INT","FLOAT","STRING"]
                item_type = input_prompt("Enter type of array element")
                while item_type not in item_types:
                    warning("Invalid element type. Accepted values: INT FLOAT STRING")
                    item_type = input_prompt("Enter item type")
                config["parameters"][parameter_name]["item-type"] = item_type
                range_confirm = confirm_prompt(f"Do you want to set a size constraint to {parameter_name}")
                if range_confirm:
                    config["parameters"][parameter_name]["size"] = size_ref("size")

            elif parameter_type == "MATRIX":
                item_types = ["INT","FLOAT","STRING"]
                item_type = input_prompt("Enter type of array element")
                while item_type not in item_types:
                    warning("Invalid element type. Accepted values: INT FLOAT STRING")
                    item_type = input_prompt("Enter item type")
                config["parameters"][parameter_name]["item-type"] = item_type
                config["parameters"][parameter_name]["row"] = size_ref('row size')
                config["parameters"][parameter_name]["col"] = size_ref('col_size')

            parameter_description = multiline_input_prompt("Enter parameter description")
            config["parameters"][parameter_name]["description"] = parameter_description

            return config

        typer.echo("Setting up parameters for your argorithm")
        typer.echo("input keywords are used to map the input passed to your function as kwargs")
        print()
        existing_parameters = find_parameters(config['file'],config['function'])
        if len(existing_parameters) > 0:
            text = typer.style('The following input keywords were found in code')
            typer.echo(text)
        for param in existing_parameters:
            typer.echo(typer.style("- "+param,fg=typer.colors.GREEN))
            config["parameters"][param] = {}

        for param in existing_parameters:
            info("input keyword",param)
            config = define_parameter(config,param)

        confirm = confirm_prompt("Do you want to another input keyword")
        while(confirm):
            typer.echo("add details for parameter")
            parameter_name = input_prompt("Enter parameter name")
            name_regex = r"^[A-Za-z].*$"
            while re.match(name_regex,parameter_name) is None:
                warning("Invalid name")
                parameter_name = input_prompt("re-enter parameter name")
            config["parameters"][parameter_name] = {}
            config = define_parameter(config,parameter_name)

            confirm = confirm_prompt("Do you want to add parameter?")
        example = input_data(config["parameters"])
        config["example"] = example
        directory = os.getcwd()
        with open(os.path.join(directory , f"{filepath}") , 'w') as configfile:
            json.dump(config,configfile)
