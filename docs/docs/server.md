# Setting up your own server

ARgorithm has a common server endpoint where the community can create
and contribute their own ARgorithms. This is by default the endpoint for
the Toolkit command line. But in case , a programmer wants to setup a
local server for testing purposes or wants to setup a specific server
for their class or organisation. The following steps are to be followed.

## System Requirements

The server is built using FastAPI. The requirements for running the application is given below

- Python 3.6+
  - jinja2
  - aiofiles
  - python-multipart
  - databases[sqlite]
  - python-jose
  - passlib[bcrypt]
  - motor
  - ARgorithmToolkit
  - PyJWT

To run it in production, use gunicorn to run as a production server. Docker-ce will be required if server image is being used

## Installation

You can clone the git repository and install requirements from the `requirements.txt` file.

<div class="termy">
```console
$ git clone https://github.com/ARgorithm/Server.git
Cloning into 'Server'
---> 100%
$ cd Server/app
$ pip install -r requirements.txt
---> 100%
Successfully installed packages
```
</div>

or you can pull the image

<div class="termy">
```console
$ docker pull alanjohn/argorithm-server
Using default tag: latest
latest: Pulling from alanjohn/argorithm-server
---> 100%
Status: Downloaded new image alanjohn/argorithm-server
```
</div>
## Configuring the Server

The application can be run in different modes

1. In-app database

   No authentication or authorization services. Data stored using sqlite database. By default, it runs in this mode

2. mongodb database

   No authentication or authorization services. Data stored in mongodb database of your choice. For this you will need to set some environment variables:

   - `DATABASE=mongodb`
   - `DB_USERNAME=yourdbusername`
   - `DB_PASSWORD=yourdbpassword`
   - `DB_ENDPOINT=yourdbendpoint`
   - `DB_PORT=27017`

3. mongodb with auth

   Authorization on all basic routes. Data stored in mongodb database of your choice. This is an enhancement to the previous mode so along with the required envs previously.

   - `SECRET_KEY=yoursecretkey`
   - `ADMIN_EMAIL=sample@email.com`
   - `ADMIN_PASSWORD=test123`

Check the `Dockerfile` for the default values of these environment variables.
The repo comes with two docker compose configuration files

- `docker-compose.local.yml` : runs application in default mode
    ```yaml
    version: "3"
    services:
        arserver:
            image: alanjohn/argorithm-server:latest
            ports: 
                - 80:80
            volumes:
                - local-uploads:/app/app/uploads
    volumes:
        local-uploads:
            driver: local
    
    ```
    
- `docker-compose.prod.yml` : runs application with mongodb and auth and will setup mongodb database as well. will read env variables from `.env` file

    ```yaml
    version: "3"
    services:
        mongodb:
            image: mongo
            ports: 
                - 27017:27017
            environment:
                - MONGO_INITDB_ROOT_USERNAME=${DB_USERNAME}
                - MONGO_INITDB_ROOT_PASSWORD=${DB_PASSWORD}
            volumes:
                - mongo-data:/data/db
        arserver:
            image: alanjohn/argorithm-server:latest
            ports: 
                - 80:80
            environment:
                - DATABASE=MONGO
                - AUTH=ENABLED
                - SECRET_KEY=${SECRET_KEY}
                - DB_USERNAME=${DB_USERNAME}
                - DB_PASSWORD=${DB_PASSWORD}
                - DB_ENDPOINT=mongodb
                - DB_PORT=27017
                - ADMIN_EMAIL=${ADMIN_EMAIL}
                - ADMIN_PASSWORD=${PASSWORD}
            volumes:
                - uploads:/app/app/uploads
            depends_on:
                - mongoexp
    volumes:
        mongo-data:
            driver: local
        uploads:
            driver: local
    ```

The environment variables in above compose files are read from `.env` file.You can create strong secret keys using
<div class="termy">
```console
$ openssl rand -hex 32
09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
```
</div>

## Running the server

Running the application using uvicorn

<div class="termy">
```console
$ uvicorn main:app --reload

INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28720]
INFO:     Started server process [28722]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```
</div>

Running the application as a docker container

<div class="termy">
```console
$ docker run --name -d server -p 80:80 --env-file=.env alanjohn/argorithm-server:latest
server
```
</div>

Running the application using `docker-compose`

<div class="termy">
```console
$ docker-compose -f docker-compose.prod.yml up
Creating network "server_default" with the default driver
Creating server_mongodb_1 ... done
Creating server_arserver_1 ... done
Attaching to server_mongodb_1,server_arserver_1
```
</div>