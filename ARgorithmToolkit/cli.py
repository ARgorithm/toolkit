"""ARgorithmToolkit comes with a powerful CLI to interact with your ARgorithm server and to assist in the process of ARgorithm creation.
It is installed and setup when you install the ARgorithmToolkit package. you can call it in the commandline::
    
    $ ARgorithm -h

"""

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
CLOUD_URL = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com"

def auth_check(local=False):
    """This function is used to check whether the server accessed by programmer has authorization setup or not

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.

    Returns:
        bool: If true means server requires authentication flag
    """
    
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
    """Logs in programmer into the server where they would be submitting their code

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.

    Raises:
        ARgorithmError: Raised when login fails due to some reason

    Returns:
        str: JWT token used for authorization headers
    """
    try:
        print("You need to enter sign in credentials")
        email = input("enter email : ")
        password = getpass.getpass("enter password : ")
        data = {
            "email" : email,
            "password" : password
        }
        if local:
            url = "http://127.0.0.1/programmers/login"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/programmers/login"
        r = requests.post(url,json=data)
        return r.json()['token']
    except:
        raise ARgorithmError("Failed Authentication")

def sign_up(local=False):
    """Creates new account for programmer on specified server

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.

    Raises:
        ARgorithmError: Raised if account creation fails
    """
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
            url = "http://127.0.0.1/programmers/register"
        else:
            url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/programmers/register"
        r = requests.post(url,json=data)
        if r.json()['status'] == "already exists":
            msg.info(f"Account already registered",f"please login with {email}")
            raise ARgorithmError("Account already registerd")
    except:
        raise ARgorithmError("Failed Registration")

def get_token(local=False,overwrite=False):
    """Checks whether the programmer is logged in or not. If logged in , then the JWT token is verified else login action is triggered

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
        overwrite (bool, optional): If true then existing login is ignored and a fresh login is triggered. Defaults to False.

    Raises:
        ARgorithmError: If token verification and login both fail

    Returns:
        str : JWT token used for authorization header
    """
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
                    url = "http://127.0.0.1/programmers/verify"
                else:
                    url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/programmers/verify"
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
    """Checks whether ARgorithmID selected by programmer is acceptable or not

    Args:
        x (str): ARgorithmID

    Returns:
        bool: whether the selected ARgorithID is acceptable or not
    """
    rules = r"[A-Za-z_]+"
    m = re.match(rules,x)
    if m!=None:
        return True
    else:
        return False

def init():
    """Creates empty template for the programmer to develop argorithm on.
    """
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
    msg.info('Run ARgorithm submit',"when ready to submit")

def submit(local=False,name=None):
    """Submits ARgorithm code file as well as ARgorithm config file to server

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
        name (str, optional): Checks whether the name of file is given in the command if not it will ask for name

    Raises:
        ARgorithmError: Raised if submission fails
    """
    
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
            if 'message' in r.json():
                print(r.json()['message'])
            raise ARgorithmError("submission failed")
    except ARgorithmError:
        msg.fail("Sorry , File couldnt be accepted")
    except:
        msg.info("Sorry , server offline")

def update(local=False,name=None):
    """Submits new ARgorithm code file as well as new ARgorithm config file for already existing ARgorithm in server

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
        name (str, optional): Checks whether the name of file is given in the command if not it will ask for name

    Raises:
        ARgorithmError: Raised if updation fails
    """
    
    if name:
        funcname = name
    else:
        funcname = input("enter name of file to be sent : ")
    
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
        url = "http://127.0.0.1/argorithms/update"
    else:
        url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/argorithms/update"

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
            msg.good('updated')
        elif r.json()['status'] == "not present":
            msg.warn('ARgorithm not found') 
        else:
            if 'message' in r.json():
                print(r.json()['message'])
            raise ARgorithmError("update failed")
    except ARgorithmError:
        msg.fail("Sorry , ARgorithm couldnt be updated")
    except Exception as e:
        msg.info("Sorry , server offline")


