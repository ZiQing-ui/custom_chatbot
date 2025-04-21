import streamlit as st
from from langchain_community.llms import Ollama

llm = Ollama(model="llama2")

st.title("Local LLM Chatbot")
prompt = st.text_input("Enter your prompt:")
if prompt:
    response = llm(prompt)
    st.write(response)
