import os
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Neo4jVector
from langchain_openai import OpenAIEmbeddings
from neo4j import GraphDatabase
from langchain_community.graphs import Neo4jGraph
from dotenv import load_dotenv
load_dotenv(".env")

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))

driver = GraphDatabase.driver(URI, auth=AUTH, encrypted=False)

graph = Neo4jGraph()

def neo_vector_Documents(question):

    vector_index = Neo4jVector.from_existing_graph(
    embedding=OpenAIEmbeddings(),
    search_type="hybrid",
    node_label="Document",
    text_node_properties=["text"],
    embedding_node_property="embedding"
)

    return vector_index



# This ingests document and vectorises in neo4j
# def neo4j_demo(query):
#     loader = TextLoader("/Users/chrisbooth/Coding/ragvsgrag/MOD_IPR_Policy_Statement.txt")

#     documents = loader.load()
#     text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#     docs = text_splitter.split_documents(documents)

#     # The Neo4jVector Module will connect to Neo4j and create a vector index if needed.

#     db = Neo4jVector.from_documents(
#         docs, embedding = OpenAIEmbeddings(), 
#         url=os.getenv('NEO4J_URL'), 
#         username=os.getenv('NEO4J_USERNAME'), 
#         password=os.getenv('NEO4J_PASSWORD'),
#     )

#     query = "How does the MOD view the exploitation of IP for the wider UK economy?"
#     docs_with_score = db.similarity_search_with_score(query, k=2)

#     return docs_with_score


# This uses a pre-existing graph and configures a keyword and Vector search (ie.hybrid) targeting nodes labelled 'Document'
