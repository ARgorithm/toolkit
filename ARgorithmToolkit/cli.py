# pylint: disable=no-self-use
# pylint: disable=too-many-statements
# pylint: disable=raise-missing-from
"""CLI tool for ARgorithm made using typer.

Example:
    $ ARgorithm --help
"""

import os
import sys
import re
import json
import traceback
import requests
import typer
from halo import Halo
import ARgorithmToolkit
from ARgorithmToolkit.security import injection_check,execution_check
from ARgorithmToolkit.parser import input_data,create,validateconfig,ValidationError

CLOUD_URL = "https://argorithm.el.r.appspot.com"
CACHE_DIR = typer.get_app_dir("ARgorithm")

app = typer.Typer(help="ARgorithm CLI")

class Messager():
    """Class for pretty printing messages using typer."""
    def msg(self,tag:str,title:str,message:str,color:str):
        """Pretty messaging for standard log messages."""
        code = typer.style(f"[{tag.upper()}]: {title.upper()}" , fg=color , bold=True)
        typer.echo(code)
        if message:
            typer.echo(message)

    def info(self,title:str,message:str=""):
        """Information message."""
        self.msg("info",title,message,typer.colors.BLUE)

    def warn(self,title:str,message:str=""):
        """Warning message."""
        self.msg("error",title,message,typer.colors.YELLOW)

    def fail(self,title:str,message:str=""):
        """Error message."""
        self.msg("critical error",title,message,typer.colors.RED)

    def good(self,title:str,message:str=""):
        """Success message."""
        self.msg("success",title,message,typer.colors.GREEN)

    def menuitem(self,argorithm):
        """pretty print argorithm details."""
        head = typer.style(f"- {argorithm['argorithmID']}",fg=typer.colors.GREEN,bold=True)
        typer.echo(head)
        typer.secho(f"by {argorithm['maintainer']}",fg=typer.colors.CYAN)
        if argorithm['description']:
            typer.echo(f"{argorithm['description']}")
        if argorithm['parameters']:
            typer.echo("Parameters")
            for key in argorithm['parameters']:
                if argorithm['parameters'][key]['description']:
                    typer.echo(f"- {key} : {argorithm['parameters'][key]['description']}")
                else:
                    typer.echo(f"- {key}")
        typer.echo()

    def state(self,states):
        """pretty print states."""
        states = states['data']
        for state in states:
            typer.echo('\n'+'-'*50)
            typer.secho(state['state_type'],bold=True)
            typer.secho('\t'+state['comments'],fg=typer.colors.CYAN)
            if state['state_def']:
                for key in state['state_def']:
                    typer.echo(f"\t{key} : {state['state_def'][key]}")

msg = Messager()


class Settings():
    """handles connection endpoints."""
    endpoint:str=CLOUD_URL

    def get_endpoint(self):
        """returns required endpoint."""
        config_file = os.path.join(CACHE_DIR , "config")
        if os.path.isfile(config_file):
            with open(config_file,"r") as conf:
                self.endpoint = conf.read()
        return self.endpoint

    def set_endpoint(self,url):
        """set up cloud endpoint."""
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.get(url+"/argorithm")
            if rq.status_code == 200:
                msg.good("Connected",f"web requests will now go to {url}")
            else:
                raise AttributeError("Not a server endpoint")
        except ValueError as ve:
            msg.warn("Please try again with proper URL")
            raise typer.Exit(1) from ve
        except AttributeError as ex:
            msg.fail(str(ex))
            raise typer.Exit(1) from ex
        except Exception as ex:
            msg.fail("Endpoint couldnt be found.")
            print(ex)
            raise typer.Exit(2) from ex
        config_file = os.path.join(CACHE_DIR , "config")
        with open(config_file,'w') as config:
            config.write(url)

app_settings = Settings()

