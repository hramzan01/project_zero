import sys
import os
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import TextLoader
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma

def file_checker(file): # a path to a file, in our case a text file containing code.
    try:
        # Instantiate our Text Loader.
        loader = TextLoader(file)
        # Load our file now.
        documents = loader.load()
    except FileNotFoundError:
        print(f"File not found: {file}")
        return None

    # Instantiate the textsplitter moudle to break our file into smaller chunks.
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # Split our our chosen file.
    texts = text_splitter.split_documents(documents)

    # Instantiate a Embedder from OpenAI using our secret key
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        print("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")
        return None
    embedder = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Use the embedder to populate a Chroma vector store with our texts.
    docsearch = Chroma.from_documents(texts, embedder)


    # instantiate a Retrieval Chain from openAI, with our key, chain_type="stuff" means the model 'stuffs' all
    # our text into a single prompt (highly unlikely any of our text files will be too large for this model to handle).
    # We set our model to be the latest GPT-4-Turbo model.
    qa = RetrievalQA.from_chain_type(llm=ChatOpenAI(model_name="gpt-4-turbo-preview",
                                                    openai_api_key=openai_api_key),
                                     chain_type="stuff",
                                     retriever=docsearch.as_retriever(search_kwargs={"k": 1}))

    # The prompt we want to ask the model.
    query = "Rate the following Python code out of 10. Give three improvements that can be made to it"

    # Invoke the model with our query.
    answer = qa.invoke(query)

    return answer["result"]

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <filename>")
    else:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(f"The file {filename} does not exist.")
        else:
            answer = file_checker(filename)
            if answer:
                print("Answer:", answer)
            else:
                print("No answer generated.")
