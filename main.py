import argparse
import database_connections as dbc

FILENAME = "./data/carts.csv"


# Function to read the carts data from the files
def read_carts(filename):
    f = open(filename, 'r')

    # Extract data
    data = []
    for line in f:
        d = line.rstrip("\n").split(";")
        data.append([int(d[0]), int(d[1]), int(d[2])])
    return data


# main() function
def main():
    # Command line args are in sys.argv[1], sys.argv[2] ..
    # sys.argv[0] is the script name itself and can be ignored
    # parse arguments
    parser = argparse.ArgumentParser(description="Main program for BD2 TPE")

    # add arguments
    parser.add_argument('-q', dest='query', required=True)
    args = parser.parse_args()

    # Convert the query param into an integer
    query_type = int(args.query)

    # Tests
    r = dbc.RedisConnection()
    p = dbc.PostgresConnection()
    r.insert_data(1, 2, 3)
    p.insert_data(1, 2, 3)


# call main
if __name__ == '__main__':
    main()