class AuthManager():
    """Handles authentication."""
    def __init__(self):
        """sets up credfile to store credentials."""
        self.credfile = os.path.join(CACHE_DIR,".credentials")

    def register(self):
        """registers account."""
        email = typer.prompt("Enter email address")
        msg.info("Password criteria",'- between 8 to 25 characters\n - contains atleast one number\n - contains atleast lower case alphabet\n - contains atleast uppercase alphabet')
        rules = r"^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{8,25}$"
        password = typer.prompt("Enter password",confirmation_prompt=True,hide_input=True)
        if not re.search(rules,password):
            msg.warn("password unacceptable")
            typer.Exit(1)
            return
        url = app_settings.get_endpoint()+'/programmers/register'
        data = {
            "username" : email,
            "password" : password
        }
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.post(url,data)
        except requests.RequestException as rqe:
            msg.fail("Connection failed",str(rqe))
            raise typer.Abort()
        if rq.status_code == 200:
            msg.good("Account created","These credentials will be used as both programmer and user credentials")
            return
        if rq.status_code == 409:
            msg.warn("Invalid email","email is already in use. Try login")
            raise typer.Exit(0)
        msg.fail("Error","Contact developer")

    def login_prompt(self):
        """login prompt to enter credentials."""
        email = typer.prompt("Enter email address")
        password = typer.prompt("Enter password",hide_input=True)
        url = f"{app_settings.get_endpoint()}/programmers/login"
        data = {
            "username" : email,
            "password" : password
        }
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.post(url,data)
        except requests.RequestException as rqe:
            msg.fail("Connection failed",str(rqe))
            raise typer.Abort()
        if rq.status_code == 404:
            msg.warn("User not found","please enter valid email")
        elif rq.status_code == 500:
            msg.fail("Server error","contact developer")
        elif rq.status_code == 401:
            msg.warn("incorrect password")
        elif rq.status_code == 402:
            msg.warn("please verify account first")
        elif rq.status_code == 200:
            msg.good("logged in successfully","credentials saved in cache")
            token = json.loads(rq.content)['access_token']
            with open(self.credfile,'w+') as cred:
                cred.write(token)
            return token
        raise typer.Exit(1)

    def get_token(self,flag=False):
        """returns valid authorization token."""
        url = app_settings.get_endpoint()
        if os.path.isfile(self.credfile):
            with open(self.credfile,'r') as cred:
                token = cred.read()
            try:
                with Halo(text='Connecting', spinner='dots'):
                    rq = requests.post(f"{url}/programmers/verify" , headers = {"authorization" : "Bearer "+token})
            except requests.RequestException as rqe:
                msg.fail("Connection failed",str(rqe))
                raise typer.Abort()
            if rq.status_code == 200:
                override = False
                if flag:
                    override = typer.confirm("Found existing valid token. do you want to login again?")
                if not override:
                    return token
            else:
                msg.warn("Valid credentials not found","Please enter login credentials again")
        token = self.login_prompt()
        with open(self.credfile,'w+') as cred:
            cred.write(token)
        return token

    def get_header(self):
        """Get authentication header."""
        header=None
        if self.auth_check():
            token = self.get_token()
            header={"authorization":"Bearer "+token}
        return header

    def auth_check(self):
        """checks if AUTH is enabled on server."""
        try:
            url = app_settings.get_endpoint() + "/auth"
            try:
                with Halo(text='Connecting', spinner='dots'):
                    rq = requests.get(url)
            except requests.RequestException as rqe:
                msg.fail("Connection failed",str(rqe))
                raise typer.Abort()
            if rq.status_code == 200:
                return True
            return False
        except Exception as ex:
            msg.warn("authentication error",str(ex))
            raise typer.Abort()

    def remove_token(self):
        """logout by deleting access token."""
        try:
            os.remove(self.credfile)
            msg.good("Logged out")
        except Exception:
            msg.warn("No credentials found")

authmanager = AuthManager()

def name_check(value:str):
    """checks validity of argorithmID."""
    rules = r"^[A-Za-z_]+$"
    m = re.search(rules,value)
    if m is None:
        msg.fail("Invalid name" , "argorithm name should be [A-Za-z_]")
        raise typer.Exit(code=1)
    return value

def autocomplete(incomplete:str):
    """autocomplete function for finding argorithms."""
    local_directory , incomplete  = os.path.split(incomplete)
    if local_directory == '':
        local_directory = '.'
    files = os.listdir(local_directory)
    res = []
    l = len(incomplete)
    for filename in files:
        if filename[:l] == incomplete and filename[-3:] == '.py':
            if local_directory == '.':
                res.append(filename)
            else:
                res.append(os.path.join(local_directory,filename))
    return res

