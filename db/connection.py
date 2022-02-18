import psycopg2
from config import DATABASE_URL


class Connection:
    def __init__(self):
        print(DATABASE_URL)
        conn = psycopg2.connect(DATABASE_URL)
        print(conn)
