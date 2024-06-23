import streamlit as st
import openai
import os
from dotenv import load_dotenv
from docx import Document
import fitz  # PyMuPDF

# Load environment variables from the .env file
load_dotenv()

# Securely get the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Document Analysis with ChatGPT-4")

uploaded_file = st.file_uploader("Choose a document...", type=["txt", "pdf", "docx"])

def read_file(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/pdf":
        return read_pdf(file)
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return read_docx(file)
    else:
        return None

def read_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def read_docx(file):
    doc = Document(file)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

if uploaded_file is not None:
    content = read_file(uploaded_file)
    if content is not None:
        st.write("Document Content:")
        st.text_area("Document Content", content, height=300)
        
        if st.button("Analyze with ChatGPT-4"):
            with st.spinner('Analyzing...'):
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": content}
                    ]
                )
                analysis = response.choices[0].message["content"]
                st.write("Analysis:")
                st.write(analysis)
    else:
        st.error("Unsupported file type or error reading the file.")
