import psycopg2
from config import DATABASE_URL


class Connection:
    def __init__(self):
        print(DATABASE_URL)
