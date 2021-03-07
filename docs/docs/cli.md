# Command line interface

The command line interface for ARgorithmToolkit grants programmers control and helps them to
create and manage their argorithms as well as manage their
server.

<div class="termy">

```console
$  ARgorithm --help
Usage: ARgorithm [OPTIONS] COMMAND [ARGS]...

  ARgorithm CLI

Options:
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

```

</div>

## Connect

This command can be used to set your own server IP. All your requests will be sent to this IP. If you are running the server locally you can  configure the IP to local host by using the `-l` or `--local` flag .

<div class="termy">

```console
$ ARgorithm connect
# Enter server endpoint :$ http://myserverendpoint.com 
[SUCCESS]: CONNECTED
Cloud requests will now go to http://myserverendpoint.com
```

</div>

## Account

This command can only be used if the server you are connected to, has the authorization feature enabled. Refer to the [configuration section](/toolkit/server/#configuring-the-server) in [server setup](/toolkit/server) to learn more about authentication and authorization setup.

The account command consists of two subcommands which are shown below

### Signup

The new subcommand in account creates a new account in the server. The email you use will be registered as both, a ``programmer`` account and a `user` account. Learn more [here](/toolkit/server#interacting-with-server).

<div class="termy">

```console
$ ARgorithm account signup
# Enter email address:$ sample@user.com
[INFO]: PASSWORD CRITERIA
- between 8 to 25 characters
 - contains atleast one number
 - contains atleast lower case alphabet
 - contains atleast uppercase alphabet
# Enter password:$ ********
# Repeat for confirmation:$ ********* 
[SUCCESS]: ACCOUNT CREATED
These credentials will be used as both programmer and user credentials

```
</div>

### Login

The login command can be used to login to your server. Once logged in, these credentials will be used when you interact with the server.

<div class="termy">

```console
$ ARgorithm account login
# Enter email address:$ sample@user.com
# Enter password:$ ******** 
[SUCCESS]: LOGGED IN SUCCESSFULLY

```

</div>


### Logout

The logout command can be used to remove access token from system for fresh login

<div class="termy">

```console
$ ARgorithm account logout
```

</div>


## Init

The `init` command is used to generate templates for ARgorithm. It creates a code file `.py`.

<div class="termy">
```console
$ ARgorithm init hello_world
Creating empty template for hello_world
[SUCCESS]: TEMPLATE GENERATED
refer documentation at https://argorithm.github.io/toolkit/ to learn how to use it
chech out examples at https://github.com/ARgorithm/toolkit/tree/master/examples

$ ls
hello_world.py
```
</div>

The files generated are shown below
**hello_world.py**
```python
    import ARgorithmToolkit

    def run(**kwargs):
        algo = ARgorithmToolkit.StateSet()

        #
        # Your code
        #

        return algo
```

## Configure

The configure command can be used to start the CLI based Config Generator. This allows users to easily create config files step by step

<div class="termy">

```console
$ ARgorithm configure hello_world

    +-----------------------------+
    |  ARGORITHM CONFIG GENERATOR |
    +-----------------------------+

ARgorithmID: hello_world
Codefile found: hello_world.py
# which function should be called [run]:$ 
# Enter ARgorithm Description:$ hello world application

Setting up parameters for your argorithm
input keywords are used to map the input passed to your function as kwargs

# Do you want to another input keyword [y/N]:$ y

add details for parameter
# Enter parameter name:$ name
# Enter parameter type:$ STRING
# Enter parameter description:$ name of user

# Do you want to set a size constraint to name [y/N]:$ n
# Do you want to add parameter? [y/N]:$ n


ENTER INPUT FOR ARGORITHM
Based on argorithm parameters, input will be taken

input keyword: name
Description: name of user
# Enter string value:$ Alan

```

</div>

The `configure` command should be used only after you are done programming. You can check out the config schema [here](/toolkit/tutorials/config). You can use the `--blank` flag to generate a blank config file which you can edit using your code editor. You can then use then configure command with the `--validate` command to check whether its properly created. This method is recommended for beginners to get you used to the config creation process.

!!!warning
	The simulation shown here might be different according to your function code.

## Execute

The execute command runs the argorithm using the config file on your machine to simulate how it will run and generate states in server

<div class="termy">

```console
$ ARgorithm execute examples/fibonacci.py 
# Do you want to add user input? [y/N]:$ y
--------------------------
ENTER INPUT FOR ARGORITHM
--------------------------
Based on argorithm parameters, input will be taken

input keyword: n
Description: Enter the position of number in fibonacci series
# Enter integer value:$ 2
using parameters:
- n : 2

--------------------------------------------------
variable_declare
	The first fibonacci number
	id : 140413604661584
	variable_name : first
	value : 1

--------------------------------------------------
variable_declare
	The second fibonacci number
	id : 140413604661456
	variable_name : second
	value : 1

--------------------------------------------------
comment
	1 is the 2th fibonacci number

```

</div>

## Submit

The submit command is used to submit new ARgorithms to server. This command takes python code file as an argument. In this case, it will search for `fibonacci.py` and `fibonacci.config.json` and after verification send them to the server.

<div class="termy">

```console
$ ARgorithm submit fibonacci
[SUCCESS]: FILES VERIFIED
[SUCCESS]: FILES TESTED
[SUCCESS]: SUBMITTED
```

</div>

## List

The list command can be used to obtain a list of all the ARgorithms that are available in the server. When `AUTH` is enabled, it shows the programmer email that created it, if not it shows the admin email.

<div class="termy">

```console
$ ARgorithm list
- fibonacci
	by sample@user.com
	Parameters
		n : int
```
</div>

## Update

The update command is used to overwrite/update pre-existing ARgorithms with different code or/and configuration. If `AUTH` is enabled, then ARgorithm can only be updated by its author or by a programmer with admin privileges.

<div class="termy">
```console
$ ARgorithm update fibonacci
[SUCCESS]: FILES TESTED
[SUCCESS]: FILES VERIFIED
[SUCCESS]: SUBMITTED
```
</div>

## Test

The test command is used to run the argorithms in the server and observe the states. The states are not being printed in order to keep the output short. You can print the states in json format using the `--output` or `-o` option. By default, the data given in the configuration example is taken as input. By using the `--user-input` flag you can enter your own input to the argorithm. 

<div class="termy">

```console
$ ARgorithm test fibonacci
Found argorithm
- fibonacci
	by sample@user.com
	Parameters
		n : int

---------------STATES---------------------------

```

</div>

## Delete

The delete command is used to delete ARgorithms from the server. If `AUTH` is enabled, then ARgorithm can only be deleted by its author or by a programmer with admin priveleges.

<div class="termy">

```console
ARgorithm delete fibonacci
Found argorithm
- fibonacci
	by sample@user.com
	Parameters
		n : int
# Are you sure you want to delete it [y/N]:$ y
[INFO]: DELETED SUCCESSFULLY
```

</div>

## Admin

The admin command like the [account](#account) command can only be used if the server has authentication and authorization enabled. This command also has the added requirement that the programmer logged in must have admin priveleges. The subcommands under this command are used to manage accounts.

### Grant

The grant subcommand is used to grant other programmer accounts admin access. Blacklisted accounts cannot be granted admin priveleges.

<div class="termy">

```console
$ ARgorithm admin grant sample@user.com
[SUCCESS]: GRANTED ADMIN PRIVELEGES
```

</div>

### Revoke

The revoke subcommand is used to take away admin access from programmer
accounts. 

<div class="termy">

```console
$ ARgorithm admin revoke sample@user.com
[SUCCESS]: REVOKED ADMIN PRIVELEGES
```

</div>

### Blacklist

The blacklist command can be used to block programmer accounts from submitting and testing ARgorithms and user accounts from running ARgorithms. This command can be used to handle cases of misconduct with the server.

<div class="termy">

```console
$ ARgorithm admin blacklist sample@user.com
[SUCCESS]: BLACKLISTED ACCOUNT
```

</div>

### Whitelist

The whitelist command can be used to whitelist a previously blacklisted
accounts.

<div class="termy">

```console
$ ARgorithm admin whitelist sample@user.com
[SUCCESS]: WHITELISTED ACCOUNT
```

</div>

### Delete

The delete subcommand in admin is used to delete accounts.
!!! info
	This `delete` is different from [delete command](#delete) as this is a subcommand to the admin command
	```console
	$ ARgorithm admin delete [USER]
	```
	and that is to delete argorithms
	```console
	$ ARgorithm delete [ARGORITHM]
	```
<div class="termy">
```console
$ ARgorithm admin delete sample@user.com
[SUCCESS]: DELETED ACCOUNT
```
</div>

By default, this subcommand only deletes the `programmer` account  (Refer [here](/toolkit/server#interacting-with-server)). To delete the user account as well use the `-u` or `--user` flag.

!!! warning
	It is not recommended to delete programmer accounts. Programmer accounts are useful for finding authors of ARgorithm. Try `blacklist` instead