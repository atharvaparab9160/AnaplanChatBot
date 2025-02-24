import os
# from dotenv import load_dotenv
#
# load_dotenv()

db_user = "AnaplanChatbot_flewrollit"
db_password = "e375971f9b738b06efe30896c9a1f414120930f2"
port = "3307"
db_host = "x6mxp.h.filess.io"
db_name = "AnaplanChatbot_flewrollit"

OPENAI_API_KEY = "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"
LANGCHAIN_TRACING_V2 = "true"
LANGCHAIN_API_KEY = "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"
import os
# from langchain_deepseek import ChatDeepSeek
# os.environ["DEEPSEEK_API_KEY"] = getpass.getpass("Enter your DeepSeek API key: ")
# os.environ[
#     "OPENAI_API_KEY"] = "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"
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ[
#     "LANGCHAIN_API_KEY"] = "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"
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from langchain.memory import ChatMessageHistory

from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser

from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI

from table_details import table_chain as select_table
from prompts import final_prompt, answer_prompt

import streamlit as st
@st.cache_resource
def get_chain():
    print("Creating chain")
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    generate_query = create_sql_query_chain(llm, db,final_prompt)
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = generate_query | execute_query
    chain = (
    RunnablePassthrough.assign(table_names_to_use=select_table) |
    RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query
    )
    | rephrase_answer
)

    return chain

def create_history(messages):
    history = ChatMessageHistory()
    for message in messages:
        if message["role"] == "user":
            history.add_user_message(message["content"])
        else:
            history.add_ai_message(message["content"])
    return history

def invoke_chain(question,messages):
    chain = get_chain()
    history = create_history(messages)
    response = chain.invoke({"question": question,"top_k":3,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response


