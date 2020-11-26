import psycopg2
import redis


# Class for the Postgres database connection
# noinspection SqlNoDataSourceInspection
class PostgresConnection:
    DEFAULT_CONFIG = {
        'database': 'postgres',
        'host': '127.0.0.1',
        'port': '5432',
        'username': 'postgres',
        'password': 'password'
    }

    # Constructor that generates a database connection and builds the tables, if needed
    def __init__(self, config=None):
        if not config:
            config = PostgresConnection.DEFAULT_CONFIG

        self.con = psycopg2.connect(database=config['database'], user=config['username'], password=config["password"],
                                    host=config['host'], port=config['port'])
        cur = self.con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                full_name TEXT NOT NULL
            );
            
            create sequence IF NOT EXISTS users_id_seq;
            
            alter table users alter column id set default nextval('public.users_id_seq');
            
            alter sequence users_id_seq owned by users.id;
            
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY,
                title text NOT NULL,
                description text NOT NULL,
                price INT NOT NULL
            );
            
            create sequence if not exists products_id_seq;
            
            alter table products alter column id set default nextval('public.products_id_seq');
            
            alter sequence products_id_seq owned by products.id;
            
            CREATE TABLE IF NOT EXISTS carts (
                product_id INT,
                user_id INT,
                quantity INT NOT NULL,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (user_id) REFERENCES users(id),
                PRIMARY KEY (product_id, user_id)
            );
        """)
        self.con.commit()
        cur.close()

    # noinspection SqlResolve
    def insert_user(self, full_name, id=None):
        cur = self.con.cursor()

        if id is None:
            cur.execute("INSERT INTO users (full_name) VALUES (%s);", full_name)
        else:
            cur.execute("INSERT INTO users (id, full_name) VALUES (%s, %s);", (id, full_name))

        self.con.commit()
        cur.close()

    # noinspection SqlResolve
    def insert_product(self, title, description, price, id=None):
        cur = self.con.cursor()

        if id is None:
            cur.execute("INSERT INTO products (title, description, price) VALUES (%s, %s, %s);",
                        (title, description, price))
        else:
            cur.execute("INSERT INTO products (id, title, description, price) VALUES (%s, %s, %s, %s);",
                        (id, title, description, price))

        self.con.commit()
        cur.close()

    # Method to insert data into the carts table
    # noinspection SqlResolve
    def insert_cart(self, user_id, product_id, quantity):
        cur = self.con.cursor()
        cur.execute("INSERT INTO carts (product_id, user_id, quantity) VALUES (%s, %s, %s);",
                    (product_id, user_id, quantity))
        self.con.commit()
        cur.close()

    # Clears the carts table
    def delete_all(self):
        cur = self.con.cursor()
        cur.execute("TRUNCATE carts CASCADE; TRUNCATE products CASCADE; TRUNCATE users CASCADE;")
        self.con.commit()

    # Closes the connection
    def close(self):
        self.con.close()

    # QUERIES
    # noinspection SqlResolve
    def query_1(self):
        cur = self.con.cursor()
        cur.execute("""
            SELECT COUNT(DISTINCT user_id) FROM carts;
        """)
        self.con.commit()
        count = cur.fetchall()[0][0]
        cur.close()
        return count if count is not None else 0

    # noinspection SqlResolve
    def query_2(self, product_id):
        cur = self.con.cursor()
        cur.execute("""
            SELECT SUM(quantity) FROM carts WHERE product_id = %s;
        """, [product_id])
        self.con.commit()
        count = cur.fetchall()[0][0]
        cur.close()
        return count if count is not None else 0

    # noinspection SqlResolve
    def query_3(self, user_id):
        cur = self.con.cursor()
        cur.execute("""
            SELECT COUNT(DISTINCT product_id) FROM carts WHERE user_id = %s;
        """, [user_id])
        self.con.commit()
        count = cur.fetchall()[0][0]
        cur.close()
        return count if count is not None else 0

    # noinspection SqlResolve
    def query_4(self):
        cur = self.con.cursor()
        cur.execute("""
            SELECT COUNT(DISTINCT product_id) FROM carts;
        """)
        self.con.commit()
        count = cur.fetchall()[0][0]
        cur.close()
        return count if count is not None else 0

    # noinspection SqlResolve
    def query_5(self, user_id, product_id):
        cur = self.con.cursor()
        cur.execute("""
            SELECT EXISTS(SELECT 1 FROM carts WHERE user_id = %s AND product_id = %s);
        """, (user_id, product_id))
        self.con.commit()
        exists = cur.fetchall()[0][0]
        cur.close()
        return exists


# Class for the Redis database connection
class RedisConnection:
    DEFAULT_CONFIG = {
        'database': 0,
        'host': 'localhost',
        'port': 6379
    }

    # Constants for the Redis key names
    CLIENT_BASE_KEY = "CLIENT_"
    CLIENTS_KEY = "CLIENTS"
    PRODUCTS_KEY = "PRODUCTS"

    # Constructor that generates a database connection
    def __init__(self, config=None):
        if not config:
            config = RedisConnection.DEFAULT_CONFIG

        self.con = redis.StrictRedis(host=config['host'], port=config['port'], db=config['database'])

    # Method to insert data into the corresponding structures
    def insert_cart(self, user_id, product_id, quantity):
        self.con.hincrby(self.CLIENT_BASE_KEY + str(user_id), product_id, quantity)
        self.con.sadd(self.CLIENTS_KEY, user_id)
        self.con.hincrby(self.PRODUCTS_KEY, product_id, quantity)

    # Deletes all the keys from the database
    def delete_all(self):
        self.con.flushall(False)

    # Closes the connection
    def close(self):
        self.con.close()

    # QUERIES
    def query_1(self):
        return self.con.scard(self.CLIENTS_KEY)

    def query_2(self, product_id):
        val = self.con.hget(self.PRODUCTS_KEY, product_id)
        return int(val) if val is not None else 0

    def query_3(self, user_id):
        val = self.con.hlen(self.CLIENT_BASE_KEY + str(user_id))
        return int(val) if val is not None else 0

    def query_4(self):
        val = self.con.hlen(self.PRODUCTS_KEY)
        return int(val) if val is not None else 0

    def query_5(self, user_id, product_id):
        val = self.con.hexists(self.CLIENT_BASE_KEY + str(user_id), product_id)
        return val
