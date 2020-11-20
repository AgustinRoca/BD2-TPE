# BD2-TPE

## Start Docker Images

### Postgres
Pull the image:
```
docker pull postgres
```

Start the container:
```
docker run --name mypostgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres
```

The username is `postgres`, the password is `password` and the database is `postgres`

Stop the container:
```
docker stop mypostgres
```

Start the container:
```
docker start mypostgres
```

### Redis
Pull the image:
```
docker pull redis
```

Start the container:
```
docker run --name myredis -p 6379:6379 -d redis
```

Stop the container:
```
docker stop myredis
```

Start the container:
```
docker start myredis
```

## Install Modules
Using `pip`, we install:
```
pip3 install psycopg2
pip3 install redis
```

## Test Connections
Once both containers are running, run the `connection_test.py` script, this script will try to connect to both databases