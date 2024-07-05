from langchain_core.runnables import (
    RunnableBranch,
    RunnableLambda,
    RunnableParallel,
    RunnablePassthrough,
)
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import Tuple, List, Optional
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain.text_splitter import TokenTextSplitter
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from neo4j import GraphDatabase
from langchain_community.vectorstores import Neo4jVector
from langchain_community.document_loaders import TextLoader

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH, encrypted=False)

graph = Neo4jGraph()

file_path = [r"C:\Users\chris\Coding\ragvsgrag\10_ways_to_save.txt"]

documents = []

for path in file_path:
    loader = TextLoader(path)
    documents.append(loader.load())

raw_documents = loader.load()
# text_splitter = TokenTextSplitter(chunk_size=512, chunk_overlap=24)
# documents = text_splitter.split_documents(raw_documents[:3])

# Construct the Graph
llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo")
llm_transformer = LLMGraphTransformer(
    llm=llm,
    allowed_nodes=["Web_page", "Guidance", "Product", "Payment method"],
    allowed_relationships=["CONTAINS", "GIVES", "USES", "SOURCED_FROM", "MANAGES"],
    #node_properties=["text", "source", "URL"]
    )

graph_documents = llm_transformer.convert_to_graph_documents(raw_documents)
print(graph_documents)
graph.add_graph_documents(
    graph_documents,
    baseEntityLabel=True,
    include_source=True
)

