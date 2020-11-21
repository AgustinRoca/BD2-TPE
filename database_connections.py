import psycopg2
import redis


# Class for the Postgres database connection
class PostgresConnection:
    # Constructor that generates a database connection and builds the tables, if needed
    def __init__(self):
        self.con = psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1",
                                    port="5432")
        cur = self.con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT PRIMARY KEY,
                full_name VARCHAR(255)
            );
            
            CREATE TABLE IF NOT EXISTS products (
                id INT PRIMARY KEY,
                description VARCHAR(511)
            );
            
            CREATE TABLE IF NOT EXISTS carts (
                product_id INT,
                user_id INT,
                quantity INT NOT NULL,
                UNIQUE(user_id, product_id),
                FOREIGN KEY (product_id) REFERENCES products(id),
                FOREIGN KEY (user_id) REFERENCES users(id)
            );
        """)
        self.con.commit()

    # Method to insert data into the carts table
    def insert_data(self, user_id, product_id, quantity):
        cur = self.con.cursor()
        cur.execute("INSERT INTO carts (product_id, user_id, quantity) VALUES (%s, %s, %s);",
                    (product_id, user_id, quantity))
        self.con.commit()

    # Clears the carts table
    def delete_all(self):
        cur = self.con.cursor()
        cur.execute("DELETE FROM carts;")
        self.con.commit()

# Class for the Redis database connection
class RedisConnection:
    # Constants for the Redis key names
    CLIENT_BASE_KEY = "CLIENT_"
    CLIENTS_KEY = "CLIENTS"
    PRODUCTS_KEY = "PRODUCTS"

    # Constructor that generates a database connection
    def __init__(self):
        self.con = redis.StrictRedis(host='localhost', port=6379, db=0)

    # Method to insert data into the corresponding structures
    def insert_data(self, user_id, product_id, quantity):
        self.con.hincrby(self.CLIENT_BASE_KEY + str(user_id), product_id, quantity)
        self.con.sadd(self.CLIENTS_KEY, user_id)
        self.con.hincrby(self.PRODUCTS_KEY, product_id, quantity)

    # Deletes all the keys from the database
    def delete_all(self):
        self.con.flushall(False)