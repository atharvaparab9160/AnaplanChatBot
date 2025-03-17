examples = [
    {
        "input": "List all Toyota cars priced over 20,000.",
        "query": "SELECT * FROM car_sales WHERE Brand = 'Toyota' AND Price > 20000;"
    },
    {
        "input": "Get the highest price of any car available.",
        "query": "SELECT MAX(Price) FROM car_sales;"
    },
    {
        "input": "Show details of all crossover body type cars.",
        "query": "SELECT * FROM car_sales WHERE Body = 'crossover';"
    },
    {
        "input": "Retrieve the models of cars manufactured in the year 2016.",
        "query": "SELECT Model FROM car_sales WHERE Year = 2016;"
    },
    {
        "input": "List all cars with mileage less than 200,000.",
        "query": "SELECT * FROM car_sales WHERE Mileage < 200000;"
    },
    {
        "input": "What is the price of a 2008 Volkswagen Touareg?",
        "query": "SELECT Price FROM car_sales WHERE Brand = 'Volkswagen' AND Model = 'Touareg' AND Year = 2008 LIMIT 1;"
    }
]

from langchain_community.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
import streamlit as st

from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

@st.cache_resource
def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
        FAISS,
        k=2,
        input_keys=["input"],
    )
    return example_selector


