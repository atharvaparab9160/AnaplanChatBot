import os
import streamlit as st
db_user = st.secrets["db_user"]
db_password = st.secrets["db_password"]
port = st.secrets["port"]
db_host = st.secrets["db_host"]
db_name = st.secrets["db_name"]

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
    
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{port}/{db_name}")
    OPENAI_API_KEY = st.secrets["openAi_API_Key"]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    generate_query = create_sql_query_chain(llm, db,final_prompt)
    # st.write("QUERY:",generate_query)
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
            from matplotlib import figure as figuretype
            if type(message["content"]) == figuretype.Figure :
                history.add_user_message("Data visualization")
            else:
                history.add_user_message(message["content"])
        else:
            from matplotlib import figure as figuretype
            if type(message["content"]) == figuretype.Figure :
                history.add_ai_message("Data visualization")
            else:
                history.add_ai_message(message["content"])
    return history

def invoke_chain(question,messages):
    try:
        chain = get_chain()
        history = create_history(messages)
        response = chain.invoke({"question": question,"top_k":3,"messages":history.messages})
        history.add_user_message(question)
        history.add_ai_message(response)
        return response
    except:
        return "You have reached your daily limit. Please try again tomorrow."   
    



