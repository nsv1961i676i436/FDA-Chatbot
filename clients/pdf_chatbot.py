# Calls /ask endpoint

import streamlit as st
import requests
from app.utils.pdf import extract_sections_from_pdf

API_URL = "http://localhost:8000/ask"

st.title("💊 FDA Drug Chatbot")
st.write("Upload a drug label PDF and ask questions!")

uploaded_file = st.file_uploader("📄 Upload PDF", type="pdf")

if uploaded_file:
    extracted = extract_sections_from_pdf(uploaded_file)
    st.success("Sections extracted. Ask a question!")

    question = st.text_input("Ask a question:")
    if question:
        with st.spinner("Thinking..."):
            response = requests.post(API_URL, json={
                "question": question,
                "context": extracted
            })
            answer = response.json()["answer"]
        st.markdown(f"**💬 Answer:** {answer}")
