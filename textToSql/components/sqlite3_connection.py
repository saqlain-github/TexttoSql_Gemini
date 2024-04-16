# module contains methods necessary for sqlite3 operations
from textToSql.exception import TexttoSQLException
from textToSql.logging import logger

from langchain_community.utilities import SQLDatabase

class Sqlite3Operations:
    """class encapsulating the methods needed for sqlite3 operations
    """
    def __init__(self, connections_url:str):
        self.connections_url = connections_url
        self.db = SQLDatabase.from_uri(self.connections_url)
    
    def establish_connection(self):
        """function to establish a connection

        Returns:
            sqlit3 object: database object after establish_connection
        """
        return self.db
    
    def execute_query(self, query):
        """function to execute a query

        Args:
            query (string): query that needs to be executed

        Returns:
            string : returns output of the query executed
        """
        return self.db.run(query)
    
    def get_dialect(self):
        # returns the dialect of the database
        return self.db.dialect
    
    def get_tables_names(self):
        # returns tables and number of records in the database
        return self.db.get_usable_table_names()