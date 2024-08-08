# text_retrieval.py
import os
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

def process_text_file(file_path):
    try:
        loader = TextLoader(file_path)
        documents = loader.load()
    except FileNotFoundError:
        return None, "File not found."

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        return None, "OpenAI API key not found. Set the OPENAI_API_KEY environment variable."

    embedder = OpenAIEmbeddings(openai_api_key=openai_api_key)
    docsearch = Chroma.from_documents(texts, embedder)

    return docsearch, None

def query_model(docsearch, user_query):
    openai_api_key = os.getenv('OPENAI_API_KEY')
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4-turbo-preview", openai_api_key=openai_api_key),
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 1})
    )

    answer = qa.invoke(user_query)
    return answer["result"]
