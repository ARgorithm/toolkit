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
        "argorithmID" : funcname,
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
    
    # PARSING ARGS
    local = False
    name = False

    for i in range(len(args)):
        if args[i] == '-l' or args[i]=='--local':
            local = True
        elif args[i] == '-n' or args[i] == '--name':
            name = True
            try:
                funcname = args[i+1]
                assert valid_funcname(funcname)
            except:
                msg.warn('please follow up on -n or --name with a valid argorithm_ID')
                return
    
    ## ACCESSING FILES
    
    if name:
        funcname = funcname
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
        "argorithmID" : funcname,
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

    if local:
        url = "http://127.0.0.1/argorithms/insert"
    else:
        url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/argorithms/insert"

    files = [
        ('document', (local_file, open(local_file, 'rb'), 'application/octet')),
        ('data', ('data', json.dumps(data), 'application/json')),
    ]

    try:
        with msg.loading("sending..."):
            r = requests.post(url, files=files)
        if r.json()['status'] == "successful":
            msg.good('Submitted')
        else:
            raise ARgorithmToolkit.ARgorithmError("submission failed")
    except ARgorithmToolkit.ARgorithmError:
        msg.fail("Sorry , File couldnt be accepted")
    except:
        msg.info("Sorry , server offline")
    

def render_menu(menu:dict):
    md = MarkdownRenderer()
    count = 0
    msg.divider('Functions available')
    for k in menu['list']:
        count += 1
        md.add(f"{count}."+color(f"{k['argorithmID']}" , fg="green")+f"\n\t{k['description']}")
    print(md.text)
    option = int(input("Enter option number : "))
    try:
        assert option > 0 and option <= len(menu['list'])
    except:
        raise ARgorithmToolkit.ARgorithmError("opt out of range")
    return menu['list'][option-1]['argorithmID']

def delete(*args):
    local =  False
    if len(args) > 0:
        try:
            assert args[0]=='-l' or args[0]=='--local'
            local = True 
        except:
            msg.warn('the only flags supported are -l or --local')
            return
    try:
        if local:
            url = "http://127.0.0.1/argorithms/"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/argorithms/"
        with msg.loading("reading data"):
            r = requests.get(url+"list")
        msg.info('argorithm menu recieved')
        assert len(r.json()['list']) > 0
        argorithmID = render_menu(r.json())
    except AssertionError:
        msg.info("no function in server")
        return
    except ARgorithmToolkit.ARgorithmError:
        msg.fail("please enter valid option no.")
        return
    except:
        msg.info("Sorry , server offline")
        return

    try:
        data = {
            "argorithmID" : argorithmID
        }
        with msg.loading("deleting argorithm from server"):
            r = requests.post(f"{url}/delete", json=data)
        if r.json()['status'] == "successful":
            msg.good("deleted")
        print(json.dumps(r.json() , indent=2))
    except:
        msg.fail('argorithm delete has failed')
    

def test(*args):

    local =  False
    if len(args) > 0:
        try:
            assert args[0]=='-l' or args[0]=='--local'
            local = True 
        except:
            msg.warn('the only flags supported are -l or --local')
            return
    try:
        if local:
            url = "http://127.0.0.1/argorithms/"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/argorithms/"
        with msg.loading("reading data"):
            r = requests.get(url+"list")
        assert len(r.json()['list']) > 0
        msg.info('argorithm menu recieved')
        argorithmID = render_menu(r.json())
    except AssertionError:
        msg.warn("no function in server")
        return
    try:
        
        data = {
            "argorithmID" : argorithmID
        }
        with msg.loading("retrieving data from server"):
            r = requests.post(f"{url}/run", json=data)
        msg.good("Recieved states")
        print(json.dumps(r.json() , indent=2))
    except:
        msg.fail('Function call has failed')    
    
def help(*args):
    md = MarkdownRenderer()
    msg.divider("CLI HELP",char='~')
    md.add("For creating the ARgorithm template")
    md.add(wrap(color("python -m ARgorithmToolkit init",fg="green",bold=True), indent=4) )
    md.add("For submitting to server")
    md.add(wrap(color("python -m ARgorithmToolkit submit",fg="green",bold=True), indent=4) )
    md.add(wrap(color("python -m ARgorithmToolkit submit --name <name>",fg="green",bold=True), indent=4) )
    md.add("For submitting to local server")
    md.add(wrap(color("python -m ARgorithmToolkit submit --local",fg="green",bold=True), indent=4) )
    md.add(wrap(color("python -m ARgorithmToolkit submit --local --name <name>",fg="green",bold=True), indent=4) )
    md.add("For testing argorithm in server")
    md.add(wrap(color("python -m ARgorithmToolkit test",fg="green",bold=True), indent=4) )
    md.add("For testing argorithm in local server")
    md.add(wrap(color("python -m ARgorithmToolkit test --local",fg="green",bold=True), indent=4) )
    md.add("For deleting argorithm from server")
    md.add(wrap(color("python -m ARgorithmToolkit delete",fg="green",bold=True), indent=4) )
    md.add("For deleting argorithm from local server")
    md.add(wrap(color("python -m ARgorithmToolkit delete --local",fg="green",bold=True), indent=4) )
    print(md.text)
    print()