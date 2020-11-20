import psycopg2
import redis

def get_postgres_connection():
    return psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1", port="5432")

def get_redis_connection():
    return redis.StrictRedis(host='localhost', port=6379, db=0)