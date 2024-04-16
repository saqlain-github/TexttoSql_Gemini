# from dotenv import load_dotev
import os
import sys

from langchain.chains import create_sql_query_chain
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

from textToSql.components.sqlite3_connection import Sqlite3Operations
from textToSql.components.gemini import GeminiLLM 
from textToSql.exception import TexttoSQLException
from textToSql.logging import logger

# Load environment variables from .env
# load_dotenv()

# openai_api_key = os.getenv("OPENAI_API_KEY")
template = """Given an input question, first create a syntactically correct {dialect} query to run, then look at the results of the query and return the {top_k} answer.
Use the following format:

Question: "Question here"
"SQL Query to run"
SQLResult: "Result of the SQLQuery"
Answer: "Final answer here"

Only use the following tables:

{table_info}.

Question: {input}"""

answer_template = """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

Question: {question}
{query}
SQL Result: {result}
Answer:
"""

class QAOverSQLiteConnection:
    def __init__(self, question:str):
        self.question = question
        self.database = Sqlite3Operations("sqlite:///Chinook1.db")
        self.geminiLLM = GeminiLLM()
        self.answer_prompt = PromptTemplate.from_template(answer_template)
        self.prompt = PromptTemplate.from_template(template)

    def get_query(self):
        return create_sql_query_chain(self.geminiLLM.model, self.database.db, self.prompt)
    
    def get_answer(self):
        return self.answer_prompt | self.geminiLLM.model | StrOutputParser()
    
    def executing_query(self):
        return QuerySQLDataBaseTool(db=self.database.db)
    
    def create_chain(self):
        return (
            RunnablePassthrough.assign(query=self.get_query()).assign(
                result=itemgetter("query") | self.executing_query()
            )
            | self.get_answer()
        )
    
    def invoking_chain(self):
        self.chain = self.create_chain()
        return self.chain.invoke({"question": self.question})
    
    def initiate_sql_pipeline(self,):
        return self.invoking_chain()