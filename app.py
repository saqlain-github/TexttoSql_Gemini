from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os

from textToSql.logging import logger
from textToSql.pipeline_agent import QAOverSQLiteConnection

if __name__ == "__main__":
    try:
        logger.info("Starting Application")
        ## Streamlit App
        st.set_page_config(page_title="I can Retrieve Any SQL query")
        st.header("App To Retrieve SQL Data")
        question=st.text_input("Input: ",key="input")
        submit=st.button("Ask the question")

        # if submit is clicked
        if submit:
            logger.info("User entered submit Button")
            chain = QAOverSQLiteConnection(question)
            response=chain.initiate_sql_pipeline()
            print(response)
            # response=read_sql_query(response,"student.db")
            st.subheader("The Response is")
            st.write(response)
            logger.info(f"Response Generated {response}")
            logger.info("Completed Application")
    except Exception as e:
        logger.error("Error occured while executing the application")








