""" A module for the persistence layer """

import sqlite3


class DatabaseManager:
    """ A class specialized for the persistence layer using SQLite """
    
    def __init__(self, database_filename: str):
        """ Initializes the connection with the SQLite database """
        
        self.connection = sqlite3.connect(database_filename)

    def __del__(self):
        """ Closes the connection when the database manager is no longer used """
        
        self.connection.close()

    def _execute(self, statement: str) -> sqlite3.Cursor:
        """ Takes in a SQL statement and executes with SQLite """
        
        cursor = self.connection.cursor()
        cursor.execute(statement)
        return cursor

    def create_table(self, table_name: str, columns: dict) -> None:
        """
        Takes in a table name and the columns with names as keys and types as values and creates
        the CREATE TABLE statement to be executed with SQLite
        """
        columns_with_types = []

        for column_name, data_type in columns.items():
            current_column = f"{column_name} {data_type.upper()}"
            columns_with_types.append(current_column)

        columns_in_statement = ", ".join(columns_with_types)

        statement = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                {columns_in_statement}
            );
        """
        
        self._execute(statement)

    def drop_table(self, table_name: str) -> None:
        """
        Takes in a table name to delete using the DROP TABLE statement to be executed with SQLite
        """
        
        statement = f"DROP TABLE {table_name};"
        self._execute(statement)