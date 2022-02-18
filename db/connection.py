import psycopg2
from config import DATABASE_URL


class Connection:
    def __init__(self):
        conn = psycopg2.connect(DATABASE_URL)
