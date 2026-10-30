# 📄 Dockerized RAG PDF Chatbot

A full-stack Retrieval-Augmented Generation (RAG) application that allows users to upload PDF documents and ask questions about their content. The system ensures the AI only answers based on the provided document context to prevent hallucinations.

## 🛠️ Tech Stack
* **Frontend**: Streamlit
* **Backend**: FastAPI
* **Vector Database**: ChromaDB (Persistent)
* **LLM / Embeddings**: Ollama (Llama 3.2) & Sentence-Transformers (all-MiniLM-L6-v2)
* **Infrastructure**: Docker & Docker Compose

## 📋 Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
* If you have a local Windows installation of Ollama, ensure it is completely quit (check the system tray) to avoid port 11434 conflicts.

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
   cd YOUR_REPO_NAME