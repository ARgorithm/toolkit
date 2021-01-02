Command Line Interface
======================

The command line interface for ARgorithmToolkit helps programmers to
create and manage their argorithms along with control and manage their
server.

.. code:: bash

    $ ARgorithm -h
    usage: ARgorithm [-h]
                     {init,configure,submit,update,test,delete,account,admin} ...

    ARgorithm CLI

    optional arguments:
      -h, --help            show this help message and exit

    command:
      {init,configure,submit,update,test,delete,account,admin}
                            try command --help for more details

configure
---------

This command can be used to set your own server IP.

.. code:: bash

    $ ARgorithm configure -h
    usage: configure [-h,--help]

    sets cloud server address

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm configure
    Enter server endpoint or press ENTER to connect to ARgorithm common server : https://customendpoint.com
    ✔ Cloud requests will now go to https://customendpoint.com

account
-------

In case the server you are connected to has the authentication feature
enabled , you need to sign up and login before interacting with server.

.. code:: bash

    $ ARgorithm account -h
    usage: ARgorithm account [-h] [-l] {login,new} ...

    account operations on server

    optional arguments:
      -h, --help   show this help message and exit
      -l, --local  connects to local server instead of cloud server

    subcommand:
      {login,new}  you can login or create a new account

If you are connecting to a local instance of server , please use the
``-l`` or ``--local`` flag before you select your subcommand

.. code:: bash

    $ ARgorithm account -l {login,new}

new
~~~

The new subcommand in account creates a new account in the server. The
account you make will be ``programmer`` account.

.. code:: bash

    $ ARgorithm account new -h
    usage: ARgorithm account new [-h]

    create new account in server to authorise actions

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm account -l new
    enter email : sampleuser@email.com    

        PASSWORD ACCEPTS A-Z,a-z,0-9
    MUST CONTAIN ATLEAST ONE LOWERCASE , ONE UPPERCASE AND ONE NUMBER
    LENGTH BETWEEN 8-25 CHARACTERS
    enter password : 
    re-enter password : 
    ✔ Successfully Registrated

login
~~~~~

The login subcommand is used to login into your account.

.. code:: bash

    $ ARgorithm account login -h
    usage: ARgorithm account login [-h] [-o]

    sign in to server to authorise actions

    optional arguments:
      -h, --help       show this help message and exit
      -o, --overwrite  overwrites any pre-existing login

.. code:: bash

    $ ARgorithm account login
    enter email : sampleuser@email.com
    enter password : 
    ✔ Successfully Authenticated

The CLI saves your last login. If the token is still accepted then you
dont have to pass your credentials again

.. code:: bash

    $ ARgorithm account login
    ✔ Successfully Authenticated

You can always use the ``-o`` or ``--override`` flag to overwrite new
login credentials when you are already logged in

``bash $ ARgorithm account login -o enter email : sampleuser@email.com enter password :  ✔ Successfully Authenticated``

init
----

The ``init`` command is used to generate templates for ARgorithm. It
creates a code file ``.py`` and a config file ``.config.json``

.. code:: bash

    $ ARgorithm init -h
    usage: init [-h,--help]

    initialises files for argorithm

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm init
    Enter name for ARgorithm File : hello_world
    ✔ success

    ========================== Template files generated ==========================
    Please ensure that the config is up to date with your code function that has to be called should have the format of


      def <function_name>(**kwargs)

    and it should return a object of ARgorithmToolkit StateSet as that is what is storing the states to be rendered.

    IT IS RECOMMENDED THAT YOU DON'T ALTER FILENAMES OF CODE FILE AND CONFIG FILE
    ℹ run ARgorithm submit
    when ready to submit

This command will generate ``hello_world.py`` and
``hello_world.config.json``

**hello\_world.py**

.. code:: python

    import ARgorithmToolkit

    def run(**kwargs):
        algo = ARgorithmToolkit.StateSet()

        #
        # Your code
        #

        return algo

**hello\_world.config.json**

.. code:: json

    {
        "argorithmID": "hello_world", 
        "file": "hello_world.py", 
        "function": "run", 
        "parameters": {}, 
        "default": {}, 
        "description": ""
    }

submit
------

The submit command is used to submit new ARgorithm to server.

.. code:: bash

    $ ARgorithm submit -h
    usage: ARgorithm submit [-h] [-n NAME] [-l]

    submits files to argorithm-server

    optional arguments:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  provide name of ARgorithm to be submitted optional
      -l, --local           connects to local server instead of cloud server

You can pass the name of your ARgorithm using the\ ``-n`` or ``--name``
. If you dont , the CLI will prompt you to input it so its not
neccessary to put the flag. When submitting to local instance of server
, be sure to pass the ``-l`` or ``--local`` flag.

.. code:: bash

    $ ARgorithm submit
    enter name of file to be submitted : hello_world
    ✔ files found
    ✔ Submitted

If you are not signed in , then the submit command will prompt you to
sign in using your credentials.

update
------

The update command is used to overwrite/update pre-existing ARgorithm
with different code or/and configuration

.. code:: bash

    $ ARgorithm update -h
    usage: ARgorithm update [-h] [-n NAME] [-l]

    submits new code files for already existing argorithm in argorithm-server

    optional arguments:
      -h, --help            show this help message and exit
      -n NAME, --name NAME  provide name of ARgorithm to be updated optional
      -l, --local           connects to local server instead of cloud server

You can pass the name of your ARgorithm using the\ ``-n`` or ``--name``
. If you dont , the CLI will prompt you to input it so its not necessary
to put the flag. When interacting with local instance of server , be
sure to pass the ``-l`` or ``--local`` flag.

