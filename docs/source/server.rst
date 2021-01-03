Setting up your own Server
==========================

ARgorithm has a common server endpoint where the community can create
and contribute their own ARgorithms. This is by default the endpoint for
the Toolkit command line. But in case , a programmer wants to setup a
local server for testing purposes or wants to setup a specific server
for their class or organisation. The following steps are to be followed.

1. **System requirements**

The server can be run using docker so the only system requirements in
this case is ``docker-ce``. You can also clone the repo and run server
without docker in which case , the system requirements are mentioned
below :-

-  Python 3.6+

   -  Flask
   -  ARgorithmToolkit
   -  pymongo

-  You will also need uwsgi, nginx and similar software if you want to
   run a production grade server.

    It is recommended to use the docker image for convenience

2. **Installing the server files**

For the docker image

.. code:: bash    

    $ docker pull alanjohn/argorithm-server

or you could clone the repository and build the image

.. code:: bash

    $ git clone https://github.com/ARgorithm/Server.git
    $ cd Server
    $ docker build . -t argorithm-server

3. **Running the server instance**

before running the image , it is advisable to get familiar with the
environment variables used to configure the docker image.

+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| environment variable   | default value      | description                                                                                                                                                                                |
+========================+====================+============================================================================================================================================================================================+
| SECRET\_KEY            | clawtime           | Secret key used to encode JWT tokens used in authentication.                                                                                                                               |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| AUTH                   | DISABLED           | Flag to enable Auth feature. by default is disabled but when running server image for non local use , it is highly recommended that you set it to ENABLED. Needs DATABASE to be ENABLED.   |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| MAIL                   | DISABLED           | Flag to enable mail verification feature by default is not enabled. Not yet supported completely. Keep it DISABLED                                                                         |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DATABASE               | DISABLED           | Flag to set database storage. Right now mongodb is supported so to enable that set it to MONGO                                                                                             |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DB\_ENDPOINT           | mongodb            | Database endpoint                                                                                                                                                                          |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DB\_PORT               | 27017              | Database port                                                                                                                                                                              |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DB\_USERNAME           | root               | Database authentication username                                                                                                                                                           |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| DB\_PASSWORD           | example            | Database authentication password                                                                                                                                                           |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ADMIN\_EMAIL           | sample@email.com   | If Auth is enabled , use this to set your pre-existing admin account email                                                                                                                 |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| ADMIN\_PASSWORD        | test123            | If Auth is enabled , use this to set your pre-existing admin account password                                                                                                              |
+------------------------+--------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

when running a local server instance for testing purposes , you do not
need advanced features hence you can ignore these env variables.
Otherwise , It is critically important to understand theses env
variables.

You can store them in an ``.env`` file.

.. code::bash 

    AUTH=DISABLED
    DATABASE=MONGO
    DB_ENDPOINT=https://mongodb-database-endpoint.com
    DB_PORT=27017
    DB_USERNAME=dbadmin
    DB_PASSWORD=dbpassword
    ADMIN_EMAIL=admin@email.com
    ADMIN_PASSWORD=Ks239dh2ehc8
    SECRET_KEY=8e68ce28-bb88-43dd-820b-82be38b699db``

To run server image with default env

.. code::bash

    $ docker run --name server -p 80:80 alanjohn/argorithm-server``

To run with env variables

.. code:: bash

    $ docker run --name server -p 80:80 --rm --env-file=.env alanjohn/argorithm-server``

You can also use docker-compose for further convenience in setting up.
Check out `the repo <https://github.com/ARgorithm/Server>`__ on how to
see docker-compose and kubernetes configurations.

4. **Connecting to server instance from command line**

If server is running locally you can use the ``-l`` or ``--local`` flag
wherever required. You can check the `cli deep dive <cli.html>`_

If server is running on cloud

.. code:: bash

    $ ARgorithm configure    
    Enter server endpoint or press ENTER to connect to ARgorithm common server : https://customendpoint.com    
    ✔ Cloud requests will now go to https://customendpoint.com

5. **Connecting mobile application to server**

The mobile application has a prompt that allows users to connect to different endpoints.
