
# from langchain_community.vectorstores import ElasticsearchStore
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.document_loaders import TextLoader
# from langchain_text_splitters import CharacterTextSplitter

# def elastic(query):
#     embeddings = OpenAIEmbeddings()

#     loader = TextLoader("/Users/chrisbooth/Coding/ragvsgrag/MOD_IPR_Policy_Statement.txt") #change to web scraper 
#     documents = loader.load()
#     text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
#     docs = text_splitter.split_documents(documents)

#     vectorstore = ElasticsearchStore.from_documents(
#         docs,
#         embedding=embeddings,
#         es_url="http://localhost:9200",
#         es_user="elastic",
#         es_password="cAe4zmUZlFg9+a78O4=F",
#         index_name="test-basic",
#     )

#     vectorstore.client.indices.refresh(index="test-basic")

#     elastic_results = vectorstore.similarity_search(query)
    
#     return elastic_results
