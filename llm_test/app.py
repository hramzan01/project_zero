import streamlit as st
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

            # Display assistant response in chat message container
            st.chat_message("assistant").markdown(result)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": result})

if __name__ == "__main__":
    main()
