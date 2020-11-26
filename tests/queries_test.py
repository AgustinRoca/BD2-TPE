import unittest
import os
import utils.database_connections as dbc


PG_HOST = 'PG_HOST'
PG_PORT = 'PG_PORT'
PG_USER = 'PG_USER'
PG_PASS = 'PG_PASS'
PG_DB = 'PG_DB'

REDIS_HOST = 'REDIS_HOST'
REDIS_PORT = 'REDIS_PORT'
REDIS_DB = 'REDIS_DB'

CLIENTS_WITH_CARTS = 2


class DatabaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.con = None

    def query_1(self):
        count = self.con.query_1()
        self.assertEqual(count, CLIENTS_WITH_CARTS)

    def query_2(self):
        count = self.con.query_2(1)
        self.assertEqual(count, 2)
        count = self.con.query_2(2)
        self.assertEqual(count, 3)
        count = self.con.query_2(3)
        self.assertEqual(count, 0)


class PostgresQueriesTest(DatabaseTest):
    @classmethod
    def setUpClass(cls):
        cls.con = dbc.PostgresConnection(cls._get_config())

    @classmethod
    def _get_config(cls):
        host = os.getenv(PG_HOST)
        port = os.getenv(PG_PORT)
        user = os.getenv(PG_USER)
        pw = os.getenv(PG_PASS)
        db = os.getenv(PG_DB)

        config = dbc.PostgresConnection.DEFAULT_CONFIG.copy()

        if host is not None:
            config['host'] = host
        if port is not None:
            config['port'] = str(port)
        if user is not None:
            config['username'] = user
        if pw is not None:
            config['password'] = pw
        if db is not None:
            config['database'] = db

        return config

    def setUp(self) -> None:
        self.con.delete_all()

        self.con.insert_user("Prueba1", 1)
        self.con.insert_user("Prueba2", 2)
        self.con.insert_user("Prueba3", 3)

        self.con.insert_product("Producto1", "", 1000000, 1)
        self.con.insert_product("Producto2", "", 1000000, 2)
        self.con.insert_product("Producto3", "", 1000000, 3)

        self.con.insert_cart(1, 1, 2)
        self.con.insert_cart(1, 2, 2)
        self.con.insert_cart(2, 2, 1)

    def test_query_1(self):
        self.query_1()

    def test_query_2(self):
        self.query_2()


class RedisQueriesTest(DatabaseTest):
    @classmethod
    def setUpClass(cls):
        cls.con = dbc.RedisConnection(cls._get_config())

    @classmethod
    def _get_config(cls):
        host = os.getenv(REDIS_HOST)
        port = os.getenv(REDIS_PORT)
        db = os.getenv(REDIS_DB)

        config = dbc.RedisConnection.DEFAULT_CONFIG.copy()

        if host is not None:
            config['host'] = host
        if port is not None:
            config['port'] = int(port)
        if db is not None:
            config['database'] = int(db)

        return config

    def setUp(self) -> None:
        self.con.delete_all()

        self.con.insert_cart(1, 1, 2)
        self.con.insert_cart(1, 2, 2)
        self.con.insert_cart(2, 2, 1)

    def test_query_1(self):
        self.query_1()

    def test_query_2(self):
        self.query_2()