def render_menu(menu:dict):
    """Shows list of available ARgorithms on server

    Args:
        menu (dict): response from server

    Raises:
        ARgorithmError: If server does not contain any ARgorithm or programmer has provided invalid option

    Returns:
        str: ARgorithmID of selected ARgorithm
    """
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
    """Deletes ARgorithm from server

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
        name (str, optional): Checks whether the name of file is given in the command if not it will ask for name

    Raises:
        ARgorithmError: Raised if deletion fails
    """
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
        else:
            if 'message' in r.json():
                print(r.json()['message'])
            raise ARgorithmError("update failed")
    except:
        msg.fail('argorithm delete has failed')
    

def test(local=False):
    """Tests ARgorithm in server

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
        name (str, optional): Checks whether the name of file is given in the command if not it will ask for name

    Raises:
        ARgorithmError: Raised if test fails
    """
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
        with msg.loading("retrieving data from server"):
            if auth_flag:
                r = requests.post(f"{url}/run", json=data, headers={"x-access-token" : token})
            else:
                r = requests.post(f"{url}/run", json=data)
        msg.good("Recieved states")
        print(json.dumps(r.json() , indent=2))
    except:
        msg.fail('Function call has failed')    

def grant(local=False):
    """Grants an account admin priveleges

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
    """
    try:
        auth_flag =  auth_check(local=local)
        if auth_flag:
            token = get_token(local=local)
        else:
            msg.info("Auth disabled on Server")
            return
    except:
        msg.fail("Authentication failed") 
        return

    if local:
        url = "http://127.0.0.1/admin/grant"
    else:
        url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/admin/grant"
    email = input("enter email that you want to grant admin access to : ")
    r = requests.post(url,json={"email" : email},headers={"x-access-token":token})
    try:
        if r.json()['status'] == 'successful':
            msg.good(f"{email} is now an admin")
        elif r.json()['status'] == 'access denied':
            msg.warn(f"You dont have admin priveleges")
        elif r.json()['status'] == 'Not Found':
            msg.warn(f"{email} cant be found")
        elif r.json()['status'] == 'blacklisted':
            msg.info(f"{email} is blacklisted")
        else:
            msg.fail("server failure")
    except:
        msg.fail("server failure")

def revoke(local=False):
    """Revokes admin priveleges from specified account

    Args:
        local (bool, optional): If true checks for local server instance. Defaults to False.
    """
    try:
        auth_flag =  auth_check(local=local)
        if auth_flag:
            token = get_token(local=local)
        else:
            msg.info("Auth disabled on Server")
            return
    except:
        msg.fail("Authentication failed") 
        return

    if local:
        url = "http://127.0.0.1/admin/revoke"
    else:
        url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/admin/revoke"
    email = input("enter email that you want to revoke admin access from : ")
    r = requests.post(url,json={"email" : email},headers={"x-access-token":token})
    try:
        if r.json()['status'] == 'successful':
            msg.warn(f"{email} is not an admin")
        elif r.json()['status'] == 'access denied':
            msg.warn(f"You dont have admin priveleges")
        elif r.json()['status'] == 'Not Found':
            msg.warn(f"{email} cant be found")
        else:
            msg.fail("server failure")
    except:
        msg.fail("server failure")

def delete_account(local=False,programmer=False):
    try:
        auth_flag =  auth_check(local=local)
        if auth_flag:
            token = get_token(local=local)
        else:
            msg.info("Auth disabled on Server")
            return
    except:
        msg.fail("Authentication failed") 
        return

    if local:
        url = "http://127.0.0.1/admin/"
    else:
        url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/admin/"
    if programmer:
        url = url + "delete_programmer"
    else:
        url = url + "delete_user"
    email = input("enter email that you want delete : ")
    r = requests.post(url,json={"email" : email},headers={"x-access-token":token})
    try:
        if r.json()['status'] == 'successful':
            msg.good(f"{email} is deleted")
        elif r.json()['status'] == 'access denied':
            msg.warn(f"You dont have admin priveleges")
        elif r.json()['status'] == 'Not Found':
            msg.warn(f"{email} cant be found")
        else:
            msg.fail("server failure")
    except:
        msg.fail("server failure")

