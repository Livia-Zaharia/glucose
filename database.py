""" 
A module for the persistence layer
"""

import datetime
import sqlite3
import typing as t
import pandas as pd
from pathlib import Path

CURRENT_PATH_CWD = Path.cwd()
IMAGES_PATH = CURRENT_PATH_CWD / "images_and_graphs"


class DatabaseManager:
    """ 
    A class specialized for the persistence layer using SQLite 
    """
    
    def __init__(self, database_filename: str):
        """
        Initializes the connection with the SQLite database 
        """
        
        self.connection = sqlite3.connect(database_filename,check_same_thread=False)
        self.key_conversion_needed=[]

    def __del__(self):
        """ Closes the connection when the database manager is no longer used """
        
        self.connection.close()

    def _execute(self, statement: str, values: t.Optional[t.Tuple[str]] = None) -> sqlite3.Cursor:
        """
        Takes in a SQL statement and optionally the values for placeholders
        and executes it with SQLite

        Args:
            statement:the command written in sql str format
            values: what to replace the placeholders with, tuples of str
        
        Returns:
            a cursor, sqlite3 cursor
        """
        try:
            with self.connection:
                
                cursor = self.connection.cursor()
                cursor.execute(statement, values or [])
                return cursor
        except (sqlite3.IntegrityError, sqlite3.OperationalError):
            print(
                f"Something went wrong with the following transaction:\n{statement}"
            )
            raise
    
    def _type_for_columns(self,columns_specs:dict)->dict:
        """
        Module that receives a dict of column names and sample of column data in python and returns a dict with the ID key inserted
        plus the same keys as before which have been converted to SQL data types

        Args:
            columns_specs: dict with key as column names and values as sample of column data
        
        Returns:
            new_columns:a dict with the same key as in input but the values contain the converted type of the value in sql equivalent
        """
        new_columns={}
        new_columns.setdefault("ID",'INTEGER PRIMARY KEY AUTOINCREMENT')
        for key, value in list(columns_specs.items()):
            current_type=type(value)
            if current_type == str or current_type == chr or current_type == datetime or current_type== datetime.timedelta:
                new_type="TEXT"
                self.key_conversion_needed.append(key)
            elif current_type == int:
                new_type="INTEGER"
            elif current_type == float:
                new_type="REAL"
            else:
                new_type = "BLOB"
                self.key_conversion_needed.append(key)
            new_columns.setdefault(key,new_type)
        
        return new_columns

    def create_table_if_not_exists(self, table_name: str, columns: t.Dict[str, str]) -> None:
        """
        Takes in a table name and the columns with names as keys and types as values and then creates
        the CREATE TABLE statement to be executed with SQLite

        Args:
            table_name: string with name of the table
            columns: dict with column names as keys and the data type in sql format for values
        """
        columns=self._type_for_columns(columns)
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

    def add(self, table_name: str, data: t.Dict[str, str]) -> int:
        """
        Takes in a table name to INSERT data INTO and a data dictionary with columns
        as keys and values as values.
        It returns the last used id
        And it works row by row

        Args:
            table_name: str -the name of the table where to add
            data:dict, the data to be added organized with keys as column names and values as actual data to be added
        
        Returns:
            last row added id
        """
        keys = data.keys()

        for elem in set(self.key_conversion_needed):
            if elem not in keys:
                # print(f"key: {elem} not in data.keys()={keys}, skipping...")
                continue

            data[elem] = str(data[elem])

        column_names = ", ".join(keys)
        placeholders = ", ".join(["?"] * len(keys))
        column_values = tuple(data.values())

        statement = f"""
            INSERT INTO
                {table_name} (
                    {column_names}
                ) VALUES (
                    {placeholders}
                );
        """

        result = self._execute(statement, column_values)
        #because the lastrow id will literally return the last- that means not 0 if it is first, but 1
        return (result.lastrowid-1)

    def delete(self, table_name: str, criteria: t.Dict[str, str]) -> None:
        """
        Takes in a table name and a criteria to DELETE FROM
        """

        placeholders = [f"{column} = ?" for column in criteria.keys()]
        delete_criteria = " AND ".join(placeholders)
        delete_criteria_values = tuple(criteria.values())

        statement = f"""
            DELETE FROM 
                {table_name}
            WHERE
                {delete_criteria};
        """

        self._execute(statement, delete_criteria_values)

    def _select_statement(
        self, 
        table_name: str, 
        criteria: t.Dict[str, str] = {}, 
        order_by: t.Optional[str] = None,
        ordered_descending: bool = False,
        ) -> str:
        """
        Takes in a table name and optionally a criteria as a dictionary, a column to order by
        and a boolean flag to order it by that column descending or not
        returns the select statement construction

        Args:
            table_name:str, the table name
            criteria: dict where keys are column name, value are values that meet the criteria of equality
            order_by: optional value to sort by
            ordered_descending:optional value to change the way it is sorted

        Returns:
            statement: the string that is searches for
        """
        
        select_criteria_values = tuple(criteria.values())

        statement = f"SELECT * FROM {table_name}"
        if criteria:
            placeholders = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = " AND ".join(placeholders)
            statement = statement + f" WHERE {select_criteria}"
        
        if order_by:
            statement = statement + f" ORDER BY {order_by}"
            if ordered_descending:
                statement = statement + " DESC"

        statement = statement + ";"
        
        # self._execute(statement,select_criteria_values)
        
        return statement
    
    def _write_to_xls_file(self, df:pd.DataFrame, name: str):
        """
        Method for writing to xls directly from the DB manager.
        It passes through a pandas Dataframe and it is written
        Called by select_and_write_to_xls_file

        Args:
            df: a dataframe whill a values take with a fetchall in previous calls
            name: str a name of the xls
        """

        with pd.ExcelWriter(name, engine="openpyxl") as writer:
            df.to_excel(writer, header=True, engine="openpyxl", index=True)
    
    def select_and_write_to_xls_file(
        self,
        name:str, 
        table_name: str, 
        criteria: t.Dict[str, str] = {}, 
        order_by: t.Optional[str] = None,
        ordered_descending: bool = False,
        ):
        """
        Method that recieves the imput for a querry in a DB, then generates the xls at given location

        Args:
            table_name:str, the table name
            criteria: dict where keys are column name, value are values that meet the criteria of equality
            order_by: optional value to sort by
            ordered_descending:optional value to change the way it is sorted

        Returns:
            None- just creates the dataframe and the output is the xls file
        """

        select_criteria_values = tuple(criteria.values())
    

        for item in select_criteria_values:
            new_statement=self._select_statement(table_name,criteria, order_by, ordered_descending).replace("?",str(item),1)
    
        df=pd.read_sql_query(new_statement, self.connection)
        self._write_to_xls_file(df, name)
    
    def add_multiple_rows(self, table_name: str, data: t.Dict[str, t.List], tuple_data:t.List[t.Tuple]) -> None:
        """
        Takes in a table name to INSERT data INTO and a data dictionary with columns
        as keys and values as multiple rows and column values.
        It returns the last used id

        Args:
        
        """
        keys = data.keys()
        
        for elem in set(self.key_conversion_needed):
            if elem not in keys:
                # print(f"key: {elem} not in data.keys()={keys}, skipping...")
                continue

            data[elem] = str(data[elem])

        column_names = ", ".join(keys)
        placeholders=", ".join(["?"] * len(keys))
        placeholders = f"({placeholders})"
        placeholders=", ".join([f"{placeholders}"]*len(list(data.values())[0]))
        column_values = tuple(tuple_data)

        statement = f"""
            INSERT INTO
                {table_name} (
                    {column_names}
                ) VALUES 
                    {placeholders}
                ;
        """

        self._execute(statement, column_values)
    