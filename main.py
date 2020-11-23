import sys

from utils import database_connections as dbc
from generators.postgres_generator import populate_database
import utils.args as args_utils

FILENAME = "./data/carts.csv"


# Function to read the carts data from the files
def read_carts(filename):
    f = open(filename, 'r')

    # Extract data
    data = []
    for line in f:
        d = line.rstrip("\n").split(";")
        data.append((int(d[0]), int(d[1]), int(d[2])))
    return data


# main() function
def main():
    args = args_utils.parse_args(sys.argv[1:])
    postgres_config = args_utils.get_postgres_config(args)
    redis_config = args_utils.get_redis_config(args)

    # Convert the query param into an integer
    # query_type = int(args.query)

    p = dbc.PostgresConnection(config=postgres_config)
    if args.generate is not None:
        populate_database(p.con)


    # Tests
    # d = read_carts(FILENAME)
    # print(len(d))
    # r = dbc.RedisConnection()
    # p = dbc.PostgresConnection()
    # r.insert_data(1, 2, 3)
    # p.insert_data(1, 2, 3)


# call main
if __name__ == '__main__':
    main()
