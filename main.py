import streamlit as st
import PyPDF2
import requests
import json

# Extract text from uploaded PDF
def extract_text_from_pdf(pdf_file):
    try:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

# Generator for streaming responses from LLaMA 3.1 via Ollama
def stream_llama_response(prompt):
    try:
        payload = {
            "model": "llama3.1",  # Ensure this matches your model name in Ollama
            "prompt": prompt,
            "stream": True
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload, stream=True)
        response.raise_for_status()

        partial_text = ""
        for line in response.iter_lines():
            if line:
                chunk = line.decode("utf-8").replace("data: ", "")
                try:
                    json_data = json.loads(chunk)
                    token = json_data.get("response", "")
                    partial_text += token
                    yield partial_text
                except:
                    continue
    except Exception as e:
        yield f"Error from model: {str(e)}"

# Streamlit UI
st.set_page_config(page_title="📄🦙 PDF Chat + Image + LLaMA", layout="wide")
st.title("📄🦙 Chat with LLaMA 3.1 (PDF + Image Input)")

# Session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# File upload
col1, col2 = st.columns(2)
with col1:
    uploaded_pdf = st.file_uploader("Upload a PDF file", type=["pdf"])
with col2:
    uploaded_image = st.file_uploader("Upload an image (optional)", type=["png", "jpg", "jpeg"])

# User input
user_input = st.text_area("Enter your message", height=120)

# Chat display
st.subheader("💬 Chat")
chat_container = st.empty()

# Send button
if st.button("Send"):
    if user_input.strip() == "":
        st.warning("Please enter a message.")
    else:
        # Add user message
        st.session_state.chat_history.append(("User", user_input))

        # Extract PDF content if available
        context = "You are a helpful assistant.\n"
        if uploaded_pdf:
            pdf_text = extract_text_from_pdf(uploaded_pdf)
            if pdf_text.startswith("Error"):
                st.session_state.chat_history.append(("Assistant", pdf_text))
                st.stop()
            context += f"Based on this PDF:\n{pdf_text}\n\n"

        # Optionally process image (future feature, like OCR)
        if uploaded_image:
            context += "(An image was also provided, but image processing is not yet enabled.)\n\n"

        # Add conversation history
        for role, msg in st.session_state.chat_history:
            context += f"{role}: {msg}\n"
        context += "Assistant:"

        # Stream and display assistant response
        full_response = ""
        response_placeholder = chat_container.empty()
        for chunk in stream_llama_response(context):
            full_response = chunk
            response_placeholder.markdown(f"**Assistant:** {full_response}")

        st.session_state.chat_history.append(("Assistant", full_response))

# Display full chat history
for role, message in st.session_state.chat_history:
    st.markdown(f"**{role}:** {message}")