class CodeManager():
    """Handles file verification, testing and submissions."""
    def __init__(self,filename):
        """gets filepath for code file and config file."""
        directory , argorithm_file = os.path.split(filename)
        argorithmID = name_check(argorithm_file[:-3])
        directory = os.getcwd() if not directory else directory
        self.codepath = os.path.join(directory,argorithm_file)
        self.configpath = os.path.join(directory,argorithmID+".config.json")
        if not os.path.isfile(self.codepath):
            msg.warn("Python file not found",'use the init command first')
            raise typer.Abort()
        if not os.path.isfile(self.configpath):
            msg.warn("config file not found",'use the configure command first')
            raise typer.Abort()

    def verify(self):
        """checks whether files are valid or not."""
        injection_check(self.codepath)
        validateconfig(self.configpath)

    def test(self,prompt:bool=False):
        """Execute code locally."""
        try:
            with open(self.configpath,'r') as configfile:
                config = json.load(configfile)
                parameters = config['example']
            if prompt:
                user = typer.confirm("Do you want to add user input?")
                if user:
                    parameters = input_data(config['parameters'])
            if parameters and prompt:
                typer.echo("using parameters:")
                for key in parameters:
                    typer.echo(f"- {key} : {parameters[key]}")
            return execution_check(self.codepath,self.configpath,parameters)
        except AssertionError:
            msg.warn("Execution Failed","execution should return ARgorithmToolkit.StateSet")
            raise typer.Exit(1)
        except Exception:
            msg.warn("Execution Failed")
            traceback.print_exception(*sys.exc_info())
            raise typer.Exit(1)

    def generate_submission(self):
        """Generate the files for submission."""
        _ , local_file = os.path.split(self.codepath)
        with open(self.configpath,'r') as configfile:
            data = json.load(configfile)
        files = [
            ('file', (local_file, open(self.codepath, 'rb'), 'application/octet')),
            ('data', ('data', json.dumps(data), 'application/json')),
        ]
        header = authmanager.get_header()
        return files,header

    def submit(self):
        """Submit code to server."""
        files,header = self.generate_submission()
        url = app_settings.get_endpoint()+"/argorithms/insert"
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.post(url,files=files,headers=header)
        except requests.RequestException as rqe:
            msg.fail("Connection failed",str(rqe))
            raise typer.Abort()
        if rq.status_code == 200:
            msg.good("Submitted")
        elif rq.status_code == 409:
            msg.warn("Already exists","An argorithm with this name already exists,try another argorithm name")
        elif rq.status_code == 406:
            msg.warn("File name was invalid","The name shoud be of type [A-Za-z_]")
        elif rq.status_code == 400:
            msg.warn("Incorrect file format","please refer documentation")
        else:
            msg.fail("Application error")

    def update(self):
        """Update code in servers."""
        files,header = self.generate_submission()
        url = app_settings.get_endpoint()+"/argorithms/update"
        try:
            with Halo(text='Connecting', spinner='dots'):
                rq = requests.post(url,files=files,headers=header)
        except requests.RequestException as rqe:
            msg.fail("Connection failed",str(rqe))
            raise typer.Abort()
        if rq.status_code == 200:
            msg.good("updated")
        elif rq.status_code == 404:
            msg.warn("Not found","Try submit command to add argorithm to server")
        elif rq.status_code == 401:
            msg.warn("Unauthorized","Only author of argorithm or admin is allowed to alter argorithms")
        else:
            msg.fail("Application error")

@app.command()
def connect(
    local:bool = typer.Option(False,"--local",'-l',help="Connects to server running on localhost",show_default=False)
):
    """Connect to your endpoint.

    More info at https://argorithm.github.io/toolkit/cli#connect
    """
    if local:
        endpoint = "http://localhost"
    else:
        endpoint = typer.prompt("Enter server endpoint",default=app_settings.get_endpoint())
    app_settings.set_endpoint(endpoint)

@app.command()
def init(
        name:str = typer.Argument(...,help="The name given to the argorithm [A-Za-z_]",callback=name_check)
    ):
    """Create Blank code template and config template for ARgorithm.

    More info at https://argorithm.github.io/toolkit/cli#init
    """
    typer.echo(f"Creating empty template for {name}")
    with open(os.path.join(ARgorithmToolkit.__path__[0],'data/template.py',),'rb') as template:
        starter = template.read()

    filename = f"{name}.py"
    with open(filename , "wb") as codefile:
        codefile.write(starter)

    msg.good("Template generated","refer documentation at https://argorithm.github.io/toolkit")