def blacklist(local=False,black=True):
    try:
        auth_flag =  auth_check(local=local)
        if auth_flag:
            token = get_token(local=local)
        else:
            msg.info("Auth disabled on Server")
            return
    except:
        msg.fail("Authentication failed") 
        return

    if local:
        url = "http://127.0.0.1/admin/"
    else:
        url = "http://ec2-13-127-193-38.ap-south-1.compute.amazonaws.com/admin/"
    if black:
        url = url + "black_list"
        email = input("enter email that you want blacklist : ")
    else:
        url = url + "white_list"
        email = input("enter email that you want whitelist : ")
    
    r = requests.post(url,json={"email" : email},headers={"x-access-token":token})
    try:
        if r.json()['status'] == 'successful':
            if black:
                msg.info(f"{email} is blacklisted")
            else:
                msg.good(f"{email} is whitelisted")
        elif r.json()['status'] == 'access denied':
            msg.warn(f"You dont have admin priveleges")
        elif r.json()['status'] == 'Not Found':
            msg.warn(f"{email} cant be found")
        else:
            msg.fail("server failure")
    except:
        msg.fail("server failure")


def cmd():
    """Generates Command Line Interface using powerful ``argparse`` library
    """
    parser = argparse.ArgumentParser(prog="ARgorithm",description="ARgorithm CLI",formatter_class=argparse.RawDescriptionHelpFormatter)
    subparsers = parser.add_subparsers(title="command",dest="command",help='try command --help for more details',required=True)

    init_parser = subparsers.add_parser(
        'init',description="initialises files for argorithm", usage='init [-h,--help]')
    
    # configure_parser = subparsers.add_parser(
    #     'configure',description="sets cloud server address", usage='configure [-h,--help]')

    submit_parser = subparsers.add_parser(
        'submit',description="submits files to argorithm-server")
    submit_parser.add_argument('-n','--name',action="store",type=str,help="provide name of ARgorithm to be submitted optional")
    submit_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
    
    update_parser = subparsers.add_parser(
        'update',description="submits new code files for already existing argorithm in argorithm-server")
    update_parser.add_argument('-n','--name',action="store",type=str,help="provide name of ARgorithm to be updated optional")
    update_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
    

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
    
    admin_parser = subparsers.add_parser(
        'admin' , description="admin operations on server"
    )
    admin_parser.add_argument('-l','--local',action="store_true", help='connects to local server instead of cloud server')
    admin_subparsers = admin_parser.add_subparsers(title="subcommand",dest="subcommand",help='you can blacklist/whitelists accounts , grant/revoke admin access',required=True)
    grant_parser = admin_subparsers.add_parser(
        'grant' , description="grant programmer admin priveleges"
    )
    revoke_parser = admin_subparsers.add_parser(
        'revoke' , description="revoke programmer admin priveleges"
    )
    blacklist_parser = admin_subparsers.add_parser(
        'blacklist' , description="blacklist programmer from using application"
    )
    whitelist_parser = admin_subparsers.add_parser(
        'whitelist' , description="whitelist previously blacklisted programmer"
    )
    delete_account_parser = admin_subparsers.add_parser(
        'delete' , description="delete account"
    )
    delete_account_parser.add_argument('-p' , '--programmer' , action="store_true" , help="deletes programmer account. if not given deletes user account")
    
    args = parser.parse_args()
    if args.command == "init":
        init()
    # elif args.command == "configure":
    #     configure()
    elif args.command == "submit":
        submit(local=args.local,name=args.name)
    elif args.command == "update":
        update(local=args.local,name=args.name)
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
    elif args.command == 'admin':
        if args.subcommand == "grant":
            grant(args.local)
        elif args.subcommand == "revoke":
            revoke(args.local)
        elif args.subcommand == "blacklist":
            blacklist(args.local)
        elif args.subcommand == "whitelist":
            blacklist(args.local,black=False)
        elif args.subcommand == "delete":
            delete_account(args.local,args.programmer)
        
        