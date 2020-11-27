import sys
import threading
from utils import database_connections as dbc
from utils import insertion_thread as it
import utils.args as args_utils
import time

FILENAME = "./data/carts.csv"
QUERY_DATA_SAMPLES_COUNT = 10
TIMES_DATA_SAMPLES_COUNT = 4
THREAD_COUNT = 100
TYPE_REDIS = "REDIS"
TYPE_POSTGRES = "POSTGRES"
TYPES = [TYPE_REDIS, TYPE_POSTGRES]

# Function to read the carts data from the files
def read_carts(filename):
    f = open(filename, 'r')

    # Extract data
    data = []
    for line in f:
        d = line.rstrip("\n").split(";")
        # User; Product; Amount
        data.append((int(d[0]), int(d[1]), int(d[2])))
    return data


def insert_in_db(carts, db):
    start = time.time()
    for cart in carts:
        db.insert_cart(cart[0], cart[1], cart[2])
    end = time.time()
    return end - start


def run_mono_stress_insertions(carts):
    r = dbc.RedisConnection()
    p = dbc.PostgresConnection()

    for i in range(TIMES_DATA_SAMPLES_COUNT):
        r.delete_all()
        p.delete_carts()
        t = insert_in_db(carts, r)
        print("REDIS TIME =", t)
        t = insert_in_db(carts, p)
        print("POSTGRES TIME =", t)


def break_up_cart_items(carts, chunk_size):
    return [carts[i:i + chunk_size] for i in range(0, len(carts), chunk_size)]


def generate_clients(amount):
    p = []
    r = []
    for i in range(amount):
        p.append(dbc.PostgresConnection())
        r.append(dbc.RedisConnection())
    m = {TYPE_REDIS: r, TYPE_POSTGRES: p}
    return m


def run_multiple_stress_insertions(carts):
    chunks = break_up_cart_items(carts, int(len(carts) / THREAD_COUNT))
    clients = generate_clients(THREAD_COUNT)

    threads = []

    for i in range(TIMES_DATA_SAMPLES_COUNT):
        clients[TYPE_REDIS][0].delete_all()
        clients[TYPE_POSTGRES][0].delete_carts()
        for ty in TYPES:
            start = time.time()
            for w in range(THREAD_COUNT):
                t = it.InsertionThread(chunks[w], clients[ty][w])
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            end = time.time()
            print(ty, "TIME =", end - start)


def insert_synchronic_data(carts):
    r = dbc.RedisConnection()
    p = dbc.PostgresConnection()

    r.delete_all()
    p.delete_carts()

    # Redis
    print("Inserting in REDIS")
    insert_in_db(carts, r)

    # Postgres
    print("Inserting in POSTGRES")
    insert_in_db(carts, p)


def init_query_map():
    m = {1: [], 2: [], 3: [], 4: [], 5: []}
    return m


def run_query_1(db):
    start = time.time()
    db.query_1()
    end = time.time()
    return end - start


def run_query_2(db):
    start = time.time()
    db.query_2(12345)
    end = time.time()
    return end - start


def run_query_3(db):
    start = time.time()
    db.query_3(12345)
    end = time.time()
    return end - start


def run_query_4(db):
    start = time.time()
    db.query_4()
    end = time.time()
    return end - start


def run_query_5(db):
    start = time.time()
    db.query_5(12345, 12345)
    end = time.time()
    return end - start


def run_queries():
    r = dbc.RedisConnection()
    p = dbc.PostgresConnection()

    # Time
    r_times = init_query_map()
    p_times = init_query_map()

    for i in range(QUERY_DATA_SAMPLES_COUNT):
        # QUERY 1
        r_times[1].append(run_query_1(r))
        p_times[1].append(run_query_1(p))
        # QUERY 2
        r_times[2].append(run_query_2(r))
        p_times[2].append(run_query_2(p))
        # QUERY 3
        r_times[3].append(run_query_3(r))
        p_times[3].append(run_query_3(p))
        # QUERY 4
        r_times[4].append(run_query_4(r))
        p_times[4].append(run_query_4(p))
        # QUERY 5
        r_times[5].append(run_query_5(r))
        p_times[5].append(run_query_5(p))

    print("REDIS TIMES")
    print(r_times)
    print("POSTGRES TIMES")
    print(p_times)


# main() function
def main():
    args = args_utils.parse_args(sys.argv[1:])
    postgres_config = args_utils.get_postgres_config(args)
    redis_config = args_utils.get_redis_config(args)

    # Tests
    carts = read_carts(FILENAME)

    if args.query == 1:
        print("Running STRESS EN 1 THREAD")
        run_mono_stress_insertions(carts)
    elif args.query == 2:
        print("Running STRESS EN 100 THREADS")
        run_multiple_stress_insertions(carts)
    elif args.query > 3:
        print("Inserting data")
        insert_synchronic_data(carts)
        print("Running ALL DATA QUERIES")
        run_queries()


# call main
if __name__ == '__main__':
    main()
