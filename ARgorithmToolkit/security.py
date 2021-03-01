"""Security module contains functions to secure code files and prevent harmful
code injection at server side."""
import re
import json
import importlib
from pyflakes import checker
from ARgorithmToolkit import ARgorithmError,StateSet

FORBIDDEN = [
    'STORAGE_FOLDER','config',
    'LRUCache','logger','PerformanceMonitor',
    'eval','exec'
]

def injection_check(filename:str):
    """Checks whether given code file does not contain harmful code to server
    operation.

    Args:
        filename (str): the code file to check

    Raises:
        ARgorithmError: Raised if possible harmful code injection
    """
    count = 0
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines:
            if "import ARgorithmToolkit" in line or "from ARgorithmToolkit" in line:
                count +=1
        if count == 0:
            raise ARgorithmError("ARgorithmToolkit not imported")

        for line in lines:
            if line.startswith("from"):
                if not re.search(r"^from\s+ARgorithmToolkit", line):
                    raise ARgorithmError("invalid module imported")

        for line in lines:
            if line.startswith("import"):
                if not re.search(r"^import\s+ARgorithmToolkit", line):
                    raise ARgorithmError("invalid module imported")

        text = '\n'.join(lines)
        file_tokens = checker.make_tokens(text)
        tokens = [token[1] for token in file_tokens if token[0] == 1]
        not_allowed = list(set(tokens) & set(FORBIDDEN))
        if len(not_allowed) > 0:
            raise ARgorithmError('possible code injection')

def execution_check(filename:str,configpath:str,parameters:dict):
    """Executes the file on kwargs provided by programmer in the config file's
    `example` key.

    Args:
        filename (str): The file with the ARgorithm code to be checked
        config (dict): The config file for ARgorithm
    """
    module_name = filename.split('/')[-1][:-3]
    spec = importlib.util.spec_from_file_location(module_name,filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with open(configpath,'r') as configfile:
        config = json.load(configfile)
    func = getattr(module , config["function"])
    output = func(**parameters)
    assert isinstance(output,StateSet)
    return output.states
