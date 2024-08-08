import sys
import os
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

def file_checker(file, user_query):
    try:
        loader = TextLoader(file)
        documents = loader.load()
    except FileNotFoundError:
        print(f"File not found: {file}")
        return None

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        return None
    embedder = OpenAIEmbeddings(openai_api_key=openai_api_key)

    docsearch = Chroma.from_documents(texts, embedder)

    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-4-turbo-preview", openai_api_key=openai_api_key),
        chain_type="stuff",
        retriever=docsearch.as_retriever(search_kwargs={"k": 1})
    )

    answer = qa.invoke(user_query)

    return answer["result"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <filename>")
    else:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(f"The file {filename} does not exist.")
        else:
            user_query = input("Enter your query about the text: ")
            answer = file_checker(filename, user_query)
            if answer:
                print("Answer:", answer)
            else:
                print("No answer generated.")
