import threading
from utils import database_connections as dbc


class InsertionThread(threading.Thread):
    def __init__(self, carts, db):
        threading.Thread.__init__(self)
        self.carts = carts
        self.db = db

    def run(self):
        for cart in self.carts:
            self.db.insert_cart(cart[0], cart[1], cart[2])
