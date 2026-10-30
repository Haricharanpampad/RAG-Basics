import chromadb
from chromadb.utils import embedding_functions
from pypdf import PdfReader
import ollama

# --- 1. Extract Text from PDF ---
print("Extracting text from PDF...")
reader = PdfReader("ewb.pdf")
full_text = ""
for page in reader.pages:
    extracted = page.extract_text()
    if extracted:
        full_text += extracted + "\n"

# --- 2. Chunk the Text ---
# ~500 characters with a 50-character overlap to prevent cutting sentences in half
print("Chunking text...")
chunk_size = 500
chunk_overlap = 50
chunks = []

start = 0
while start < len(full_text):
    end = start + chunk_size
    chunks.append(full_text[start:end])
    start += (chunk_size - chunk_overlap)

# --- 3 & 4. Embed and Store in ChromaDB ---
print(f"Embedding and storing {len(chunks)} chunks in ChromaDB (this may take a moment on the first run to download the embedding model)...")
client = chromadb.Client() # Creates an in-memory database for this script run

# This uses sentence-transformers locally under the hood
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

collection = client.create_collection(name="pdf_collection", embedding_function=sentence_transformer_ef)

# Add chunks with unique IDs
collection.add(
    documents=chunks,
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# --- 5. Retrieve Top 3 Chunks ---
# Change this question to test different scenarios
question = "where is this delivery is going on whose name  and what type of product it is and what is the vechile number and bill number is what?  "
# question = "What is the recipe for a chocolate cake?" # (Use this to test a question the PDF can't answer)

print(f"\nQuestion: {question}")
results = collection.query(
    query_texts=[question],
    n_results=3
)

retrieved_chunks = results["documents"][0]
context = "\n\n---\n\n".join(retrieved_chunks)

# --- 6. Generate Answer with Ollama ---
print("\nGenerating answer...")
prompt = f"""Answer the question ONLY using the provided context. If you cannot answer based on the context, politely state that the information is not in the document.

Context:
{context}

Question: {question}
Answer:"""

response = ollama.generate(model="llama3.2", prompt=prompt)
print("\n=== AI Answer ===")
print(response["response"])