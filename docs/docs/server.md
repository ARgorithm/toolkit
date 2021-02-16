# Setting up your own server

ARgorithm has a common server endpoint where the community can create
and contribute their own ARgorithms. This is by default the endpoint for
the toolkit command line. But in case , a programmer wants to setup a
local server for testing purposes or wants to setup a specific server
for their class or organisation. The following steps are to be followed.

## System Requirements

The server is built using FastAPI. The requirements for running the application is given below

- Python 3.6+
  - fastapi
  - uvicorn[standard]
  - gunicorn
  - jinja2
  - aiofiles
  - python-multipart
  - databases[sqlite]
  - python-jose
  - passlib[bcrypt]
  - motor
  - tornado
  - dnspython
  - pytest
  - ARgorithmToolkit
  - PyJWT
  - aioredis
  - prometheus-client

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

#### In-app database

No authentication or authorization services. Data stored using sqlite database. By default, it runs in this mode

#### mongodb database

No authentication or authorization services. Data stored in mongodb database of your choice. For this you will need to set some environment variables:

   - `DATABASE=mongodb`
   - `DB_USERNAME=yourdbusername`
   - `DB_PASSWORD=yourdbpassword`
   - `DB_ENDPOINT=yourdbendpoint`
   - `DB_PORT=27017`

!!! info
    If using a cloud mongo database like atlas which provides mongo+srv url as endpoint, you just need to paste that URL as your `DB_ENDPOINT`. You can ignore the `DB_USERNAME` and `DB_PASSWORD` env variables.

#### mongodb with auth

Authorization on all basic routes. Data stored in mongodb database of your choice. This is an enhancement to the previous mode so along with the required envs previously.

   - `SECRET_KEY=yoursecretkey`
   - `ADMIN_EMAIL=sample@email.com`
   - `ADMIN_PASSWORD=test123`

#### caching

Caching on state generation when execution request comes on `/argorithms/run`. Uses [redis](https://redis.io) for implementing LRU cache. The following environment variables have to be set

   - `CACHING=ENABLED`
   - `REDIS_HOST=redis`
   - `REDIS_PORT=6379`
   - `REDIS_PASSWORD=notmypassword`

#### monitoring

By default, [prometheus](https://prometheus.io) metrics have been implemented and can be accessed at `/metrics` route. Programmer can secure the route by using the `METRICS_TOKEN` environment variable to add authorization bearer token. If not given then by default, there is no authorization required

   - `METRICS_TOKEN=yourmetricstoken`

You can check out the grafana folder in the code repository for a ARgorithm specific dashboard

### Docker-compose examples

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
                - local-uploads:/tmp/argorithm
    volumes:
        local-uploads:
            driver: local

    ```
    
- `docker-compose.prod.yml` : runs application with mongodb and auth and will setup mongodb database. A redis server is launched to handle caching and prometheus and grafana nodes are created for monitoring It will read environment variables from `.env` file

    ```yaml
    # Sets up multiple services to demonstrate how a server cluster would run with cloud storage, authorization, caching and monitoring
    # This file requires the existense of .env with neccessary variable
    # The docker-compose file is added for emulation of how the application can be setup with full functionality
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
        redis:
            image: redis
            ports:
                - 6379:6379
            volumes:
                - ./redis.conf:/usr/local/etc/redis/redis.conf
            command: redis-server /usr/local/etc/redis/redis.conf
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
	            - ADMIN_PASSWORD=${ADMIN_PASSWORD}
	            - CACHING=ENABLED
	            - REDIS_HOST=redis
	            - REDIS_PORT=6379
	            - REDIS_PASSWORD=notmypassword
	        volumes:
	            - uploads:/tmp/argorithm
	        depends_on:
	            - mongodb
	            - redis
	    prometheus:
	        image: prom/prometheus
	        ports:
	        - 9090:9090
	        command:
	        - --config.file=/etc/prometheus/prometheus.yml
	        volumes:
	        - ./prometheus.yml:/etc/prometheus/prometheus.yml:ro
	        depends_on:
	        - arserver
	    grafana:
	        image: grafana/grafana
	        ports:
	        - 3000:3000
	        volumes:
	        - ./grafana/datasource.yml:/etc/grafana/provisioning/datasource.yml
	        env_file:
	        - ./grafana/config.monitoring
	        depends_on:
	        - prometheus
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

## Interacting with server

1. Once the server is running, you can check whether its running by entering the public IP on the browswer. You should get the server running page. you can check the api routes on `/docs` page with help of FastAPI Swagger UI. You can get the api routes in json format at the `/openapi.json`.

    ![](https://user-images.githubusercontent.com/35735486/104831190-97d6fb80-58ac-11eb-92d3-bd7a6d823cfe.png)

2. There are two type of accounts in the server:

    - `Programmer`
    - `User`

3. The programmer account allows you to create and manage argorithms. The user account allows you to run argorithms and get states. When using the CLI [account new](/toolkit/cli#new) command, it create both a progammer and a user account for that email. The mobile application can only create user accounts.

4. logs are generated in server.log file which you will find in `/tmp/argorithm`. The `server.log` file contains request based logs for every path.

5. Application metrics are available at `/metrics`