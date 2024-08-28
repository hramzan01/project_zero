import streamlit as st
import os
from PIL import Image
import fitz
import io
import time
from text_retrieval import process_text_file, query_model
from pdf_extractor import extract_text_from_pdf

# Set the page layout
st.set_page_config(layout="wide")

# Header and layout
hl, space, hr = st.columns((1, 5, 1))
with hr:
    st.image('speckle/pz_logo.png', width=200)

with hl:
    st.image('speckle/logo.png', width=250)

st.title("PROJECT ZERO: Project Analytics")


#//////////////////////////////////////////////////////////////////////////////

# Function to simulate typing
def type_writer(text, speed=0.02):
    placeholder = st.empty()
    typed_text = ""
    for char in text:
        typed_text += char
        placeholder.markdown(typed_text)
        time.sleep(speed)
    return typed_text

# Main function
def main():
    st.subheader("Project Zero AI Assistant")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        # Load the PDF
        pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        # Extract the first page
        first_page = pdf_document.load_page(0)

        # Convert the page to an image
        pix = first_page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes()))

        # Display the image
        st.image(image, caption='First page of uploaded PDF', use_column_width=True)


    txt_path = None  # Initialize txt_path to avoid reference error

    if uploaded_file is not None:
        # Create a temporary directory to store the uploaded PDF
        temp_dir = "temp_files"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Define paths for the temporary PDF and the output text file
        temp_pdf_path = os.path.join(temp_dir, uploaded_file.name)
        txt_path = temp_pdf_path.replace(".pdf", ".txt")

        # Save the uploaded file to the temporary directory
        with open(temp_pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Call the function to extract text
        try:
            text_file_path = extract_text_from_pdf(temp_pdf_path, txt_path)
            st.success(f"Text extracted and saved to {text_file_path}")

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    if txt_path:  # Ensure txt_path is defined before using it
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages from history on app rerun
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        docsearch, error = process_text_file(txt_path)

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
