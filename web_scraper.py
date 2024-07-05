from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_openai import ChatOpenAI
#from langchain.chains import create_extraction
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains import create_extraction_chain
import pprint
from langchain_openai import OpenAIEmbeddings

from dotenv import load_dotenv
load_dotenv(".env")

## STANDARD SCRAPE?
loader = AsyncChromiumLoader(["https://www.natwest.com/life-moments/managing-your-money/top-money-saving-tips.html"])
html = loader.load()

# Transform
bs_transformer = BeautifulSoupTransformer()
docs_transformed = bs_transformer.transform_documents(html, tags_to_extract=["h2","h3","p","li"])

print(docs_transformed[0].page_content[0:30000])

# #### SCRAPING WITH EXTRACTION
# llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0613")

# schema = {
#     "properties": {
#         "Money_saver_header": {"type": "string"},
#         "Money_saver_content": {"type": "string"},
#     },
#     "required": ["header", "content"],
# }
# def extract(content: str, schema: dict):
#     return create_extraction_chain(schema=schema, llm=llm).run(content)

# def scrape_with_playwright(urls, schema):
#     loader = AsyncChromiumLoader(urls)
#     docs = loader.load()
#     bs_transformer = BeautifulSoupTransformer()
#     docs_transformed = bs_transformer.transform_documents(
#         docs, tags_to_extract=["span"]
#     )
#     print("Extracting content with LLM")

#     # Grab the first 1000 tokens of the site
#     splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
#         chunk_size=1000, chunk_overlap=0
#     )
#     splits = splitter.split_documents(docs_transformed)

#     # Process the first split
#     extracted_content = extract(schema=schema, content=splits[0].page_content)
#     pprint.pprint(extracted_content)
#     return extracted_content

# urls = ["https://www.natwest.com/life-moments/managing-your-money/top-money-saving-tips.html"]
# extracted_content = scrape_with_playwright(urls, schema=schema)


##### QA over website

# from langchain.docstore.document import Document
# from langchain.indexes import VectorstoreIndexCreator
# from langchain_community.utilities import ApifyWrapper


# apify = ApifyWrapper()
# # Call the Actor to obtain text from the crawled webpages
# loader = apify.call_actor(
#     actor_id="apify/website-content-crawler",
#     run_input={"startUrls": [{"url": "https://www.natwest.com/life-moments/managing-your-money.html/"}]},
#     dataset_mapping_function=lambda item: Document(
#         page_content=item["text"] or "", metadata={"source": item["url"]}
#     ),
# )

# # Create a vector store based on the crawled data
# index = VectorstoreIndexCreator().from_loaders([loader])

# # Query the vector store
# query = "What do I do if my account is in collections or recoveries?"
# result = index.query(query)
# print(result)


   