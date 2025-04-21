import streamlit as st
from langchain_community.llms import Ollama

# Initialize LLM
llm = Ollama(model="llama2")  # or use "llama3:latest" if needed

# Streamlit UI
st.title("🦙 Chat with LLaMA 2 (Local via Ollama)")

prompt = st.text_area("Enter your prompt:", height=150)

if st.button("Generate"):
    if prompt.strip() != "":
        with st.spinner("Generating response..."):
            response = llm.invoke(prompt)
            st.markdown("### 💬 Response:")
            st.write(response)
    else:
        st.warning("Please enter a prompt.")
