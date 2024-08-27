import streamlit as st
import time
from text_retrieval import process_text_file, query_model

# Specify the path to the text file
TEXT_FILE_PATH = "llm_test/data/silly.txt"


# 01 HEADER AND VISUAL LAYOUT
st.set_page_config(layout="wide")

hl, space, hr = st.columns((1, 5, 1))
with hr:
    st.image('speckle/pz_logo.png', width=200)

with hl:
    st.image('speckle/logo.png', width=250)

st.title("PROJECT ZERO: Project Analytics")




# ////////////////////////////////////////////////////////////////
def type_writer(text, speed=0.02):
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(typed_text)
        time.sleep(speed)
    return typed_text

def main():
    st.title("Text File Chatbot")

    docsearch, error = process_text_file(TEXT_FILE_PATH)

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if error:
        st.error(error)
    else:
        user_query = st.chat_input("Enter your query about the text:")
        if user_query:
            # Display user message in chat message container
            st.chat_message("user").markdown(user_query)
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": user_query})

            # Query the model and get the result
            result = query_model(docsearch, user_query)

            # Simulate typing for assistant response
            with st.chat_message("assistant"):
                typed_response = type_writer(result)

            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": typed_response})

if __name__ == "__main__":
    main()