@app.command()
def configure(
    filepath:str=typer.Argument(... , help="The code file to be configured" , autocompletion=autocomplete),
    blank:bool=typer.Option(False,'-b','--blank',help="create blank config file"),
    validate:bool=typer.Option(False,'-v','--validate',help="only validate existing config file,Dont create")
    ):
    """Create configuration file for argorithm.

    More info at https://argorithm.github.io/toolkit/cli#configure
    """
    directory,filename = os.path.split(filepath)
    name = filename[:-3]
    if not os.path.isfile(filepath):
        msg.warn("Python file not found",'use the init command first')
        raise typer.Abort()
    configpath = os.path.join(os.getcwd(),directory,name+".config.json")
    try:
        validateconfig(configpath)
        typer.echo("Valid config file found")
        if not blank:
            if not validate:
                redo = typer.confirm(f"Do you remake the {name}.config.json?")
                if redo:
                    create(configpath)
            raise typer.Exit(0)
    except ValidationError:
        if not validate and not blank:
            create(configpath)
            raise typer.Exit(0)
    except FileNotFoundError:
        if validate:
            msg.warn("Config file not found")
            raise typer.Exit(0)
        if not blank:
            create(configpath)
            raise typer.Exit(0)
    config = {
        "argorithmID" : name,
        "file" : name+".py",
        "function" : "run",
        "parameters" : {},
        "example" : {},
        "description" : ""
    }
    with open(configpath, "w") as configfile:
        json.dump(config,configfile,indent=4)


@app.command()
def submit(
        filename:str=typer.Argument(... , help="The code file to be submitted" , autocompletion=autocomplete)
    ):
    """Submit argorithms to server.

    More info at https://argorithm.github.io/toolkit/cli#submit
    """
    code = CodeManager(filename)
    with Halo(text='Verifying', spinner='dots'):
        code.verify()
    msg.good("Files verified")
    with Halo(text='Testing', spinner='dots'):
        code.test(prompt=False)
    msg.good("Files verified")
    code.submit()

@app.command()
def update(
        filename:str=typer.Argument(... , help="The code file to be submitted" , autocompletion=autocomplete)
    ):
    """Updates pre existing argorithms at server.

    More info at https://argorithm.github.io/toolkit/cli#update
    """
    code = CodeManager(filename)
    with Halo(text='Verifying', spinner='dots'):
        code.verify()
    msg.good("Files verified")
    with Halo(text='Testing', spinner='dots'):
        code.test(prompt=False)
    msg.good("Files verified")
    code.update()


@app.command()
def delete(
    argorithm_id:str = typer.Argument(... , help="argorithmID of function to be deleted.")
    ):
    """Deletes argorithm from server.

    More info at https://argorithm.github.io/toolkit/cli#delete
    """
    params = search(argorithm_id)
    flag = typer.confirm("Are you sure you want to delete it?")
    if not flag:
        typer.echo("Not deleting")
        raise typer.Abort()
    header=authmanager.get_header()

    data = {
        "argorithmID" : params["argorithmID"],
    }
    url = app_settings.get_endpoint()+"/argorithms/delete"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.info("Deleted successfully",)
    elif rq.status_code == 401:
        msg.warn("Not authorized","only author of argorithm or admin can delete it")
    else:
        msg.fail("application error")

def search(argid,show=True):
    """Searches argorithm on server."""
    url = app_settings.get_endpoint()+"/argorithms/view/"+argid
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.get(url)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        data = json.loads(rq.content)
        if show:
            typer.echo("Found argorithm")
            msg.menuitem(data)
        return data
    if rq.status_code == 404:
        msg.warn("Not found",f"{argid} not found in database")
        raise typer.Exit(1)
    msg.fail("Application error")
    raise typer.Exit(1)

@app.command("list")
def list_argorithms():
    """Get list of argorithms in server.

    More info at https://argorithm.github.io/toolkit/cli#list
    """
    url = app_settings.get_endpoint()+"/argorithms/list"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.get(url)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        menu = json.loads(rq.content)
        if len(menu) == 0:
            msg.warn("No argorithms")
            raise typer.Exit(1)
        for item in menu:
            msg.menuitem(item)

@app.command()
def test(
    argorithm_id:str = typer.Argument(... , help="argorithmID of function to be called. If not passed then menu will be presented"),
    output:bool = typer.Option(False,'--output','-o',help="print results in json format",show_default=False),
    user_input:bool = typer.Option(False,'--user-input','-u',help="if present, takes input from user",show_default=False),
    ):
    """Test argorithms stored in server.

    More info at https://argorithm.github.io/toolkit/cli#test
    """
    params = search(argorithm_id,show=not output)
    header=authmanager.get_header()

    data = {
        "argorithmID" : params["argorithmID"],
        "parameters" : params["example"]
    }
    if user_input:
        data["parameters"] = input_data(params["parameters"])
    url = app_settings.get_endpoint()+"/argorithms/run"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        if output:
            print(rq.text)
        else:
            msg.state(json.loads(rq.content))
    elif rq.status_code == 401:
        msg.warn("Authentication failed",json.loads(rq.content)['detail'])
    else:
        msg.fail("application error")

