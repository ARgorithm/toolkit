import json
import re
import os
import requests
from wasabi import msg , MarkdownRenderer , color , wrap

import ARgorithmToolkit

def valid_funcname(x):
    rules = r"[A-Za-z_]+"
    m = re.match(rules,x)
    if m!=None:
        return True
    else:
        return False

def init(*args):
    funcname = input('Enter name for ARgorithm File : ')
    while not valid_funcname(funcname):
        funcname = input('Please enter valid filename [A-Za-z_] : ')

    with open(f"{funcname}.py" , "w") as codefile:
        code_starter = """
import ARgorithmToolkit

def run(**kwargs):
    algo = ARgorithmToolkit.StateSet()

    #
    # Your code
    #

    return algo

        """
        codefile.write(code_starter)

    config = {
        "name" : funcname,
        "file" : funcname+".py",
        "function" : "run",
        "parameters" : {},
        "default" : {},
        "description" : ""
    }

    with open(f"{funcname}.config.json" , "w") as configfile:
        json.dump(config,configfile)

    msg.good('success')
    msg.divider("Template files generated")
    md=MarkdownRenderer()
    md.add("Please ensure that the config is up to date with your code function that has to be called should have the format of\n")
    md.add(wrap(color("def <function_name>(**kwargs)",fg="green",bold=True), indent=2) )
    md.add("and it should return a object of ARgorithmToolkit StateSet as that is what is storing the states to be rendered.")
    md.add(color("IT IS RECOMMENDED THAT YOU DON'T ALTER FILENAMES OF CODE FILE AND CONFIG FILE" , bold=True))
    print(md.text)
    msg.info('Run python -m ARgorithmToolkit submit',"when ready to submit")
    

def submit(*args):
    
    ## ACCESSING FILES
    
    if len(args)  == 2:
        if args[0] == "--name":
            funcname = args[1]
    else:
        funcname = input("enter name of file to be submitted ")
    
    funcname = funcname[:-3] if funcname[-3:] == ".py" else funcname
    directory = os.getcwd()
    
    if os.path.isfile( os.path.join(directory,funcname+".py")):
        if os.path.isfile( os.path.join(directory , f"{funcname}.config.json") ):
            pass
        else:
            msg.fail(f"cant find {funcname}.config.json")
            return 
    else:
        msg.fail(f"{funcname}.py not found")
        return

    msg.good('files found')
    
    ## VERIFYING FILES

    required_tags = {
        "name" : funcname,
        "file" : funcname+".py",
        "function" : "run",
        "parameters" : {},
        "default" : {},
        "description" : ""
    }

    with open(os.path.join(directory , f"{funcname}.config.json") , 'r') as configfile:    
        data = json.load(configfile)
        for key in required_tags:
            if key not in data:
                msg.fail(f"please check {funcname}.config.json {key} is missing")
                return
        for key in data:
            if key not in required_tags:
                msg.fail(f"please check {funcname}.config.json {key} is uneccessary")
                return
            if type(data[key]) != type(required_tags[key]):
                msg.fail(f"please check {key} in {funcname}.config.json")
                return

    #submitting
    local_file = f"{funcname}.py"

    url = "http://127.0.0.1/argorithms/insert"

    files = [
        ('document', (local_file, open(local_file, 'rb'), 'application/octet')),
        ('data', ('data', json.dumps(data), 'application/json')),
    ]

    try:
        r = requests.post(url, files=files) # Server isnt online yet XD
        if r.json()['status'] == "successful":
            msg.good('Submitted')
        else:
            raise ARgorithmToolkit.ARgorithmError("submission failed")
    except ARgorithmToolkit.ARgorithmError:
        msg.fail("Sorry , File couldnt be accepted")
    except:
        msg.info("Sorry , server offline")
    
def help(*args):
    md = MarkdownRenderer()
    msg.divider("CLI HELP",char='~')
    md.add("For creating the ARgorithm template")
    md.add(wrap(color("python -m ARgorithmToolkit init",fg="green",bold=True), indent=4) )
    md.add("For submitting to server")
    md.add(wrap(color("python -m ARgorithmToolkit submit",fg="green",bold=True), indent=4) )
    md.add(wrap(color("python -m ARgorithmToolkit submit --name <name>",fg="green",bold=True), indent=4) )
    print(md.text)
    print()