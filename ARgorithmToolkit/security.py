"""Security module contains functions to secure code files and prevent harmful code injection at server side
"""
import re
from ARgorithmToolkit import ARgorithmError
from pyflakes import checker

def injection_check(filename):
    count = 0
    f = open(filename, 'r')
    lines = f.readlines()
    for line in lines:
        if "import ARgorithmToolkit" in line or "from ARgorithmToolkit" in line:
            count +=1
    if count == 0:
        raise ARgorithmError("ARgorithmToolkit not imported")

    for line in lines:
        if line.startswith("from"):
            if re.search("^from\s+ARgorithmToolkit", line) == False:
                raise ARgorithmError("invalid module imported")

    
    for line in lines:
        if line.startswith("import"):
            if re.search("^import\s+ARgorithmToolkit", line) == False:
                raise ARgorithmError("invalid module imported")

    forbidden = ['logger','FileHandler', 'config']
    file_tokens = checker.make_tokens(lines)
    tokens = [token[1] for token in file_tokens if token[0] == 1]
    not_allowed = list(set(tokens) & set(forbidden))
    print(len(not_allowed))
    if len(not_allowed) > 0:
        raise Exception('Found forbidden variable')