@app.command()
def execute(
    filename:str=typer.Argument(... , help="The code file to be submitted" , autocompletion=autocomplete)
    ):
    """Execute locally stored ARgorithms.

    More info at https://argorithm.github.io/toolkit/cli#execute
    """
    code = CodeManager(filename)
    code.verify()
    states = [x.content for x in code.test(prompt=True)]
    msg.state({"data" : states})


account_app = typer.Typer(help="Manages account")
app.add_typer(account_app,name="account")

@account_app.command()
def login():
    """Log in to ARgorithmServer.

    Only is AUTH is enabled on server. More info at
    https://argorithm.github.io/toolkit/cli#login
    """
    if not authmanager.auth_check():
        msg.warn("AUTH disabled at server")
        raise typer.Exit(0)
    authmanager.get_token(flag=True)

@account_app.command()
def signup():
    """Create new programmer and user account in ARgorithmServer.

    Only is AUTH is enabled on server. More info at
    https://argorithm.github.io/toolkit/cli#signup
    """
    if not authmanager.auth_check():
        msg.warn("AUTH disabled at server")
        raise typer.Exit(0)
    authmanager.register()

@account_app.command()
def logout():
    """Remove pre-existing login credentials.

    More info at https://argorithm.github.io/toolkit/cli#logout
    """
    authmanager.remove_token()

admin_app = typer.Typer(help="Administrator level methods")
app.add_typer(admin_app,name="admin")

@admin_app.callback()
def admin_auth_check():
    """Check if auth is enabled for admin routes."""
    if not authmanager.auth_check():
        msg.warn("AUTH is disabled at this endpoint")
        raise typer.Exit(1)

@admin_app.command()
def grant(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """Grants admin acess.

    More info at https://argorithm.github.io/toolkit/cli#grant
    """
    data = {
        "email" : email
    }
    header=authmanager.get_header()
    url = app_settings.get_endpoint()+"/admin/grant"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("granted admin priveleges")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 406:
        msg.warn("Blacklisted email","This email is blacklisted thus cannot be granted admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command()
def revoke(
        email:str=typer.Argument( ... , help="The account email that would be lose admin access")
    ):
    """Revokes admin acess.

    More info at https://argorithm.github.io/toolkit/cli#revoke
    """
    data = {
        "email" : email
    }
    header=authmanager.get_header()
    url = app_settings.get_endpoint()+"/admin/revoke"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("revoked admin priveleges")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command("delete")
def account_delete(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access"),
        user:bool=typer.Option(False,'-u','--user',help="If flag is present, it will delete the user account")
    ):
    """Deletes account.

    Requires admin priveleges. More info at
    https://argorithm.github.io/toolkit/cli#delete_1
    """
    data = {
        "email" : email
    }
    header=authmanager.get_header()
    if user:
        url = app_settings.get_endpoint()+"/admin/delete_user"
    else:
        url = app_settings.get_endpoint()+"/admin/delete_programmer"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("deleted account")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command()
def blacklist(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """Blacklists account.

    Requires admin priveleges. More info at
    https://argorithm.github.io/toolkit/cli#blacklist
    """
    data = {
        "email" : email
    }
    header=authmanager.get_header()
    url = app_settings.get_endpoint()+"/admin/black_list"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("blacklisted account")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")

@admin_app.command()
def whitelist(
        email:str=typer.Argument( ... , help="The account email that would be granted admin access")
    ):
    """Whitelist accounts.

    Requires admin priveleges. More info at
    https://argorithm.github.io/toolkit/cli#whitelist
    """
    data = {
        "email" : email
    }
    header=authmanager.get_header()
    url = app_settings.get_endpoint()+"/admin/white_list"
    try:
        with Halo(text='Connecting', spinner='dots'):
            rq = requests.post(url,json=data,headers=header)
    except requests.RequestException as rqe:
        msg.fail("Connection failed",str(rqe))
        raise typer.Abort()
    if rq.status_code == 200:
        msg.good("whitelisted account")
    elif rq.status_code == 401:
        msg.warn("Not authorized","You need admin priveleges")
    elif rq.status_code == 404:
        msg.warn("Not found","No such email registered")
    else:
        msg.fail("Application Error")