.. code:: bash

    $ ARgorithm update -l
    enter name of file to be sent : hello_world
    ✔ files found
    ✔ updated

If you are not signed in , then the update command will prompt you to
sign in using your credentials. You can only update an ARgorithm if you
are it's original creator or you have **admin** priveleges.

delete
------

The delete command is used to delete ARgorithm from server.

.. code:: bash

    $ ARgorithm delete -h
    usage: ARgorithm delete [-h] [-l]

    deletes argorithm stored in server

    optional arguments:
      -h, --help   show this help message and exit
      -l, --local  connects to local server instead of cloud server

When interacting with local instance of server , be sure to pass the
``-l`` or ``--local`` flag.

.. code:: bash

    $ ARgorithm delete -l
    ℹ argorithm menu recieved

    ============================ Functions available ============================
    1.bubblesort
        demonstrate bubble sort

    2.fibonacci
        Print the nth fibonacci number

    3.hello_world
        
    Enter option number : 3
    ✔ deleted

If you are not signed in , then the delete command will prompt you to
sign in using your credentials. You can only delete an ARgorithm if you
are it's original creator or you have **admin** priveleges.

test
----

The test command allows to check whether your ARgorithm is executing as
expected in the server.

.. code:: bash

    $ ARgorithm test -h
    usage: ARgorithm test [-h] [-l]

    tests argorithm stored in server

    optional arguments:
      -h, --help   show this help message and exit
      -l, --local  connects to local server instead of cloud server

When interacting with local instance of server , be sure to pass the
``-l`` or ``--local`` flag.

.. code:: bash

    $ ARgorithm test -l
    ℹ argorithm menu recieved

    ============================ Functions available ============================
    1.bubblesort
        demonstrate bubble sort

    2.fibonacci
        Print the nth fibonacci number
    Enter option number : 2
    ✔ Recieved states

    #... states printed here ...

If you are not signed in , then the delete command will prompt you to
sign in using your credentials.

admin
-----

When authentication and authorization is enabled on server , admin users
can control accounts and access using the admin command. Using the admin
command needs admin priveleges.

.. code:: bash

    $ ARgorithm admin -h
    usage: ARgorithm admin [-h] [-l] {grant,revoke,blacklist,whitelist,delete} ...

    admin operations on server

    optional arguments:
      -h, --help            show this help message and exit
      -l, --local           connects to local server instead of cloud server

    subcommand:
      {grant,revoke,blacklist,whitelist,delete}
                            you can blacklist/whitelists accounts , grant/revoke
                            admin access

Like ``account`` ,the admin command when used for local server needs the
``-l`` or ``--local`` flag before subcommand

.. code:: bash

    $ ARgorithm admin -l {grant,revoke,blacklist,whitelist,delete}

grant
~~~~~

The grant subcommand is used to grant other programmer accounts admin
access

.. code:: bash

    $ ARgorithm admin grant -h
    usage: ARgorithm admin grant [-h]

    grant programmer admin priveleges

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm admin -l grant
    enter email that you want to grant admin access to : sampleuser@email.com
    ✔ sampleuser@email.com is now an admin

Blacklisted users cannot be granted admin access.

.. code:: bash

    $ ARgorithm admin -l grant
    enter email that you want to grant admin access to : sampleuser@email.com
    ℹ sampleuser@email.com is blacklisted

revoke
~~~~~~

The revoke subcommand is used to take away admin access from programmer
accounts

.. code:: bash

    $ ARgorithm admin revoke -h
    usage: ARgorithm admin revoke [-h]

    revoke programmer admin priveleges

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm admin -l revoke
    enter email that you want to revoke admin access from : sampleuser@email.com
    ⚠ sampleuser@email.com is not an admin

blacklist
~~~~~~~~~

The blacklist command can be used to block programmer accounts from
submitting and testing ARgorithms and user accounts from running
ARgorithms.

.. code:: bash

    $ ARgorithm admin blacklist -h
    usage: ARgorithm admin blacklist [-h]

    blacklist programmer from using application

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm admin -l blacklist
    enter email that you want blacklist : sampleuser@email.com
    ℹ sampleuser@email.com is blacklisted

If an admin account is blacklisted , then the programmer account loses
admin priveleges

whitelist
~~~~~~~~~

The whitelist command can be used to whitelist previously blacklisted
accounts.

.. code:: bash

    $ ARgorithm admin whitelist -h
    usage: ARgorithm admin whitelist [-h]

    whitelist previously blacklisted programmer

    optional arguments:
      -h, --help  show this help message and exit

.. code:: bash

    $ ARgorithm admin -l whitelist
    enter email that you want whitelist : sampleuser@email.com
    ✔ sampleuser@email.com is whitelisted

delete
~~~~~~

The delete subcommand in admin is used to delete accounts.

.. code:: bash

    $ ARgorithm admin delete -h
    usage: ARgorithm admin delete [-h] [-p]

    delete account

    optional arguments:
      -h, --help        show this help message and exit
      -p, --programmer  deletes programmer account. if not given deletes user
                        account

The delete subcommand deletes user accounts by email by default. You can
pass the ``-p`` or ``--programmer`` flag to delete programmer accounts
registered to the email.

.. code:: bash

    $ ARgorithm admin -l delete -p
    enter email that you want delete : sampleuser@email.com
    ✔ sampleuser@email.com is deleted

.. note::

    The delete command and the delete subcommand under admin command are distinctively different from each other. Prefer blacklisting programmer accounts rather than deleting them.