# app.py
import streamlit as st
from text_retrieval import process_text_file, query_model

# Specify the path to the text file
TEXT_FILE_PATH = "llm_test/data/kidrock.txt"

def main():
    st.title("Text File Chatbot")

    docsearch, error = process_text_file(TEXT_FILE_PATH)
    if error:
        st.error(error)
    else:
        user_query = st.text_input("Enter your query about the text:")
        if user_query:
            result = query_model(docsearch, user_query)
            st.write("Answer:", result)

if __name__ == "__main__":
    main()
