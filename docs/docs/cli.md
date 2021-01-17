# Command line interface

The command line interface for ARgorithmToolkit helps programmers to
create and manage their argorithms along with control and manage their
server.

<div class="termy">
```console
$  ARgorithm --help
Usage: ARgorithm [OPTIONS] COMMAND [ARGS]...

  ARgorithm CLI

Options:
  -l, --local           Connects to server running on localhost
  --install-completion  Install completion for the current shell.
  --show-completion     Show completion for the current shell, to copy it or
                        customize the installation.

  --help                Show this message and exit.

```
</div>

## Configure

This command can be used to set your own server IP. All your requests will be sent to this IP. If you are running server locally you dont need to configure IP, instead you can use the `-l` or `--local` flag to connect to local servers.

!!! info
	when using the local flag before use it before the command
	```console
	$ ARgorithm --local [COMMAND]
	```

<div class="termy">
```console
$ ARgorithm configure
# Enter server endpoint :$ http://myserverendpoint.com 
[SUCCESS]: CONNECTED
Cloud requests will now go to http://myserverendpoint.com
```
</div>

## Account

This command can only be used if the server you are connected to has authorization feature enabled. Refer the [configuration section](/server/#configuring-the-server) in [server setup](/server) to learn more about authentication and authorization setup.

The account command consists of two subcommands which are shown below

### New

The new subcommand in account creates a new account in the server. The
account you make will be ``programmer`` account. Learn more about `programmer` accounts in [introduction](/).

<div class="termy">
```console
$ ARgorithm account new
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
!!! info
	If you are already logged in and you want to login using different credentials,use the `-o` or `--override` flag after `login` command.
	
## Init

The `init` command is used to generate templates for ARgorithm. It creates a code file `.py` and a config file `.config.json`.

<div class="termy">
```console
$ ARgorithm init hello_world
Creating empty template for hello_world
[SUCCESS]: TEMPLATE GENERATED
refer documentation at https://argorithmtoolkit.readthedocs.io/ to learn how to use it
chech out examples at https://github.com/ARgorithm/Toolkit/tree/master/examples

$ ls
hello_world.config.json	hello_world.py
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
**hello_world.config.json**
```json
{
    "argorithmID": "hello_world", 
    "file": "hello_world.py", 
    "function": "run", 
    "parameters": {}, 
    "default": {}, 
	"description": ""
}
```

## Submit

The submit command is used to submit new ARgorithm to server. This comand takes the name of the argorithm for eg: `fibonacci`. In this case , it will search for `fibonacci.py` and `fibonacci.config.json` and after verification send them to server.

<div class="termy">
```console
$ ARgorithm submit fibonacci
[SUCCESS]: FILES FOUND
[SUCCESS]: FILES VERIFIED
[SUCCESS]: SUBMITTED
```
</div>

## List

The list command can be used to check what all ARgorithms are available in server. When `AUTH` is enabled, it shows the programmer email that created it, if not it shows the admin email.

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

The update command is used to overwrite/update pre-existing ARgorithm with different code or/and configuration. If `AUTH` is enabled, then ARgorithm can only be updated by its author or by a programmer with admin priveleges.

<div class="termy">
```console
$ ARgorithm update fibonacci
[SUCCESS]: FILES FOUND
[SUCCESS]: FILES VERIFIED
[SUCCESS]: SUBMITTED
```
</div>

## Test

The test command is used to run the argorithms in the server and observe the states. Here the states are not being printed as that can be long output. You can print the the states in json format in a file of your choice using the `--to-file` or `-t` option.

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

The delete command is used to delete ARgorithm from server. If `AUTH` is enabled, then ARgorithm can only be deleted by its author or by a programmer with admin priveleges.

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

The blacklist command can be used to block programmer accounts from submitting and testing ARgorithms and user accounts from running ARgorithms. This command can be used to handle cases of misconduct with server.

<div class="termy">
```console
$ ARgorithm admin blacklist sample@user.com
[SUCCESS]: BLACKLISTED ACCOUNT
```
</div>

### Whitelist

The whitelist command can be used to whitelist previously blacklisted
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
$ ARgorithm admin whitelist sample@user.com
[SUCCESS]: WHITELISTED ACCOUNT
```
</div>

By default, this subcommand only deletes the `user` account  (Refer [introduction](/)). To delete the progammer account as well use the `-p` or `--programmer` flag.
!!! warning
	It is not recommended to delete programmer accounts. Programmer accounts are useful for finding authors of ARgorithm. Try `blacklist` instead