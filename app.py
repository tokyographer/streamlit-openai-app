import streamlit as st
import openai
import os
from dotenv import load_dotenv
import textract

# Load environment variables from the .env file
load_dotenv()

# Securely get the OpenAI API key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("Document Analysis with ChatGPT-4")

uploaded_file = st.file_uploader("Choose a document...", type=["txt", "pdf", "docx"])

def read_file(file):
    if file.type == "text/plain":
        return file.read().decode("utf-8")
    elif file.type == "application/pdf" or file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        return textract.process(file).decode("utf-8")
    else:
        return None

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
                analysis = response['choices'][0]['message']['content']
                st.write("Analysis:")
                st.write(analysis)
    else:
        st.error("Unsupported file type.")
