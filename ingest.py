import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader

def process_and_store_pdf(file_path: str):
    # 1. Extract
    reader = PdfReader(file_path)
    full_text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            full_text += extracted + "\n"

    # 2. Chunk
    chunk_size = 500
    chunk_overlap = 50
    chunks = []
    start = 0
    while start < len(full_text):
        end = start + chunk_size
        chunks.append(full_text[start:end])
        start += (chunk_size - chunk_overlap)

    # 3. Store persistently
    # 'chromadb' matches the service name in docker-compose.yml
    client = chromadb.HttpClient(host="chromadb", port=8000)
    sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    
    # get_or_create allows adding multiple PDFs to the same database over time
    collection = client.get_or_create_collection(name="pdf_collection", embedding_function=sentence_transformer_ef)
    
    existing_count = collection.count()
    ids = [f"chunk_{i + existing_count}" for i in range(len(chunks))]
    
    collection.add(documents=chunks, ids=ids)
    return len(chunks)