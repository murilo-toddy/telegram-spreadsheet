import psycopg2
import config


class Connection:
    """
    Singleton class used to communicate with a PostgreSQL database

    Parameters
    ----------
    debug - bool: Enables debug mode
    """

    # Ensures singleton behaviour
    def __new__(cls, debug=False):
        if not hasattr(cls, "instance"):
            cls.instance = super(Connection, cls).__new__(cls)
        return cls.instance

    def __init__(self, debug=False):
        self.__debug = debug
        self.__connect()

    # Connects to database
    def __connect(self) -> None:
        self.connection = psycopg2.connect(config.DATABASE_URL)
        self.cursor = self.connection.cursor()

        if self.__debug:
            print("\n  [!] Connected to database")
            self.cursor.execute("SELECT version()")
            print(f"  [!!] {self.cursor.fetchone()}")

    # Finishes connection
    def disconnect(self) -> None:
        if self.connection:
            self.connection.close()
            if self.__debug:
                print("\n  [!] Database connection ended")

    def exec(self, command: str, *args, func: callable = None) -> any:
        """
        Execute a SQL query

        Parameters
        ----------
        command - str: SQL command to be executed
        *args - [str]: List of arguments to be passed to query
        func - callable: Function to be called after command is executed
        """
        self.cursor.execute(command, args)
        return func(self.cursor) if func else None

    def commit(self) -> None:
        """Commit changes to database"""
        self.connection.commit()

    def exec_and_commit(self, command: str, *args, func: callable = None) -> any:
        """
        Execute a SQL query and commit changes afterwards

        Parameters
        ----------
        command - str: SQL command to be executed
        *args - [str]: List of arguments to be passed to query
        func - callable: Function to be called after command is executed
        """
        execution_return = self.exec(command, *args, func=func)
        self.commit()
        return execution_return
