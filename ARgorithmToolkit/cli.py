import argparse
import getpass
import json
import re
import os
import requests
from wasabi import msg , MarkdownRenderer , color , wrap
from ARgorithmToolkit import ARgorithmError

from os.path import expanduser
HOME = expanduser("~")

def auth_check(local=False):
    try:
        if local:
            url = "http://127.0.0.1/auth"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/auth"
        r = requests.get(url).json()
        return r["status"] == True
    except:
        return False
       
def login(local=False):
    try:
        email = input("enter email : ")
        password = getpass.getpass("enter password : ")
        data = {
            "email" : email,
            "password" : password
        }
        if local:
            url = "http://127.0.0.1/users/login"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/users/login"
        r = requests.post(url,json=data)
        return r.json()['token']
    except:
        raise ARgorithmError("Failed Authentication")

def sign_up(local=False):
    try:
        email = input("enter email : ")
        rules = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        m = re.match(rules,email)
        if m == None:
            msg.fail("invalid email")
            raise ARgorithmError("Invalid email")

        print("\n\tPASSWORD ACCEPTS A-Z,a-z,0-9\nMUST CONTAIN ATLEAST ONE LOWERCASE , ONE UPPERCASE AND ONE NUMBER\nLENGTH BETWEEN 8-25 CHARACTERS")
        password = getpass.getpass("enter password : ")
        rules = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,25}$"
        m = re.match(rules,password)
        if m == None:
            msg.fail("invalid password")
            raise ARgorithmError("invalid password")
        
        repassword = getpass.getpass("re-enter password : ")
        if password != repassword:
            msg.fail("passwords don't match")
            raise ARgorithmError("password mismatch")
        
        data = {
            "email" : email,
            "password" : password
        }
        if local:
            url = "http://127.0.0.1/users/register"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/users/register"
        r = requests.post(url,json=data)
        if r.json()['status'] == "already exists":
            msg.info(f"Account already registered",f"please login with {email}")
            raise ARgorithmError("Account already registerd")
    except:
        raise ARgorithmError("Failed Registration")

def get_token(local=False,overwrite=False):
    try:
        storage = True
        CACHE_DIR = os.path.join(HOME,".argorithm")
        if not os.path.isdir(CACHE_DIR):
            os.mkdir(CACHE_DIR)
        FILENAME = os.path.join(CACHE_DIR , "creds.json")
    
        if not overwrite:
            if os.path.isfile(FILENAME):
                with open(FILENAME,'r') as cred:
                    token = json.load(cred)['token']
                if local:
                    url = "http://127.0.0.1/users/verify"
                else:
                    url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/users/verify"
                r = requests.get(url,headers={"x-access-token" : token})
                if r.json()['status'] == True:
                    return token
    except:
        storage = False
    try:
        token = login(local=local)
        if storage:
            with open(FILENAME,'w') as cred:
                json.dump({"token" : token},cred)
        return token
    except:
        raise ARgorithmError("Failed Authentication")

def valid_funcname(x):
    rules = r"[A-Za-z_]+"
    m = re.match(rules,x)
    if m!=None:
        return True
    else:
        return False

def init():
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

def submit(local=False,name=None):
    
    ## ACCESSING FILES
    
    if name:
        funcname = name
    else:
        funcname = input("enter name of file to be submitted : ")
    
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

    #authorizing

    try:
        auth_flag =  auth_check(local=local)
        if auth_flag:
            token = get_token(local=local)
    except:
        msg.fail("Authentication failed") 
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
            if auth_flag:
                r = requests.post(url, files=files , headers={"x-access-token" : token})
            else:
                r = requests.post(url, files=files)
        if r.json()['status'] == "successful":
            msg.good('Submitted')
        else:
            raise ARgorithmError("submission failed")
    except ARgorithmError:
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
        raise ARgorithmError("opt out of range")
    return menu['list'][option-1]['argorithmID']

def delete(local=False):
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
    except ARgorithmError:
        msg.fail("please enter valid option no.")
        return
    except:
        msg.info("Sorry , server offline")
        return

     #authorizing

    try:
        auth_flag =  auth_check(local=local)
        if auth_flag:
            token = get_token(local=local)
    except:
        msg.fail("Authentication failed") 
        return

    try:
        data = {
            "argorithmID" : argorithmID
        }
        with msg.loading("deleting argorithm from server"):
            if auth_flag:
                r = requests.post(f"{url}/delete", json=data , headers={"x-access-token" : token})
            else:
                r = requests.post(f"{url}/delete", json=data)
        if r.json()['status'] == "successful":
            msg.good("deleted")
        print(json.dumps(r.json() , indent=2))
    except:
        msg.fail('argorithm delete has failed')
    

def test(local=False):

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


def cmd():
    parser = argparse.ArgumentParser(prog="ARgorithm",description="ARgorithm CLI",formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(title="command",dest="command",help='try command --help for more details',required=True)

    init_parser = subparsers.add_parser(
        'init',description="initialises files for argorithm", usage='init [-h,--help]')
    
    submit_parser = subparsers.add_parser(
        'submit',description="submits files to argorithm-server")
    submit_parser.add_argument('-n','--name',action="store",type=str,help="provide name of ARgorithm to be submitted optional")
    submit_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
    
    test_parser = subparsers.add_parser(
        'test' , description="tests argorithm stored in server")
    test_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
    
    delete_parser = subparsers.add_parser(
        'delete' , description="deletes argorithm stored in server")
    delete_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
     
    account_parser = subparsers.add_parser(
        'account' , description="account operations on server")
    account_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
    account_subparsers = account_parser.add_subparsers(title="subcommand",dest="subcommand",help='you can login or create a new account',required=True)

    login_parser = account_subparsers.add_parser(
        'login' , description="sign in to server to authorise actions")
    login_parser.add_argument('-o' , '--overwrite' , action="store_true" , help="overwrites any pre-existing login")
    sign_parser = account_subparsers.add_parser(
        'new' , description="create new account in server to authorise actions")
    

    args = parser.parse_args()
    if args.command == "init":
        init()
    elif args.command == "submit":
        submit(local=args.local,name=args.name)
    elif args.command == "test":
        test(local=args.local)
    elif args.command == 'delete':
        delete(local=args.local)
    elif args.command == 'account':
        if args.subcommand == 'login':
            try:
                auth_flag =  auth_check(local=args.local)
                if auth_flag:
                    token = get_token(local=args.local,overwrite=args.overwrite)
                else:
                    msg.warn("No Authentication Feature at endpoint")
                    return
            except:
                msg.fail("Authentication failed") 
                return
            msg.good("Successfully Authenticated")
    
        if args.subcommand == 'new':
            try:
                auth_flag =  auth_check(local=args.local)
                if auth_flag:
                    sign_up(local=args.local)
                else:
                    msg.warn("No Authentication Feature at endpoint")
                    return
            except:
                msg.fail("Registration failed") 
                return
            msg.good("Successfully Registrated")
