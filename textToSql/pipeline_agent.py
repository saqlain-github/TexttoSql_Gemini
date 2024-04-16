# from dotenv import load_dotev
import os
import sys


from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from textToSql.components.sqlite3_connection import Sqlite3Operations
from textToSql.components.gemini import GeminiLLM 
from textToSql.exception import TexttoSQLException
from textToSql.logging import logger


class QAOverSQLiteConnection:
    """Class is used to create sql agent and answer question by the user"""

    def __init__(self, question:str):
        """class from components are initialized along with
        question from the user

        Args:
            question (str): question by the user regarding the database
        """
        self.question = question
        self.database = Sqlite3Operations("sqlite:///Chinook1.db")
        self.geminiLLM = GeminiLLM()

    def creating_agent(self):
        """this function is used to initialize the the agent

        Raises:
            TexttoSQLException: custom class to log exactly where error occurred
        """
        try:
            logger.info("Creating agent for sqlite database")
            self.agent_exector =  create_sql_agent(self.geminiLLM.model,
                                    toolkit=SQLDatabaseToolkit(db=self.database.db, llm=self.geminiLLM.model),
                                    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                    verbose=True)
            logger.info("Completed Creating agent for sqlite database")
        except Exception as e:
            raise TexttoSQLException(e, sys)

    def initiate_sql_pipeline(self,):
        """this function is starting point of the class 
        all operations are performed in sequence using this function
        
        Only this function is exposed to the front end

        Raises:
            TexttoSQLException: custom class to log exactly where error occurred

        Returns:
            string: return the output from the chain 
        """
        try:
            self.creating_agent()
            logger.info("Starting sqlite pipeline")
            response =  self.agent_exector.invoke(
                {
                    "input": self.question
                }
            )
            logger.info("Completed sql pipeline")
            return response
        except Exception as e:
            raise TexttoSQLException(e, sys)