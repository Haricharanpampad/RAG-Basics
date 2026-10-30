import chromadb
from chromadb.utils import embedding_functions
import ollama

def ask_question(question: str):
# 'chromadb' matches the service name in docker-compose.yml
    client = chromadb.HttpClient(host="chromadb", port=8000)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    try:
        collection = client.get_collection(name="pdf_collection", embedding_function=sentence_transformer_ef)
    except Exception:
        return {"answer": "Database is empty. Please upload a PDF first.", "sources": []}
        
    results = collection.query(query_texts=[question], n_results=3)
    
    if not results["documents"] or not results["documents"][0]:
        return {"answer": "No relevant documents found.", "sources": []}
        
    retrieved_chunks = results["documents"][0]
    context = "\n\n---\n\n".join(retrieved_chunks)

    prompt = f"""Answer the question ONLY using the provided context. If you cannot answer based on the context, politely state that the information is not in the document.

    Context:
    {context}

    Question: {question}
    Answer:"""

    from ollama import Client
# 'ollama' matches the service name in docker-compose.yml
    ollama_client = Client(host="http://ollama:11434")
    response = ollama_client.generate(model="llama3.2", prompt=prompt)
    
    return {
        "answer": response["response"],
        "sources": retrieved_chunks
    }