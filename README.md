# BD2-TPE
**INFORMATION**: All the code snippets are meant to be run from the root of the project.

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
Using `pip`, we install the required dependencies:
```
pip3 install -r requirements.txt
```

## Test Connections
Once both containers are running, run the `connection_test.py` script, this script will try to connect to both databases and inform if the connections are successful or not:
```
python3 ./tests/connection_test_docker.py
```

## Generating Information
To generate the information to be used in the benchmark, the following scripts can be used:
```
python3 ./generators/data_generator.py -u 1000000 -p 100000
```
Where **-u** indicates the amount of users to generate, and **-p** indicates the amount of products to generate.

To generate the information for the carts, we run:
```
python3 ./generators/cart_generator.py -c 1000000 -u 1000000 -p 100000
```
Where **-c** indicates the amount of cart entries to generate, **-u** indicates the amount of users available, and **-p** indicates the amount of products available.

## Preloading Users and Products
To load the information that needs to exist in Postgres (having already generated the CSV files), we start the Postgres docker container:
```
docker start mypostgres
```

We copy the CSV files into the container, along with the *setup.sql* file:
```
docker cp data/products.csv mypostgres:/products.csv
docker cp data/users.csv mypostgres:/users.csv
docker cp setup.sql mypostgres:/setup.sql
```

From the host, we can connect to Postgres in order to execute the SQL file:
```
psql -h localhost -p 5432 -U postgres
```

Once inside the Postgres terminal, we run:
```
\i setup.sql
```

## Running the Project
In order to run the queries and tests, both containers need to be up and running as instructed before.

To run the queries and tests there are several options:
 1. Speed test 1: Inserting 1 million products in the cart using 1 thread
```
python3 ./main.py -q 1
```
 2. Speed test 2: Inserting 1 million products in the cart using 100 threads (10000 from each thread)
```
python3 ./main.py -q 2
```
 3. Speed test 3: Degradation
```
python3 ./main.py -q 3
```
 4. Queries test
```
python3 ./main.py -q 4
```

During the running of the tests, the times will be printed out to the standard output, in seconds.

**NOTE**: The database insertions may take several hours.

## Authors
This is a Final Project for Bases de Datos 2, in the second semester of 2020:
 - Gonzalo Hirsch
 - Agustín Roca
 - Nicolás Britos
 
## Resources
 - [Results](https://docs.google.com/spreadsheets/d/1Yyr_KQhfXO7h96Mle9TbPJxaFhV-GWrd9TCkY8an-Nc/edit?usp=sharing)
 - [Presentation](https://docs.google.com/document/d/1REf2UbTHONCoQsxj5i1AesFYFbdq-3GdqU-RUi9tSj4/edit?usp=sharing)