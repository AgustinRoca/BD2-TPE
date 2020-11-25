import psycopg2
import redis

# Postgres
print("Trying to open Postgres connection")
con = psycopg2.connect(database="postgres", user="postgres", password="password", host="127.0.0.1", port="5432")
print("Postgres connected successfully")

# Redis
print("Trying to open Redis connection")
r = redis.StrictRedis(host='localhost', port=6379, db=0)
r.set('foo', 'Redis connected successfully')
print(r.get('foo').decode())
r.delete("foo")
