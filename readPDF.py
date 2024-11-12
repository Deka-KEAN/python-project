import os
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import requests

os.environ["GROQ_API_KEY"]=""

groq_api_key = ""

pdfReader = PdfReader("C:/Users/anupd/OneDrive/Desktop/Itinerary.pdf")


raw_text = ''
for i, page in enumerate(pdfReader.pages):
    content = page.extract_text()
    if content:
        raw_text += content

# print(raw_text)

text_splitter = CharacterTextSplitter(
    separator = "\n",
    chunk_size = 800,
    chunk_overlap  = 200,
    length_function = len,
)
texts = text_splitter.split_text(raw_text)

print(len(texts))
import groq

groq_client = groq.Client(api_key=groq_api_key)
# embeddings = groq_client.embed_text(raw_text)

query = "What is the travel time?"
response = groq_client.query_document(text=raw_text, query=query)
print("Answer:", response)

# def create_embeddings(text):
#     response = requests.post(
#         groq_embeddings_url,
#         headers={"Authorization": f"Bearer {groq_api_key}"},
#         json={"text": text}
#     )
#     return response.json()["embeddings"]

# # Create embeddings for each chunk
# embeddings = create_embeddings(texts)
# import numpy as np

# # Convert embeddings into a numpy array
# embeddings_matrix = np.array(embeddings)


# document_search = FAISS.from_embeddings(texts, embeddings)


# query = "What is the travel time?"
# similar_docs = document_search.similarity_search(query)

# # Print the most relevant document chunks
# for doc in similar_docs:
#     print(doc['text'])