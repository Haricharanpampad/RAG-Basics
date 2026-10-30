import streamlit as st
import requests

# This matches the FastAPI service name and internal port in docker-compose.yml
API_URL = "http://api:8000"

st.set_page_config(page_title="RAG PDF Chatbot", page_icon="📄")
st.title("📄 RAG PDF Chatbot")

# --- Sidebar: File Upload ---
with st.sidebar:
    st.header("1. Upload Document")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
    
    if st.button("Process PDF"):
        if uploaded_file is not None:
            with st.spinner("Uploading and chunking..."):
                # Send file to FastAPI
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json()["message"])
                    else:
                        st.error(f"API Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to connect to backend: {e}")
        else:
            st.warning("Please select a file first.")

# --- Main Page: Chat Interface ---
st.header("2. Ask Questions")
question = st.text_input("What would you like to know about the document?")

if st.button("Ask"):
    if question:
        with st.spinner("Generating answer..."):
            try:
                # Send question to FastAPI
                response = requests.post(f"{API_URL}/ask", json={"question": question})
                
                if response.status_code == 200:
                    data = response.json()
                    
                    st.markdown("### Answer")
                    st.write(data["answer"])
                    
                    # Optional expander to let users see the raw text chunks retrieved
                    with st.expander("View Source Chunks"):
                        for i, chunk in enumerate(data.get("sources", [])):
                            st.markdown(f"**Chunk {i+1}:**")
                            st.info(chunk)
                else:
                    st.error(f"API Error: {response.text}")
            except Exception as e:
                st.error(f"Failed to connect to backend: {e}")
    else:
        st.warning("Please type a question.")