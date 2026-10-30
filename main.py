from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from ingest import process_and_store_pdf
from retrieve import ask_question

app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
        
    # Save the uploaded file temporarily to disk so pypdf can read it
    temp_file_path = f"temp_{file.filename}"
    with open(temp_file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    try:
        chunks_saved = process_and_store_pdf(temp_file_path)
        return {"message": f"Successfully stored {chunks_saved} chunks from {file.filename}"}
    finally:
        # Clean up the temporary file immediately after ingestion
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/ask")
def ask(request: QuestionRequest):
    return ask_question(request.question)