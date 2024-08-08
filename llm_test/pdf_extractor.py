import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path, txt_path):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Open the text file for writing
    with open(txt_path, 'w', encoding='utf-8') as text_file:
        # Iterate through each page in the PDF
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            # Extract text from the page
            text = page.get_text()
            # Write the text to the file
            text_file.write(text)
            text_file.write("\n\n")  # Separate pages with two newlines

    # Close the PDF document
    pdf_document.close()
    print('document exported!')

# Paths to the PDF and the output text file
pdf_path = 'llm_test/data/kidrock.pdf'
txt_path = 'llm_test/data/kidrock.txt'

# Extract text from the PDF and save it to a text file
extract_text_from_pdf(pdf_path, txt_path)
